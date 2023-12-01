<script lang="ts" setup>
import PlaylistCard from "./PlaylistCard.vue";
import * as database from "firebase/database";
import {Playlist} from "@/common";
import {Ref, onBeforeUnmount, ref} from "vue";

const props = defineProps<{
  playlistId: string;
  uid: string;
  visibility: "public" | "private";
}>();
const db = database.getDatabase();

const playlist: Ref<Playlist | null> = ref(null);

const playlistUnsubscribe = database.onValue(
  database.ref(db, `users/${props.uid}/playlists/${props.playlistId}`),
  snapshot => {
    let data: any = snapshot.val();
    if (data !== undefined && data !== null &&
      data.title !== undefined && typeof data.title === "string" &&
      data.description !== undefined && typeof data.description === "string" &&
      data.image !== undefined && typeof data.image === "string") {
      if (data.songs === undefined) {
        data.songs = [];
      }
      if (Array.isArray(data.songs) && data.songs.every((v: unknown) => typeof v === "string")) {
        playlist.value = data;
      }
    }
  },
  e => console.log(e));

onBeforeUnmount(() => {
  playlistUnsubscribe();
});
</script>

<template>
  <template v-if="playlist !== null">
    <PlaylistCard :playlist-title="playlist.title" :playlist-description="playlist.description" :songs="playlist.songs"
      :playlist-image="playlist.image" :playlist-id="playlistId" :visibility="visibility" />
  </template>
</template>
