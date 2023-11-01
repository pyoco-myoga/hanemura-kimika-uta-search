<script lang="ts" setup>
import type {Song} from "@/@types/global/song.d.ts";
import SongCard from "./SongCard.vue";
import PlaylistSongCard from "./PlaylistSongCard.vue";
import {favoriteSongs} from "@/common";
import {useAppStore} from "@/store/app";
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
}
</script>

<template>
  <v-expansion-panels>
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-row no-gutters>
          <v-col cols="1">
            <v-btn class="mx-1" :icon="true" @click="playPlayList" @click.stop>
              <v-icon icon="mdi-play" />
            </v-btn>
          </v-col>
          <v-col cols="3" class="d-flex align-center text-center">
            <v-card-title>
              {{ props.playlistTitle }}
            </v-card-title>
          </v-col>
          <v-col cols="1" class="d-flex align-center text-center">
            <v-card-subtitle>
              {{ props.songs.length }}曲
            </v-card-subtitle>
          </v-col>
          <v-col cols="7" class="d-flex align-center text-center">
            <v-card-subtitle>
              {{ playlistDescription }}
            </v-card-subtitle>
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
          }" />
        </template>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>
