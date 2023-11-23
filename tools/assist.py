import dataclasses
import itertools
import json
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

import pyperclip
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

COMMAND_LIST = {
    "write": "write to src/songs.json",
    "add": "add song to buffer",
    "exit": "write to src/songs.json and exit",
    "live": "timestamp mode in live stream",
}


def youtube_url(video_id: str, second: int) -> str:
    return f"https://youtube.com/watch?v={video_id}&t={second}"


def time_to_second(time_str: str) -> int:
    """
    time_str: str
        [[[%H:]%M:]%S]
    """
    time_parts = time_str.split(":") if len(time_str) > 0 else []
    hours = int(time_parts[-3]) if len(time_parts) == 3 else 0
    minutes = int(time_parts[-2]) if len(time_parts) >= 2 else 0
    seconds = int(time_parts[-1]) if len(time_parts) >= 1 else 0
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds


def datetime_to_time(t: datetime, base: datetime) -> str:
    delta = t - base
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    seconds = delta.seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


class LengthEnum(str, Enum):
    full = "full"
    short = "short"

    @staticmethod
    def all() -> list[str]:
        return [x.value for x in LengthEnum]


class SingTypeEnum(str, Enum):
    live = "live"
    known = "known"
    improvised = "improvised"
    shorts = "shorts"
    movie = "movie"

    @staticmethod
    def all() -> list[str]:
        return [x.value for x in SingTypeEnum]


@dataclass
class SongInfo:
    uuid: str
    name: str
    video: str
    t: int
    recommended: bool
    endt: Optional[int] = None
    length: Optional[LengthEnum] = None
    singType: Optional[SingTypeEnum] = None

    @staticmethod
    def input_artist(
        data: dict[str, list["SongInfo"]], song: Optional[str] = None, default: str = ""
    ) -> Optional[str]:
        if song is None:
            artists_completer = WordCompleter(list(data.keys()))
        else:
            artist_candidates: set[str] = set()
            for artist, songs in data.items():
                if song in set(map(lambda song: song.name, songs)):
                    artist_candidates.add(artist)
            artists_completer = WordCompleter(list(artist_candidates))
        artist = (
            prompt("artist> ", completer=artists_completer, default=default) or None
        )
        return artist

    @staticmethod
    def input_song(
        data: dict[str, list["SongInfo"]],
        artist: Optional[str] = None,
        default: Optional[str] = None,
    ) -> str:
        songs_completer = WordCompleter(
            list(
                set(
                    map(
                        lambda x: x.name,
                        data.get(artist, []) if artist is not None else [],
                    )
                )
            )
        )
        song = prompt("song> ", completer=songs_completer, default=default or "")
        return song

    @staticmethod
    def input_video(
        data: dict[str, list["SongInfo"]],
        default: Optional[str] = None,
    ) -> str:
        videos_completer = WordCompleter(
            list(
                set(
                    map(
                        lambda song: song.video,
                        itertools.chain.from_iterable(data.values()),
                    )
                )
            )
        )
        video = prompt("video> ", completer=videos_completer, default=default or "")
        return video

    @staticmethod
    def input_length(default: Optional[LengthEnum] = None) -> Optional[LengthEnum]:
        try:
            length_completer = WordCompleter(LengthEnum.all())
            length = prompt(
                "length> ",
                completer=length_completer,
                default=str(default) if default is not None else "",
            )
            return LengthEnum[length]
        except KeyError:
            print("Warning: KeyError")
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def input_singtype(
        default: Optional[SingTypeEnum] = None,
    ) -> Optional[SingTypeEnum]:
        singtype_completer = WordCompleter(SingTypeEnum.all())
        try:
            sing_type = prompt(
                "singType> ",
                completer=singtype_completer,
                default=str(default) if default is not None else "",
            )
            return SingTypeEnum[sing_type]
        except KeyError:
            print("Warning: KeyError")
        except Exception as e:
            print(e)
        return None


class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SongInfo):
            return dataclasses.asdict(obj)
        return json.JSONEncoder.default(self, obj)


class Commands:
    COMMAND_LIST = {
        "write": "write to src/songs.json",
        "add": "add song to buffer",
        "exit": "write to src/songs.json and exit",
        "live": "timestamp mode in live stream",
        "merge": "merge live command result to src/songs.json",
    }
    previous_video: Optional[str] = None
    data: dict[str, list[SongInfo]] = {}

    @classmethod
    def load(cls):
        with open("./src/songs.json", encoding="utf8") as f:
            cls.data = {
                artist: [SongInfo(**song_info) for song_info in song_infos]
                for artist, song_infos in json.load(f).items()
            }

    @classmethod
    def input_song_info(cls) -> tuple[str, SongInfo]:
        artist = SongInfo.input_artist(cls.data)

        song = SongInfo.input_song(data=cls.data, artist=artist)

        if artist is None:
            artist = SongInfo.input_artist(cls.data) or ""

        video = SongInfo.input_video(cls.data, cls.previous_video)
        cls.previous_video = video

        t = time_to_second(prompt("t> "))
        endt = time_to_second(prompt("endt> "))

        length = SongInfo.input_length()

        sing_type = SongInfo.input_singtype()

        song_info = SongInfo(
            uuid=str(uuid.uuid4()),
            name=song,
            video=video,
            t=t,
            endt=endt,
            length=length,
            singType=sing_type,
            recommended=False,
        )
        return artist, song_info

    @classmethod
    def write(cls):
        with open("./src/songs.json", "w", encoding="utf8") as f:
            f.write(
                json.dumps(
                    cls.data,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                    cls=ExtendedJSONEncoder,
                )
            )

    @classmethod
    def add(cls):
        artist, song_info = cls.input_song_info()
        cls.data.setdefault(artist, [])
        cls.data[artist].append(song_info)
        cls.data[artist].sort(key=lambda x: x.name)

        json_str = json.dumps(
            song_info,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            cls=ExtendedJSONEncoder,
        )
        print(f"{artist}: {json_str}")

    @classmethod
    def merge(cls, song_list: list[tuple[str, SongInfo]]):
        for artist, song_info in song_list:
            cls.data.setdefault(artist, [])
            cls.data[artist].append(song_info)
            cls.data[artist].sort(key=lambda x: x.name)
            json_str = json.dumps(
                song_info,
                ensure_ascii=False,
                sort_keys=True,
                indent=4,
                cls=ExtendedJSONEncoder,
            )
            print(json_str)


class LiveCommand:
    COMMAND_LIST = {
        "add": "add song to buffer",
        "base": "set base time",
        "ls": "show song list and copy it to clipboard",
        "url": "show url",
        "modify": "modify song info",
        "exit": "exit live shell",
    }
    base: Optional[datetime] = None
    _song_list: list[tuple[str, SongInfo]] = []
    video: Optional[str] = None
    data: dict[str, list[SongInfo]]

    @classmethod
    def load(cls, data: dict[str, list[SongInfo]]):
        cls.data = data

    @classmethod
    def input_song(cls) -> tuple[str, SongInfo]:
        start_timestamp = int(datetime.now().timestamp())

        artist = SongInfo.input_artist(cls.data)

        song = SongInfo.input_song(data=cls.data, artist=artist)

        if artist is None:
            artist = SongInfo.input_artist(cls.data) or ""

        video = SongInfo.input_video(cls.data, cls.video)
        cls.video = video

        length = SongInfo.input_length()

        sing_type = SongInfo.input_singtype()

        input(">>> ")
        end_timestamp = int(datetime.now().timestamp())

        song_info = SongInfo(
            uuid=str(uuid.uuid4()),
            name=song,
            video=video,
            t=start_timestamp,
            endt=end_timestamp,
            length=length,
            singType=sing_type,
            recommended=False
        )
        return artist, song_info

    @classmethod
    def add(cls):
        artist, song_info = cls.input_song()
        cls._song_list.append((artist, song_info))

    @classmethod
    def input_base(cls) -> Optional[datetime]:
        base = prompt(
            "base> ",
            default=str((cls.base or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")),
        )
        try:
            return datetime.strptime(base, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(e)

    @classmethod
    def ls(cls):
        if cls.base is None:
            print("base_time is not set, please set")
            return
        timestamp_str = ""
        for artist, song_info in cls._song_list:
            timestamp_str += (
                f"{datetime_to_time(datetime.fromtimestamp(song_info.t), cls.base)} "
                f"{datetime_to_time(datetime.fromtimestamp(song_info.endt or 0), cls.base)} "
                f"{song_info.name} / {artist}\n"
            )
        print(timestamp_str)
        pyperclip.copy(timestamp_str)

    @classmethod
    def url(cls) -> list[str]:
        if cls.base is None:
            print("base_time is not set, please set")
            return []
        if cls.video is None:
            print("video_id is not set, please set")
            return []
        urls = []
        for index, (artist, song_info) in enumerate(cls._song_list):
            delta = datetime.fromtimestamp(song_info.t) - cls.base
            url = (
                f"{index}: {song_info.name} / {artist}\n"
                f"t: {youtube_url(cls.video, int(delta.total_seconds()))}\n"
            )
            delta = datetime.fromtimestamp(song_info.endt or 0) - cls.base
            url += f"t: {youtube_url(cls.video, int(delta.total_seconds()))}\n"
            urls.append(url)
        return urls

    @classmethod
    def export_song_list(cls) -> Optional[list[tuple[str, SongInfo]]]:
        if cls.base is None:
            print("set base")
            return None
        song_list = []
        for artist, song_info in cls._song_list:
            delta = datetime.fromtimestamp(song_info.t) - cls.base
            song_info.t = int(delta.total_seconds())
            if song_info.endt is not None:
                delta = datetime.fromtimestamp(song_info.endt) - cls.base
                song_info.endt = int(delta.total_seconds())
            song_list.append((artist, song_info))
        return song_list

    @classmethod
    def modify(cls, index: int, attr: str):
        if 0 <= index < len(cls._song_list):
            artist, song_info = cls._song_list[index]
            match attr:
                case "artist":
                    artist = SongInfo.input_artist(
                        cls.data, song=song_info.name, default=artist
                    )
                case "song":
                    song_info.name = SongInfo.input_song(
                        cls.data, default=song_info.name
                    )
                case "video":
                    song_info.video = SongInfo.input_video(
                        cls.data, default=song_info.video
                    )
                case "t":
                    song_info.t = time_to_second(
                        prompt("t> ", default=str(song_info.t))
                    )
                case "endt":
                    song_info.endt = time_to_second(
                        prompt("endt> ", default=str(song_info.endt))
                    )
                case "length":
                    song_info.length = SongInfo.input_length(default=song_info.length)
                case "singtype":
                    song_info.singType = SongInfo.input_singtype(
                        default=song_info.singType
                    )
            cls._song_list[index] = (artist or "", song_info)

    @classmethod
    def live_shell(cls):
        while True:
            try:
                command_completer = WordCompleter(list(LiveCommand.COMMAND_LIST.keys()))
                match prompt(">> ", completer=command_completer).split():
                    case cmd, *cmd_args:
                        pass
                    case _:
                        continue
            except EOFError:
                if input("exit? y/n>") == "y":
                    break
                else:
                    continue

            match cmd:
                case "add":
                    LiveCommand.add()
                case "base":
                    cls.base = cls.input_base()
                case "ls":
                    cls.ls()
                case "url":
                    urls = cls.url()
                    for url in urls:
                        print(url)
                case "modify":
                    if len(cmd_args) < 2:
                        continue
                    index = int(cmd_args[0])
                    attr = cmd_args[1]
                    cls.modify(index, attr)
                case "exit":
                    break


if __name__ == "__main__":
    Commands.load()
    while True:
        try:
            command_completer = WordCompleter(list(Commands.COMMAND_LIST.keys()))
            match prompt("> ", completer=command_completer).split():
                case cmd, *cmd_args:
                    pass
                case _:
                    continue
        except EOFError:
            if input("exit? y/n>") == "y":
                Commands.write()
                break
            else:
                continue

        match cmd:
            case "write":
                Commands.write()
            case "add":
                Commands.add()
            case "merge":
                if (song_list := LiveCommand.export_song_list()) is not None:
                    Commands.merge(song_list)
                    Commands.write()
            case "exit":
                break
            case "live":
                LiveCommand.load(Commands.data)
                LiveCommand.live_shell()
