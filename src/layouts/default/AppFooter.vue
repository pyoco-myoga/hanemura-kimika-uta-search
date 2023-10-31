<script lang="ts" setup>
import {songs} from '@/common';
import {useAppStore} from '@/store/app';
import {ref, Ref} from 'vue';
import YouTube from 'vue3-youtube';
import PlayerStates from "youtube-player/dist/constants/PlayerStates";
const store = useAppStore();

const progress: Ref<number | null> = ref(null)
let timerId: NodeJS.Timeout | null = null;

const playing = ref(false);
const play = ref(() => {});
const pause = ref(() => {});

const onReady = (e: any) => {
  if (timerId !== null) {
    clearInterval(timerId)
  }
  e.target.playVideo();
  play.value = () => e.target.playVideo();
  pause.value = () => e.target.pauseVideo();

  console.log(e.target);

  timerId = setInterval(() => {
    if (store.indexPlayList === null) {
      progress.value = 0;
    } else {
      const t = songs[store.playingPlayList[store.indexPlayList]].t;
      const endt = songs[store.playingPlayList[store.indexPlayList]].endt;
      if (endt === null) {
        progress.value = 0;
      } else {
        progress.value = 100 * (e.target.getCurrentTime() - t) / (endt - t);
      }
    }
  }, 500);
};

const onStateChange = (e: any) => {
  if (e.data === PlayerStates.PLAYING) {
    playing.value = true;
  }
  if (e.data === PlayerStates.PAUSED) {
    playing.value = false;
  }
  if (e.data === PlayerStates.ENDED) {
    store.playNextPlayListSong();
    playing.value = false;
  }
};

const onClose = () => {
  store.setPlayList([]);
  if (timerId !== null) {
    clearInterval(timerId);
  }
}

</script>

<template>
  <template v-if="store.indexPlayList !== null">
    <v-footer app class="elevation-10">
      <v-container class="my-1">
        <v-row>
          <v-col cols="auto" class="text-center">
            <you-tube :src="songs[store.playingPlayList[store.indexPlayList]].video"
              :vars="{start: songs[store.playingPlayList[store.indexPlayList]].t, end: songs[store.playingPlayList[store.indexPlayList]].endt ?? undefined, controls: 0, modestbranding: 1}"
              @ready="onReady" height="20%" width="auto" @state-change="onStateChange"
              :key="store.playingPlayList[store.indexPlayList]" />

          </v-col>
          <v-col class="text-center">
            <v-row class="text-center">
              <v-col>
                <v-list-item-title>{{ songs[store.playingPlayList[store.indexPlayList]].name }}</v-list-item-title>
                <v-list-item-subtitle>{{ songs[store.playingPlayList[store.indexPlayList]].artist
                }}</v-list-item-subtitle>

              </v-col>
            </v-row>
            <v-row>
              <v-progress-linear :model-value="progress ?? undefined" />
            </v-row>
            <v-row>
              <v-col class="text-center">
                <v-btn icon="mdi-rewind" variant="text" @click="store.playPreviousPlayListSong()" />
                <template v-if="playing">
                  <v-btn icon="mdi-pause" variant="text" @click="pause" />
                </template>
                <template v-else>
                  <v-btn icon="mdi-play" variant="text" @click="play" />
                </template>

                <v-btn class="ms-0" icon="mdi-fast-forward" variant="text" @click="store.playNextPlayListSong()" />
              </v-col>
              <v-col cols="1">
                <v-btn icon="mdi-close" variant="text" @click="onClose" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </template>
</template>