<script lang="ts" setup>
import {ref} from "vue";
import * as database from "firebase/database";
import BottomListMenu from "@/components/BottomListMenu.vue";
import AddToPlaylistMenu from "@/components/AddToPlaylistMenu.vue";
import BaseSongCard from "./BaseSongCard.vue";
import {uidRef, Song} from "@/common";

const props = defineProps<Song & {
  isFavorite: boolean | null;
  isFull: boolean | null;
  visibility: "public" | "private",
  playlistId?: string,
  playlist: ({uuid: string} & Song)[],
  playlistIndex: number
}>();
const emits = defineEmits<{
  addFavorite: [songUUID: string],
  removeFavorite: [songUUID: string],
}>();

const youtubeURL = `https://www.youtube.com/watch?v=${props.video}&t=${props.t}`;

const showCopiedPopup = ref(false);
const shareButtonEvent = async () => {
  try {
    await navigator.clipboard.writeText(`${props.name} / ${props.artist}: ${youtubeURL}`);
    showCopiedPopup.value = true;
  } catch (e) {
    console.error(e);
  }
};

const youtubeThumbnailURL = `https://img.youtube.com/vi/${props.video}/0.jpg`;

const showBottomMenu = ref(false);
const showAddToPlaylistMenu = ref(false);

const db = database.getDatabase();
const removeFromPlaylist = () => {
  if (props.playlistId !== undefined) {
    database.set(
      database.ref(db, `users/${uidRef.value}/playlists/${props.playlistId}/songs`),
      [
        ...props.playlist.slice(0, props.playlistIndex).map(song => song.uuid),
        ...props.playlist.slice(props.playlistIndex + 1).map(song => song.uuid),
      ]);
  }
};
const tiles = ref([
  {icon: "mdi-youtube", color: "red", title: "YouTubeへ移動", click: () => {window.open(youtubeURL);}, requireLogin: false},
  {icon: "mdi-share-variant", color: "blue-lighten-4", title: "共有", click: shareButtonEvent, requireLogin: false},
  {icon: "mdi-image-area", color: "blue-grey", title: "サムネ画像を取得", click: () => {window.open(youtubeThumbnailURL);}, requireLogin: false},
]);
if (props.visibility === "private") {
  tiles.value.push(
    {icon: "mdi-playlist-music", color: "black", title: "プレイリストから削除", click: removeFromPlaylist, requireLogin: true});
}
</script>

<template>
  <BaseSongCard v-bind="{...props}" v-model="showBottomMenu">
    <template v-slot:post-icon>
      <template v-if="isFavorite !== null">
        <template v-if="isFavorite">
          <v-btn icon="mdi-heart" @click="emits('removeFavorite', playlist[playlistIndex].uuid)" :elevation="0" />
        </template>
        <template v-else>
          <v-btn icon="mdi-heart-outline" @click="emits('addFavorite', playlist[playlistIndex].uuid)" :elevation="0" />
        </template>
      </template>
    </template>
  </BaseSongCard>

  <v-snackbar v-model="showCopiedPopup" :timeout="1000">
    <div>
      クリップボードにコピーしました
    </div>
    <div>
      {{ name }} / {{ artist }}
    </div>
  </v-snackbar>

  <BottomListMenu :tiles="tiles" v-model="showBottomMenu" />
  <template v-if="uidRef !== null">
    <AddToPlaylistMenu v-model="showAddToPlaylistMenu" :song-id="playlist[playlistIndex].uuid" />
  </template>
</template>
