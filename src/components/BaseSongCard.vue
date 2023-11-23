<script lang="ts" setup>
import type {Song} from "@/@types/global/song.d.ts";
import {useAppStore} from "@/store/app";

const store = useAppStore();

const props = defineProps<Song & {
  isFavorite: boolean | null;
  isFull: boolean | null;
  playlist: ({uuid: string} & Song)[],
  playlistIndex: number
}>();

const resetNextSongsAndSetNext = () => {
  store.setPlayList(props.playlist);
  store.setPlayListIndex(props.playlistIndex);
}

const showBottomMenu = defineModel<boolean>();

const img = new URL(`../assets/thumbnail/${props.video}/0.jpg`, import.meta.url).href;
</script>

<style scoped>
.custom-title-style {
  text-overflow: ellipsis;
}
</style>

<template>
  <v-card class="mx-auto" elevation="2" @click="resetNextSongsAndSetNext()">
    <v-sheet height="80" class="d-flex">
      <div class="d-flex me-3">
        <v-btn height="100%" @click.stop="resetNextSongsAndSetNext()" :style="{
          backgroundImage: `url(${img})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }" elevation="0">
          <v-icon size="x-large" icon="mdi-play" />
        </v-btn>
      </div>
      <div class="d-flex flex-column flex-grow-1 overflow-hidden justify-center">
        <v-list-item-title class="overflow-hidden custom-title-style">
          {{ props.name }}
          <template v-if="props.endt === null">
            <v-icon icon="mdi-close" />
          </template>
        </v-list-item-title>
        <v-list-item-subtitle class="overflow-hidden" style="white-space: nowrap;">
          {{ props.artist }}
        </v-list-item-subtitle>
      </div>
      <div class="d-flex">
        <slot name="post-icon" />
        <v-btn icon="mdi-dots-vertical" @click.stop="showBottomMenu = !showBottomMenu" :elevation="0" />
      </div>
    </v-sheet>
  </v-card>
</template>
