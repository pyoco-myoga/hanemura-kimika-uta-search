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

const img = new URL(`../assets/thumbnail/${props.video}/0.jpg`, import.meta.url).href;
</script>

<template>
  <v-card class="mx-auto" elevation="2">
    <v-row>
      <v-col cols="2" class="d-flex align-center">
        <v-btn width="100%" height="100%" @click="resetNextSongsAndSetNext(props.playlist, props.playlistIndex)" :style="{
          backgroundImage: `url(${img})`,
          backgroundSize: '100% auto',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }" elevation="0">
          <v-icon size="x-large" icon="mdi-play" />
        </v-btn>
      </v-col>
      <v-col>
        <v-card-title>{{ props.name }}</v-card-title>
        <v-card-subtitle>{{ props.artist }}</v-card-subtitle>
        <template v-if="props.endt === null">
          <v-icon icon="mdi-close" />
        </template>
      </v-col>
      <v-col cols="auto">
        <v-card-text>
          <div>
            <slot name="post-icon" />
            <v-btn class="mx-1" icon="mdi-dots-vertical" @click="showBottomMenu = !showBottomMenu" :elevation="0" />
          </div>
        </v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>
