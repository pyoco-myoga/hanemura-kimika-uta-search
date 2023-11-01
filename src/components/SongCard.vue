<script lang="ts" setup>
import {ref} from 'vue';
import * as database from "firebase/database";
import type {Song} from "@/@types/global/song.d.ts";
import SongBottomMenu from "@/components/SongBottomMenu.vue";
import BaseSongCard from './BaseSongCard.vue';
import {privatePlaylists, uidRef} from '@/common';
import {Ref} from 'vue';

const props = defineProps<Song & {
  isFavorite: boolean | null;
  isFull: boolean | null;
  playlist: string[],
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
const tiles = ref([
  {icon: "mdi-youtube", color: "red", title: "YouTubeへ移動", click: () => window.open(youtubeURL), requireLogin: false},
  {icon: "mdi-share-variant", color: "blue-lighten-4", title: "共有", click: shareButtonEvent, requireLogin: false},
  {icon: "mdi-image-area", color: "blue-grey", title: "サムネ画像を取得", click: () => window.open(youtubeThumbnailURL), requireLogin: false},
  {icon: "mdi-playlist-music", color: "black", title: "プレイリストに追加", click: () => {showAddToPlaylistMenu.value = true;}, requireLogin: true},
]);


const showAddToPlaylistMenu = ref(false);
const selected: Ref<string[]> = ref([]);
const db = database.getDatabase();
const addToPlaylist = () => {
  for (const playlistId of selected.value) {
    database.set(
      database.ref(db, `users/${uidRef.value}/playlists/${playlistId}/songs`),
      [
        ...privatePlaylists.value![playlistId].songs ?? [],
        props.playlist[props.playlistIndex]
      ]);
  }
};
</script>

<template>
  <BaseSongCard v-bind="{...props}" v-model="showBottomMenu">
    <template v-slot:pre-icon>
      <template v-if="isFavorite !== null">
        <v-col cols="auto" class="mx-5 d-flex align-center">
          <!-- favorite buttom -->
          <template v-if="isFavorite">
            <v-icon icon="mdi-heart" @click="emits('removeFavorite', playlist[playlistIndex])" />
          </template>
          <template v-else>
            <v-icon icon="mdi-heart-outline" @click="emits('addFavorite', playlist[playlistIndex])" />
          </template>
        </v-col>
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

  <SongBottomMenu :tiles="tiles" v-model="showBottomMenu" />
  <template v-if="uidRef !== null">
    <v-bottom-sheet v-model="showAddToPlaylistMenu">
      <v-list>
        <v-list-item v-for="({title}, playlistId) in privatePlaylists" :key="playlistId" density="compact">
          <v-checkbox v-model="selected" :value="playlistId" :label="title" />
        </v-list-item>
        <v-list-item @click="() => {addToPlaylist(); showAddToPlaylistMenu = false;}">
          <span>追加</span>
        </v-list-item>
      </v-list>
    </v-bottom-sheet>
  </template>
</template>
