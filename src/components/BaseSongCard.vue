<script lang="ts" setup>
import type {Song} from "@/@types/global/song.d.ts";
import {useAppStore} from "@/store/app";

const store = useAppStore();

const props = defineProps<Song & {
  isFavorite: boolean | null;
  isFull: boolean | null;
  playlist: string[],
  playlistIndex: number
}>();

const resetNextSongsAndSetNext = (playlist: string[], index: number) => {
  store.setPlayList(playlist);
  store.setPlayListIndex(index);
}

const showBottomMenu = defineModel<boolean>();
</script>

<template>
  <v-card class="mx-auto" elevation="2">
    <v-row>
      <slot name="pre-icon" />
      <v-col>
        <v-card-title>{{ props.name }}</v-card-title>
        <v-card-subtitle>{{ props.artist }}</v-card-subtitle>
      </v-col>
      <v-col cols="auto">
        <v-card-text>
          <div>
            <v-btn class="mx-1" :icon="true" @click="resetNextSongsAndSetNext(props.playlist, props.playlistIndex)">
              <v-icon icon="mdi-play" />
            </v-btn>
            <v-btn class="mx-1" :icon="true" @click="showBottomMenu = !showBottomMenu">
              <v-icon icon="mdi-dots-vertical" />
            </v-btn>
          </div>
        </v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>
