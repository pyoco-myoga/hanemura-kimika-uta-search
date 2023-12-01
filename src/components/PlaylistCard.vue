<script lang="ts" setup>
import {removePlayList, playPlaylist, playPlaylistRandom} from "@/common";
import BottomListMenu from "./BottomListMenu.vue";
import PlaylistForm from "./PlaylistForm.vue";
import {ref} from "vue";
import PlaylistDetailSheet from "./PlaylistDetailSheet.vue";
const props = defineProps<{
  playlistId: string | "favorite" | "recommended";
  playlistTitle: string;
  playlistDescription: string;
  playlistImage: string,
  visibility: "public" | "private",
  songs: string[],
}>();

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

const image = new URL(props.playlistImage, window.location.toString()).href;
console.debug(image);
</script>

<template>
  <v-card class="mx-auto" @click.stop="showPlaylistBottom = true" link>
    <v-img :src="image" :height="200" cover />

    <v-card-title class="overflow-hidden" style="min-height: 50px;">
      {{ playlistTitle }}
    </v-card-title>
    <v-card-subtitle>
      <div class="overflow-hidden" style="min-height: 30px;">{{ playlistDescription }}</div>
      <div>{{ props.songs.length }}曲</div>
    </v-card-subtitle>

    <v-card-actions>
      <v-col>
        <v-btn icon="mdi-play" @click.prevent="playPlaylist(songs)" elevation="1" @click.stop />
        <v-btn icon="mdi-shuffle" @click.prevent="playPlaylistRandom(songs)" elevation="1" @click.stop />
      </v-col>
      <v-col cols="auto">
        <v-btn icon="mdi-dots-vertical" @click.prevent="showBottomMenu = true" elevation="1" @click.stop />
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
