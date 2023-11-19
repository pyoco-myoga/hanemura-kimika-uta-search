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

<template>
  <v-card class="mx-auto" elevation="2" @click="resetNextSongsAndSetNext()">
    <v-row>
      <v-col cols="auto">
        <v-btn height="100%" @click.stop="resetNextSongsAndSetNext()" :style="{
          backgroundImage: `url(${img})`,
          backgroundSize: 'cover',
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
            <v-btn icon="mdi-dots-vertical" @click.stop="showBottomMenu = !showBottomMenu" :elevation="0" />
          </div>
        </v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>
