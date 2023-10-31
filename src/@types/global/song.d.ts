
export type Length = "full" | "short";

// live: セトリの決まったライブ
// known: チャレンジではない、一度やったことがあるような歌
// improvised: チャレンジなどの即興演奏
export type SingType = "live" | "known" | "improvised"

export interface Song {
  artist: string;
  name: string;
  video: string;
  t: number;
  endt: number | null;
  length: Length | null;
  singType: SingType | null;
  recommended?: boolean;
}

export interface SongJson {
  songs: {
    [uuid: string]: Song;
  },
}

declare module "@/@types/global/songs.json" {
  const value: SongJson;
  export default value;
}

