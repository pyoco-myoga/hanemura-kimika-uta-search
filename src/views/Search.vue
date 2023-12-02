<script lang="ts" setup>
import SongCard from "@/components/SongCard.vue";

import {ref, Ref} from "vue";
import {watch} from "vue";
import InfiniteLoading from "v3-infinite-loading";
import "v3-infinite-loading/lib/style.css";
import {StateHandler} from "v3-infinite-loading/lib/types";
import {v4 as uuidv4} from "uuid";
import {
  favoriteSongs,
  uidRef,
  addToFavorite,
  removeFromFavorite,
  algoliaIndex,
  Song
} from "@/common";

const params = new URLSearchParams(location.search);
const q = params.get("q");
const v = params.get("v");

const searchWord = ref(q || "");
const filterYoutubeURL = ref(v || "");

function getVideoID(youtubeUrlOrVideoID: string): string | null {
  const IS_VIDEOID_REGEX = /^[a-zA-Z0-9_-]{11}$/;
  if (IS_VIDEOID_REGEX.test(youtubeUrlOrVideoID)) {
    return youtubeUrlOrVideoID;
  }

  let youtubeURL;
  try {
    youtubeURL = new URL(youtubeUrlOrVideoID);
  } catch (e) {
    return null;
  }

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

const HITS_PER_PAGE = 100;

type SearchOptions = "favorite" | "full" | "recommended";
const validSearchOptions: Ref<Array<SearchOptions>> = ref(["recommended"]);

let resultId: string = uuidv4();
const showedSongs: Ref<{uuid: string, song: Song}[]> = ref([]);
let loadedPageNumber = -1;

async function search() {
  const videoID = getVideoID(filterYoutubeURL.value);
  const searchResult = await algoliaIndex.search<Song>(searchWord.value, {
    page: ++loadedPageNumber,
    hitsPerPage: HITS_PER_PAGE,
    filters: (validSearchOptions.value.includes("favorite") && favoriteSongs.value !== null) ?
      Array.from(favoriteSongs.value).map(uuid => `objectID:${uuid}`).join(" OR ") : "",
    facets: [
      "recommended",
      "video",
      "length",
    ],
    facetFilters: [
      ...((validSearchOptions.value.includes("recommended")) ? ["recommended:true"] : []),
      ...((videoID !== null) ? [`video:${videoID.replace(/^(-)/, "\\$1")}`] : []),
      ...((validSearchOptions.value.includes("full")) ? ["length:full"] : []),
    ],
  });
  return searchResult.hits.map(hit => ({
    uuid: hit.objectID,
    song: {
      artist: hit.artist,
      name: hit.name,
      video: hit.video,
      t: hit.t,
      endt: hit.endt,
      length: hit.length,
      singType: hit.singType,
      recommended: hit.recommended
    }
  }));
}

let searchTimerId: NodeJS.Timeout | null = null;

watch([searchWord, validSearchOptions, filterYoutubeURL], () => {
  if (searchTimerId !== null) {
    clearTimeout(searchTimerId);
  }
  try {
    loadedPageNumber = -1;
    showedSongs.value = [];
    resultId = uuidv4();
  } catch (e) {
    console.debug(e);
  }
});

const load = async (state: StateHandler) => {
  searchTimerId = setTimeout(async () => {
    try {
      const result = await search();
      showedSongs.value.push(
        ...result
      );
      if (result.length < HITS_PER_PAGE) {
        state.complete();
      } else {
        state.loaded();
      }
    } catch (e) {
      console.debug(e);
      state.error();
    }
  }, 500);
};

</script>

<template>
  <v-container>
    <v-row class="ma-2">
      <v-text-field label="曲名 / アーティスト名" density="compact" prepend-inner-icon="mdi-magnify" append-inner-icon="mdi-close"
        @click:append-inner="searchWord = ''" v-model="searchWord" variant="solo" single-line hide-details />
    </v-row>

    <v-row class="ma-2">
      <v-col cols="12" sm="auto" md="auto" lg="auto" xl="auto">
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

  <template v-for="{uuid, song} in showedSongs" :key="`${result}-${uuid}`">
    <SongCard :video="song.video" :artist="song.artist" :name="song.name" :t="song.t" :endt="song.endt"
      :length="song.length" :sing-type="song.singType" :is-favorite="favoriteSongs?.has(uuid) ?? null" :is-full="false"
      :recommended="song.recommended" @add-favorite="addToFavorite" @remove-favorite="removeFromFavorite" :uuid="uuid" />
  </template>
  <InfiniteLoading :key="resultId" @infinite="load" :distance="100">
    <template v-slot:spinner>
      <div class="text-center">
        <v-progress-circular indeterminate />
      </div>
    </template>
    <template v-slot:complete>
      <v-divider />
    </template>
  </InfiniteLoading>
</template>
