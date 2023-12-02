<script lang="ts" setup>
import type {Song} from "@/common";
import {useAppStore} from "@/store/app";
import {computed} from "vue";

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

const isPlaying = computed(() => {
  if (store.indexPlayList === null) {
    return false;
  }
  if (store.indexPlayList !== null && store.playingPlayList[store.indexPlayList] === props.playlist[props.playlistIndex]) {
    return true;
  } else {
    return false;
  }
})

const color = computed(() => {
  const playingColor = "grey-lighten-2";
  const notPlayingColor = "white";
  return isPlaying.value ? playingColor : notPlayingColor;
});
</script>

<style scoped>
.custom-title-style {
  text-overflow: ellipsis;
}
</style>

<template>
  <v-card class="mx-auto" elevation="2" @click="resetNextSongsAndSetNext()">
    <v-sheet height="80" class="d-flex" :color="color">
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
        </v-list-item-title>
        <v-list-item-subtitle class="overflow-hidden" style="white-space: nowrap;">
          {{ props.artist }}
        </v-list-item-subtitle>
      </div>
      <div class="d-flex align-center">
        <slot name="post-icon" />
        <v-btn icon="mdi-dots-vertical" @click.stop="showBottomMenu = !showBottomMenu" :elevation="0" />
      </div>
    </v-sheet>
  </v-card>
</template>
