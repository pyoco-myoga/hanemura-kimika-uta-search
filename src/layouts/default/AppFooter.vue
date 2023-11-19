<script lang="ts" setup>
import {addToFavorite, favoriteSongs, removeFromFavorite, uidRef, getYoutubeURL} from "@/common";
import {useAppStore} from "@/store/app";
import {ref, Ref} from "vue";
import YouTube from "vue3-youtube";
import PlayerStates from "youtube-player/dist/constants/PlayerStates";
import {YouTubePlayer} from "youtube-player/dist/types";
import ShareYoutube from "@/components/ShareYoutube.vue";
import {computed} from "vue";
const store = useAppStore();

const progress: Ref<number | null> = ref(null)

const secondsFromStart: Ref<number> = ref(0);
const secondsToEnd: Ref<number | null> = ref(null);

let timerId: NodeJS.Timeout | null = null;

const youtube: Ref<YouTubePlayer | null> = ref(null);
const playing = ref(false);

const fireShareEvent = ref(false);

const onReady = () => {
  if (timerId !== null) {
    clearInterval(timerId)
  }
  youtube.value?.playVideo();

  timerId = setInterval(async () => {
    if (store.indexPlayList === null) {
      progress.value = 0;
    } else {
      const t = store.playingPlayList[store.indexPlayList].t;
      const endt = store.playingPlayList[store.indexPlayList].endt;

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

const youtubeURL = computed(() => {
  if (store.indexPlayList !== null) {
    return getYoutubeURL(
      store.playingPlayList[store.indexPlayList].video,
      store.playingPlayList[store.indexPlayList].t)
  } else {
    return null;
  }
});

const gotoYoutube = () => {
  if (youtubeURL.value !== null) {
    window.open(youtubeURL.value);
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
            <YouTube :src="store.playingPlayList[store.indexPlayList].video"
              :vars="{start: store.playingPlayList[store.indexPlayList].t, end: store.playingPlayList[store.indexPlayList].endt ?? undefined, controls: 0, modestbranding: 1}"
              @ready="onReady" height="20%" width="auto" @state-change="onStateChange"
              :key="store.playingPlayList[store.indexPlayList].uuid" ref="youtube" />

          </v-col>
          <!-- controller -->
          <v-col class="text-center">
            <v-row class="text-center">
              <v-col cols="auto">
                <v-btn icon="mdi-share-variant" variant="text" @click="fireShareEvent = true;" />
              </v-col>
              <v-col>
                <v-list-item-title>{{ store.playingPlayList[store.indexPlayList].name }}</v-list-item-title>
                <v-list-item-subtitle>{{ store.playingPlayList[store.indexPlayList].artist }}</v-list-item-subtitle>
              </v-col>
              <v-col cols="auto">
                <v-btn icon="mdi-youtube" variant="text" @click="gotoYoutube" />
              </v-col>
            </v-row>
            <v-row>
              <v-progress-linear :model-value="progress ?? undefined" />
              <v-col cols="auto" class="pa-0 text-caption">{{ displayTime(secondsFromStart) }}</v-col>
              <v-col />
              <v-col cols="auto" class="pa-0 text-caption">{{ displayTime(secondsToEnd) }}</v-col>
            </v-row>
            <v-row>
              <v-col cols="auto">
                <template v-if="uidRef === null">
                  <v-btn :icon="true" variant="text" />
                </template>
                <template v-else-if="favoriteSongs?.has(store.playingPlayList[store.indexPlayList].uuid)">
                  <v-btn icon="mdi-heart" variant="text"
                    @click="removeFromFavorite(store.playingPlayList[store.indexPlayList].uuid)" />
                </template>
                <template v-else>
                  <v-btn icon="mdi-heart-outline" variant="text"
                    @click="addToFavorite(store.playingPlayList[store.indexPlayList].uuid)" />
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
    <ShareYoutube v-model="fireShareEvent" :name="store.playingPlayList[store.indexPlayList].name"
      :artist="store.playingPlayList[store.indexPlayList].artist"
      :video="store.playingPlayList[store.indexPlayList].video" :t="store.playingPlayList[store.indexPlayList].t" />
  </template>
</template>
