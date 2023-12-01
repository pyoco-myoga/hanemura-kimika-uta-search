<script lang="ts" setup>
import {ref, Ref} from "vue";
import * as database from "firebase/database";
import BottomListMenu from "@/components/BottomListMenu.vue";
import BaseSongCard from "./BaseSongCard.vue";
import ShareYoutube from "./ShareYoutube.vue";
import {privatePlaylists, uidRef, getYoutubeURL, Song} from "@/common";

const props = defineProps<Song & {
  uuid: string,
  isFavorite: boolean | null;
  isFull: boolean | null;
}>();
const emits = defineEmits<{
  addFavorite: [songUUID: string],
  removeFavorite: [songUUID: string],
}>();

const youtubeURL = getYoutubeURL(props.video, props.t);

const fireShareEvent = ref(false);

const youtubeThumbnailURL = `https://img.youtube.com/vi/${props.video}/0.jpg`;

const showBottomMenu = ref(false);
const tiles = ref([
  {icon: "mdi-youtube", color: "red", title: "YouTubeへ移動", click: () => window.open(youtubeURL), requireLogin: false},
  {icon: "mdi-share-variant", color: "blue-lighten-4", title: "共有", click: () => {fireShareEvent.value = true;}, requireLogin: false},
  {icon: "mdi-image-area", color: "blue-grey", title: "サムネ画像を取得", click: () => window.open(youtubeThumbnailURL), requireLogin: false},
  (props.endt === null) ?
    {icon: "mdi-playlist-music", color: "black", title: "情報不足によりプレイリストに追加できません", click: () => {}, requireLogin: true} :
    {icon: "mdi-playlist-music", color: "black", title: "プレイリストに追加", click: () => {showAddToPlaylistMenu.value = true;}, requireLogin: true},
]);


const showAddToPlaylistMenu = ref(false);
const selectedPlaylist: Ref<string[]> = ref([]);
const db = database.getDatabase();
const addToPlaylist = () => {
  for (const playlistId of selectedPlaylist.value) {
    database.set(
      database.ref(db, `users/${uidRef.value}/playlists/${playlistId}/songs`),
      [
        ...privatePlaylists.value![playlistId].songs ?? [],
        props.uuid
      ]);
  }
};
</script>

<template>
  <BaseSongCard v-bind="{
    playlist: [props],
    playlistIndex: 0,
    ...props
  }" v-model="showBottomMenu">
    <template v-slot:post-icon>
      <template v-if="isFavorite !== null">
        <!-- favorite buttom -->
        <template v-if="isFavorite">
          <v-btn icon="mdi-heart" @click.stop="emits('removeFavorite', uuid)" :elevation="0" />
        </template>
        <template v-else>
          <v-btn icon="mdi-heart-outline" @click.stop="emits('addFavorite', uuid)" :elevation="0" />
        </template>
      </template>
    </template>
  </BaseSongCard>

  <ShareYoutube v-model="fireShareEvent" :name="props.name" :artist="props.artist" :video="props.video" :t="props.t" />

  <BottomListMenu :tiles="tiles" v-model="showBottomMenu" />
  <template v-if="uidRef !== null">
    <v-bottom-sheet v-model="showAddToPlaylistMenu">
      <v-list>
        <v-list-item v-for="({title}, playlistId) in privatePlaylists" :key="playlistId" density="compact">
          <v-checkbox v-model="selectedPlaylist" :value="playlistId" :label="title" />
        </v-list-item>
        <v-list-item @click="() => {addToPlaylist(); showAddToPlaylistMenu = false;}">
          <span>追加</span>
        </v-list-item>
      </v-list>
    </v-bottom-sheet>
  </template>
</template>
