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

const playingSong = computed(() => {
  if (store.indexPlayList === null) {
    return null;
  } else {
    return store.playingPlayList[store.indexPlayList];
  }
});

const onReady = () => {
  youtube.value?.playVideo();
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

  if (timerId !== null) {
    clearInterval(timerId)
  }
  timerId = setInterval(async () => {
    if (playingSong.value === null) {
      progress.value = 0;
    } else {
      const t = playingSong.value.t;
      const endt = playingSong.value.endt;

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
  }, 300);
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

let rewindTimerId: NodeJS.Timeout | null = null;
function onRewindClickedEvent() {
  if (rewindTimerId === null) {
    rewindTimerId = setTimeout(() => {
      if (playingSong.value !== null) {
        youtube.value?.seekTo(playingSong.value.t, true);
      }
      if (rewindTimerId !== null) {
        clearTimeout(rewindTimerId);
        rewindTimerId = null;
      }
    }, 100);
  } else {
    // footerが消えたときに間違えてその下にあった要素を押さないように
    setTimeout(() => {
      store.playPreviousPlayListSong();
    }, 50);
    clearTimeout(rewindTimerId);
    rewindTimerId = null;
  }
}

</script>

<template>
  <template v-if="playingSong !== null">
    <v-footer app class="elevation-10 justify-center">
      <v-container class="ma-0 pa-0">
        <v-row class="ma-0 pa-0 justify-center">
          <!-- player -->
          <v-col xs="12" sm="5" md="5" lg="5" xl="5" class="text-center">
            <YouTube :src="playingSong.video"
              :vars="{start: playingSong.t, end: playingSong.endt ?? undefined, controls: 0, modestbranding: 1}"
              @ready="onReady" height="20%" width="auto" @state-change="onStateChange" :key="playingSong.uuid"
              ref="youtube" />

          </v-col>
          <!-- controller -->
          <v-col xs="12" sm="7" md="7" lg="7" xl="7" class="justify-center">
            <v-row class="text-center justify-center">
              <v-col class="ma-auto" cols="1">
                <v-btn icon="mdi-share-variant" variant="text" @click="fireShareEvent = true;" />
              </v-col>
              <v-col cols="10">

                <v-list-item-title>
                  {{ playingSong.name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ playingSong.artist }}
                </v-list-item-subtitle>
              </v-col>
              <v-col class="ma-auto" cols="1">
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
                <template v-else-if="favoriteSongs?.has(playingSong.uuid)">
                  <v-btn icon="mdi-heart" variant="text" @click="removeFromFavorite(playingSong.uuid)" />
                </template>
                <template v-else>
                  <v-btn icon="mdi-heart-outline" variant="text" @click="addToFavorite(playingSong.uuid)" />
                </template>
              </v-col>
              <v-col class="text-center">
                <v-btn icon="mdi-rewind" variant="text" @click.stop="onRewindClickedEvent" />
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
    <ShareYoutube v-model="fireShareEvent" :name="playingSong.name" :artist="playingSong.artist"
      :video="playingSong.video" :t="playingSong.t" />
  </template>
</template>
