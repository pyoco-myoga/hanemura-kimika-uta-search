<script lang="ts" setup>
import * as database from "firebase/database";
import type {Song} from "@/@types/global/song.d.ts";
import PlaylistSongCard from "./PlaylistSongCard.vue";
import BottomListMenu from "./BottomListMenu.vue";
import PlaylistForm from "./PlaylistForm.vue";
import {favoriteSongs, uidRef} from "@/common";
import {useAppStore} from "@/store/app";
import {ref} from "vue";
const store = useAppStore();
const props = defineProps<{
  playlistId?: string;
  playlistTitle: string;
  playlistDescription: string;
  visibility: "public" | "private",
  songs: (Song & {uuid: string})[],
}>();

const playPlayList = () => {
  const playListSongsUUID = props.songs.map(song => song.uuid);
  store.setPlayList(playListSongsUUID);
  store.playNextPlayListSong();
};
const onAddFavorite = (songUUID: string) => {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (favoriteSongs.value.has(songUUID)) {
    return;
  }
  const db = database.getDatabase();
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...favoriteSongs.value, songUUID]
  );
};
const onRemoveFavorite = (songUUID: string) => {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (!favoriteSongs.value.has(songUUID)) {
    return;
  }
  const db = database.getDatabase();
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...(favoriteSongs.value || [])].filter(v => v !== songUUID)
  );
};

const showPlaylistForm = ref(false);

const showBottomMenu = ref(false);
const tiles = ref([
  ...(props.playlistId !== undefined) ?
    [
      {icon: "mdi-pencil", color: "black", title: "タイトル/概要/公開・非公開を編集", click: () => {showPlaylistForm.value = true;}, requireLogin: true},
      {icon: "mdi-delete", color: "red", title: "プレイリストを削除", click: () => {}, requireLogin: true},
    ]
    : [],
  {icon: "mdi-share-variant", color: "blue-lighten-4", title: "共有", click: () => {}, requireLogin: false},
]);
</script>

<template>
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-row no-gutters>
          <v-col cols="auto">
            <v-btn class="mx-1" :icon="true" @click="playPlayList" @click.stop>
              <v-icon icon="mdi-play" />
            </v-btn>
          </v-col>
          <v-col cols="2" class="d-flex align-center text-center">
            <v-card-title>
              {{ props.playlistTitle }}
            </v-card-title>
          </v-col>
          <v-col class="d-flex align-center text-center">
            <div class="d-none d-sm-block">
              <v-card-subtitle>
                {{ props.songs.length }}曲
              </v-card-subtitle>
            </div>
          </v-col>
          <v-col cols="6" class="d-flex align-center text-center">
            <div class="d-none d-sm-block">
              <v-card-subtitle>
                {{ playlistDescription }}
              </v-card-subtitle>
            </div>
          </v-col>
          <v-col cols="auto">
            <v-btn class="mx-1" :icon="true" elevation="0" @click.stop>
              <v-icon icon="mdi-dots-vertical" @click="showBottomMenu = true;" />
            </v-btn>
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <template v-for="({uuid, ...song}, index) in songs" :key="song.uuid">
          <PlaylistSongCard v-bind="{
            ...song,
            isFavorite: favoriteSongs?.has(uuid) ?? null,
            isFull: song.length === 'full',
            playlist: props.songs.map(song => song.uuid),
            playlistIndex: index,
            visibility,
            playlistId
          }" @add-favorite="onAddFavorite" @remove-favorite="onRemoveFavorite" />
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
  <BottomListMenu v-model="showBottomMenu" :tiles="tiles" />
  <template v-if="playlistId !== undefined">
    <PlaylistForm v-model="showPlaylistForm" :playlist-id="playlistId" :title="playlistTitle"
      :description="playlistDescription" :is-public="visibility" :songs="songs.map(song => song.uuid)" />
  </template>
</template>
