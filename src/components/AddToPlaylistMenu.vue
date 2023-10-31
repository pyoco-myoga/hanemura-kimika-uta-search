<script lang="ts" setup>
import {privatePlaylists, uidRef} from '@/common';
import * as database from "firebase/database";
import {Ref} from 'vue';
import {ref} from 'vue';

const show = defineModel<boolean>();
const props = defineProps<{songId: string}>();

const selected: Ref<string[]> = ref([]);
const db = database.getDatabase();

const addToPlaylist = () => {
  for (const playlistId of selected.value) {
    database.set(
      database.ref(db, `users/${uidRef.value}/playlists/${playlistId}/songs`),
      [...privatePlaylists.value![playlistId].songs ?? [], props.songId]);
  }
};
</script>


<template>
  <v-bottom-sheet v-model="show">
    <v-list>
      <v-list-item v-for="({title}, playlistId) in privatePlaylists" :key="playlistId" density="compact">
        <v-checkbox v-model="selected" :value="playlistId" :label="title" />
      </v-list-item>
      <v-list-item @click="() => {addToPlaylist(); show = false;}">
        <span>追加</span>
      </v-list-item>
    </v-list>
  </v-bottom-sheet>
</template>

