<script lang="ts" setup>
import {addToFavorite, favoriteSongs, removeFromFavorite, songs} from '@/common';
import {useAppStore} from '@/store/app';
import {ref, Ref} from 'vue';
import YouTube from 'vue3-youtube';
import PlayerStates from "youtube-player/dist/constants/PlayerStates";
import {YouTubePlayer} from 'youtube-player/dist/types';
const store = useAppStore();

const progress: Ref<number | null> = ref(null)
// const isSliderFocused = ref(false);
// const computedProgress = computed({
//   get: () => progress.value ?? undefined,
//   set: (newValue) => {
//     console.debug(newValue);
//     progress.value = 0;
//   }
// });

const secondsFromStart: Ref<number> = ref(0);
const secondsToEnd: Ref<number | null> = ref(null);

let timerId: NodeJS.Timeout | null = null;

const youtube: Ref<YouTubePlayer | null> = ref(null);
const playing = ref(false);

const onReady = () => {
  if (timerId !== null) {
    clearInterval(timerId)
  }
  youtube.value?.playVideo();

  timerId = setInterval(async () => {
    if (store.indexPlayList === null) {
      progress.value = 0;
    } else {
      const t = songs[store.playingPlayList[store.indexPlayList]].t;
      const endt = songs[store.playingPlayList[store.indexPlayList]].endt;

      const currentTime = await youtube?.value?.getCurrentTime();
      if (currentTime !== undefined) {
        secondsFromStart.value = currentTime - t;
        secondsToEnd.value = endt !== null ? (endt - currentTime) : null;
      }

      if (endt === null) {
        progress.value = 0;
      } else {
        progress.value = 100 * secondsFromStart.value / (endt - t);
      }
    }
  }, 500);
};

const displayTime = (seconds: number | null) => {
  if (seconds === null) {
    return "--:--";
  }
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  const formattedHours = String(hours).padStart(2, '0');
  const formattedMinutes = String(minutes).padStart(2, '0');
  const formattedSeconds = String(remainingSeconds).padStart(2, '0');

  if (hours === 0) {
    return `${formattedMinutes}:${formattedSeconds}`;
  } else {
    return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
  }
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
          <!-- player -->
          <v-col cols="12" sm="auto" md="auto" lg="auto" xl="auto" class="text-center">
            <YouTube :src="songs[store.playingPlayList[store.indexPlayList]].video"
              :vars="{start: songs[store.playingPlayList[store.indexPlayList]].t, end: songs[store.playingPlayList[store.indexPlayList]].endt ?? undefined, controls: 0, modestbranding: 1}"
              @ready="onReady" height="20%" width="auto" @state-change="onStateChange"
              :key="store.playingPlayList[store.indexPlayList]" ref="youtube" />

          </v-col>
          <!-- controller -->
          <v-col class="text-center">
            <v-row class="text-center">
              <v-col>
                <v-list-item-title>{{ songs[store.playingPlayList[store.indexPlayList]].name }}</v-list-item-title>
                <v-list-item-subtitle>{{ songs[store.playingPlayList[store.indexPlayList]].artist
                }}</v-list-item-subtitle>

              </v-col>
            </v-row>
            <!-- <v-row rows="auto" class="ma-0 pa-0"> -->
            <!--   <v-slider -->
            <!--     thumb-size="10" -->
            <!--     class="ma-0 pa-0" -->
            <!--     @start="isSliderFocused = true;" -->
            <!--     @end="isSliderFocused = false;" -->
            <!--     :model-value="progress ?? undefined" -->
            <!--     @update:model-value="() => {console.log('FFFFFFFFFFFF')}" /> -->
            <!-- </v-row> -->
            <v-row>
              <v-progress-linear :model-value="progress ?? undefined" />
              <v-col cols="auto" class="pa-0 text-caption">{{ displayTime(secondsFromStart) }}</v-col>
              <v-col />
              <v-col cols="auto" class="pa-0 text-caption">{{ displayTime(secondsToEnd) }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="auto">
                <template v-if="favoriteSongs?.has(store.playingPlayList[store.indexPlayList])">
                  <v-btn icon="mdi-heart" variant="text"
                    @click="removeFromFavorite(store.playingPlayList[store.indexPlayList])" />
                </template>
                <template v-else>
                  <v-btn icon="mdi-heart-outline" variant="text"
                    @click="addToFavorite(store.playingPlayList[store.indexPlayList])" />
                </template>
              </v-col>
              <v-col class="text-center">
                <v-btn icon="mdi-rewind" variant="text" @click="store.playPreviousPlayListSong()" />
                <template v-if="playing">
                  <v-btn icon="mdi-pause" variant="text" @click="youtube?.pauseVideo()" />
                </template>
                <template v-else>
                  <v-btn icon="mdi-play" variant="text" @click="youtube?.playVideo()" />
                </template>
                <v-btn icon="mdi-fast-forward" variant="text" @click="store.playNextPlayListSong()" />
              </v-col>
              <v-col cols="auto">
                <v-btn icon="mdi-close" variant="text" @click="onClose" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </template>
</template>
