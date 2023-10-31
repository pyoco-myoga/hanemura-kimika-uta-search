<script lang="ts" setup>
import {Song} from "@/@types/global/song";
import SongCard from "@/components/SongCard.vue";

import {ref, Ref} from "vue";
import * as database from "firebase/database";
import Fuse from "fuse.js";
import {watch} from "vue";
import InfiniteLoading from "v3-infinite-loading";
import "v3-infinite-loading/lib/style.css";
import {StateHandler} from "v3-infinite-loading/lib/types";
import {v4 as uuidv4} from "uuid";
import {favoriteSongs, uidRef, songs} from "@/common";

const db = database.getDatabase();

const params = new URLSearchParams(location.search);
const q = params.get("q");
const v = params.get("v");

let songList: {uuid: string; song: Song}[] = [];
Object.keys(songs).map((uuid) => {
  songList.push({
    uuid: uuid,
    song: songs[uuid],
  });
});
songList.sort((a, b) => {
  if (a.song.artist > b.song.artist) {
    return 1;
  } else if (a.song.artist === b.song.artist) {
    return a.song.name > b.song.name ? 1 : -1;
  } else {
    return -1;
  }
});

const searchWord = ref(q || "");
const filterYoutubeURL = ref(v || "");

function getVideoID(youtubeUrlOrVideoID: string): string | null {
  const IS_VIDEOID_REGEX = /^[a-zA-Z0-9_-]{11}$/;
  if (IS_VIDEOID_REGEX.test(youtubeUrlOrVideoID)) {
    return youtubeUrlOrVideoID;
  }
  const youtubeURL = new URL(youtubeUrlOrVideoID);

  // youtu.be
  // youtube.com
  if (youtubeURL.pathname == "/watch") {
    const videoID = youtubeURL.searchParams.get("v");
    return videoID ?? null;
  } else {
    const mayVideoID = youtubeURL.pathname.split("/").at(-1);
    if (mayVideoID === undefined) {
      return null;
    } else {
      if (IS_VIDEOID_REGEX.test(mayVideoID)) {
        return mayVideoID;
      } else {
        return null;
      }
    }
  }
}

const fuse = new Fuse(songList, {
  shouldSort: true,
  threshold: 0.4,
  keys: ["song.artist", "song.name"],
});

type SearchOptions = "favorite" | "full" | "recommended";
const validSearchOptions: Ref<Array<SearchOptions>> = ref(["recommended"]);

const onAddFavorite = (songUUID: string) => {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (favoriteSongs.value.has(songUUID)) {
    return;
  }
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...favoriteSongs.value, songUUID]
  );
};

const onDeleteFavorite = (songUUID: string) => {
  console.log(favoriteSongs.value);
  if (uidRef.value === null) {
    return;
  }
  if (favoriteSongs.value === null) {
    return;
  }
  if (!favoriteSongs.value.has(songUUID)) {
    return;
  }
  database.set(
    database.ref(db, `users/${uidRef.value}/favorite`),
    [...(favoriteSongs.value || [])].filter(v => v !== songUUID)
  );
};

const NUM_NEW_LOAD = 30;
const searchResult: Ref<{uuid: string, song: Song}[]> = ref([]);
const resultId: Ref<string> = ref(uuidv4());
const showedSongs: Ref<{uuid: string, song: Song}[]> = ref([]);

let searchTimerId: NodeJS.Timeout | null = null;
const updateSearchResult = () => {
  if (searchTimerId !== null) {
    clearTimeout(searchTimerId);
  }
  searchTimerId = setTimeout(() => {
    let result: Array<{uuid: string, song: Song}>;
    if (searchWord.value === "") {
      result = songList;
    } else {
      result = fuse.search(searchWord.value)
        .map(result => ({uuid: result.item.uuid, song: result.item.song, }));
    }
    result = result
      .filter(({uuid}) => {
        if (uidRef.value === null) {
          return true;
        } else if (validSearchOptions.value.includes("favorite") && !favoriteSongs.value?.has(uuid)) {
          return false;
        } else {
          return true;
        }
      })
      .filter(({song}) => {
        if (validSearchOptions.value.includes("full")) {
          return song.length === "full";
        } else {
          return true;
        }
      })
      .filter(({song}) => {
        if (validSearchOptions.value.includes("recommended")) {
          return song.recommended ?? false;
        } else {
          return true;
        }
      })
      .filter(({song}) => {
        if (filterYoutubeURL.value === "") {
          return true;
        }
        if (song.video === getVideoID(filterYoutubeURL.value)) {
          return true;
        } else {
          return false;
        }
      });

    searchResult.value = result;
    resultId.value = uuidv4();
    showedSongs.value = [];
  }, 50);
};

updateSearchResult();
watch([searchWord, validSearchOptions, filterYoutubeURL], updateSearchResult);

const load = (state: StateHandler) => {
  if (showedSongs.value.length == searchResult.value.length) {
    state.complete();
  } else {
    showedSongs.value.push(
      ...searchResult.value.slice(
        showedSongs.value.length,
        showedSongs.value.length + NUM_NEW_LOAD));
    state.loaded();
  }
}

</script>

<template>
  <v-container>
    <v-row class="ma-2">
      <v-text-field label="曲名 / アーティスト名" density="compact" prepend-inner-icon="mdi-magnify" append-inner-icon="mdi-close"
        @click:append-inner="searchWord = ''" v-model="searchWord" variant="solo" single-line hide-details />
    </v-row>

    <v-row class="ma-2">
      <v-col cols="auto">
        <v-btn-toggle class="elevation-1" v-model="validSearchOptions" background-color="primary" dark multiple>
          <template v-if="uidRef">
            <v-btn value="favorite">
              お気に入りのみ
            </v-btn>
          </template>
          <v-btn value="recommended">
            おすすめのみ
          </v-btn>
          <v-btn value="full">
            フルのみ
          </v-btn>
        </v-btn-toggle>
      </v-col>
      <v-col>
        <v-text-field prepend-inner-icon="mdi-youtube" append-inner-icon="mdi-close"
          @click:append-inner="filterYoutubeURL = ''" variant="solo" label="YouTube URL / Video ID"
          v-model="filterYoutubeURL" density="compact" single-line hide-details />
      </v-col>
    </v-row>
  </v-container>

  <template v-for="{uuid, song} in showedSongs" :key="song.uuid">
    <SongCard :video="song.video" :artist="song.artist" :name="song.name" :t="song.t" :endt="song.endt"
      :length="song.length" :sing-type="song.singType" :is-favorite="favoriteSongs?.has(uuid) ?? null" :is-full="false"
      :recommended="song.recommended" @add-favorite="onAddFavorite" @remove-favorite="onDeleteFavorite"
      :playlist="[uuid]" :playlist-index="0" />
  </template>
  <InfiniteLoading :key="resultId" @infinite="load" :distance="100" />
</template>
