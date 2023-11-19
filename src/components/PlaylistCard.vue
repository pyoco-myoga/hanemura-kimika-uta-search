<script lang="ts" setup>
import {algoliaIndex, removePlayList} from "@/common";
import BottomListMenu from "./BottomListMenu.vue";
import PlaylistForm from "./PlaylistForm.vue";
import {useAppStore} from "@/store/app";
import {Song} from "@/@types/global/song";
import {ref} from "vue";
import {ObjectWithObjectID} from "@algolia/client-search";
import PlaylistDetailSheet from "./PlaylistDetailSheet.vue";
const store = useAppStore();
const props = defineProps<{
  playlistId: string | "favorite" | "recommended";
  playlistTitle: string;
  playlistDescription: string;
  visibility: "public" | "private",
  songs: string[],
}>();

async function getPlaylistSongs(): Promise<({uuid: string} & Song)[]> {
  const searchSongs = await algoliaIndex.getObjects<Song>(props.songs);
  return searchSongs.results
    .filter((song): song is Song & ObjectWithObjectID => song !== null)
    .map(({objectID, ...song}) => ({uuid: objectID, ...song}));
}

const playPlayList = async () => {
  const playlistSongs = await getPlaylistSongs();
  store.setPlayList(playlistSongs);
  store.playNextPlayListSong();
};
const playPlayListRandom = async () => {
  const playlistSongs = await getPlaylistSongs();
  let randomPlaylist = playlistSongs;
  randomPlaylist.sort(() => 0.5 - Math.random());
  store.setPlayList(randomPlaylist);
  store.playNextPlayListSong();
};

const showPlaylistForm = ref(false);

const showBottomMenu = ref(false);
const tiles = ref([
  ...(props.playlistId !== "favorite" && props.playlistId !== "recommended") ?
    [
      {
        icon: "mdi-pencil",
        color: "black",
        title: "タイトル/概要/公開・非公開を編集",
        click: () => {showPlaylistForm.value = true;},
        requireLogin: true
      },
      {
        icon: "mdi-delete",
        color: "red",
        title: "プレイリストを削除",
        click: () => {removePlayList(props.playlistId!, props.visibility)},
        requireLogin: true
      },
    ]
    : [],
  {icon: "mdi-share-variant", color: "blue-lighten-4", title: "共有", click: () => {console.log("TODO")}, requireLogin: false},
]);

const showPlaylistBottom = ref(false);

const img = new URL(`../assets/image/smile.png`, import.meta.url).href;
</script>

<template>
  <v-card class="mx-auto" @click.stop="showPlaylistBottom = true" link>
    <v-img :src="img" height="200px" cover />

    <v-card-title>
      {{ playlistTitle }}
    </v-card-title>

    <v-card-subtitle>
      {{ playlistDescription }}
      <div>{{ props.songs.length }}曲</div>
    </v-card-subtitle>

    <v-card-actions>
      <v-col>
        <v-btn :icon="true" elevation="1" @click.stop>
          <v-icon icon="mdi-play" @click.prevent="playPlayList" />
        </v-btn>
        <v-btn :icon="true" elevation="1" @click.stop>
          <v-icon icon="mdi-shuffle" @click.prevent="playPlayListRandom" />
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn :icon="true" elevation="1" @click.stop>
          <v-icon icon="mdi-dots-vertical" @click.prevent="showBottomMenu = true;" />
        </v-btn>
      </v-col>
    </v-card-actions>
  </v-card>

  <BottomListMenu v-model="showBottomMenu" :tiles="tiles" />
  <template v-if="playlistId !== undefined">
    <PlaylistForm v-model="showPlaylistForm" :playlist-id="playlistId" :title="playlistTitle"
      :description="playlistDescription" :is-public="visibility" :songs="songs" />
  </template>
  <template v-if="showPlaylistBottom">
    <PlaylistDetailSheet v-model="showPlaylistBottom" :playlist-id="playlistId" :title="playlistTitle"
      :description="playlistDescription" :visibility="visibility" :songs="songs" />
  </template>
</template>
