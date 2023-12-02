<script lang="ts" setup>
import PlaylistCard from "@/components/PlaylistCard.vue";
import PlaylistForm from "@/components/PlaylistForm.vue";
import CustomPlaylistCard from "@/components/CustomPlaylistCard.vue";
import {favoriteSongs, publicPlaylists, privatePlaylists, officialPlaylists, uidRef, algoliaIndex} from "@/common";
import {ref, Ref, onMounted} from "vue";
import Fuse from "fuse.js";
import {watch} from "vue";

const params = new URLSearchParams(location.search);
const q = params.get("q");
const searchWord = ref(q || "");

// 持ち曲がこの数を超えることはないだろう
const MAX_HITS_PER_PAGE = 5000;
const recommendedSongs: Ref<string[] | null> = ref(null);

onMounted(async () => {
  const searchResult = await algoliaIndex.search<string>("", {
    attributesToRetrieve: ["objectID"],
    hitsPerPage: MAX_HITS_PER_PAGE,
    facets: ["recommended"],
    facetFilters: ["recommended:true"],
  });
  recommendedSongs.value = searchResult.hits.map(hit => hit.objectID);

});

type PlaylistElem = {
  title: string;
  description: string;
  image: string;
  songs: string[];
  playlistId: string;
}
type PlaylistFuse = Fuse<PlaylistElem>;

let privateFuse: PlaylistFuse | null = null;
watch([favoriteSongs, privatePlaylists], () => {
  if (privatePlaylists.value === null) {
    return;
  }
  const playlists = [
    {
      playlistId: "favorite",
      title: "お気に入り",
      description: "お気に入り登録した曲リスト",
      image: new URL("../../public/image/16x9/smile.png", import.meta.url).pathname,
      songs: Array.from(favoriteSongs.value ?? []),
    },
    ...Object.entries(privatePlaylists.value).map(([playlistId, playlist]) => ({
      playlistId,
      ...playlist
    })).sort((a, b) => b.title.localeCompare(a.title))
  ];
  if (privatePlaylists.value === null) {
    privateFuse = null;
  } else {
    privateFuse = new Fuse(playlists, {
      shouldSort: true,
      threshold: 0.4,
      keys: [
        "title",
        "description"
      ]
    });
  }
}, {immediate: true});

let officialFuse: PlaylistFuse | null = null;
watch([recommendedSongs, officialPlaylists], () => {
  if (officialPlaylists.value === null) {
    return;
  }
  const playlists = [
    {
      playlistId: "favorite",
      title: "おすすめ",
      description: "おすすめ曲",
      image: new URL("../../public/image/16x9/angel-smile.png", import.meta.url).pathname,
      songs: Array.from(recommendedSongs.value ?? []),
    },
    ...Object.entries(officialPlaylists.value).map(([playlistId, playlist]) => ({
      playlistId,
      ...playlist
    })).sort((a, b) => b.title.localeCompare(a.title))
  ];
  officialFuse = new Fuse(playlists, {
    shouldSort: true,
    threshold: 0.4,
    keys: [
      "title",
      "description"
    ]
  });
}, {immediate: true});

function getSearchResults(fuse: PlaylistFuse | null, searchWord: string): PlaylistElem[] {
  if (fuse === null) {
    console.debug(fuse);
    return [];
  }
  if (searchWord === "") {
    return (fuse as any)._docs;
  }
  return fuse.search(searchWord).map(({item}) => item);
}

const showPlaylistForm = ref(false);

const tab: Ref<"private" | "official" | "public"> = ref(uidRef.value !== null ? "private" : "official");

const favoritePlaylistImage = new URL("../../public/image/16x9/smile.png", import.meta.url).pathname;
const recommendedPlaylistImage = new URL("../../public/image/16x9/angel-smile2.png", import.meta.url).pathname;


</script>
<template>
  <v-tabs v-model="tab" fixed-tabs>
    <template v-if="uidRef !== null">
      <v-tab value="private">
        PRIVATE
      </v-tab>
    </template>
    <v-tab value="official">
      OFFICIAL
    </v-tab>
    <v-tab value="public">
      PUBLIC
    </v-tab>
  </v-tabs>

  <v-container>
    <v-row>
      <v-col class="ma-2">
        <v-text-field label="プレイリスト名" density="compact" prepend-inner-icon="mdi-magnify" append-inner-icon="mdi-close"
          @click:append-inner="searchWord = ''" v-model="searchWord" variant="solo" single-line hide-details />
      </v-col>
      <template v-if="uidRef !== null && tab === 'private'">
        <v-col class="my-2" cols="auto">
          <v-btn icon="mdi-plus" elevation="8" @click="showPlaylistForm = true" />
        </v-col>
      </template>
    </v-row>
  </v-container>

  <v-container>
    <v-window v-model="tab">
      <v-window-item value="private">
        <v-row>
          <!-- <template v-if="favoriteSongs !== null"> -->
          <!--   <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4"> -->
          <!--     <PlaylistCard playlist-id="favorite" playlist-title="お気に入り" playlist-description="お気に入り登録した曲リスト" -->
          <!--       :playlist-image="favoritePlaylistImage" visibility="public" :songs="Array.from(favoriteSongs)" /> -->
          <!--   </v-col> -->
          <!-- </template> -->
          <template v-if="privatePlaylists !== null"> <!-- <=> if loaded -->
            <template v-if="privateFuse !== null">
              <template
                v-for="({playlistId, title, description, songs, image}) of getSearchResults(privateFuse, searchWord)"
                :key="playlistId">
                <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4">
                  <PlaylistCard :playlist-id="playlistId as string" :playlist-title="title"
                    :playlist-description="description" :playlist-image="image" visibility="private" :songs="songs" />
                </v-col>
              </template>
              <!-- <template v-for="({item: {playlistId, title, description, songs, image}}) of privateFuse.search(searchWord)" -->
              <!--   :key="playlistId"> -->
              <!--   <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4"> -->
              <!--     <PlaylistCard :playlist-id="playlistId as string" :playlist-title="title" -->
              <!--       :playlist-description="description" :playlist-image="image" visibility="private" :songs="songs" /> -->
              <!--   </v-col> -->
              <!-- </template> -->
            </template>
            <!-- <template v-for="({title, description, songs, image}, playlistId) of privatePlaylists" :key="playlistId"> -->
            <!--   <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4"> -->
            <!--     <PlaylistCard :playlist-id="playlistId as string" :playlist-title="title" -->
            <!--       :playlist-description="description" :playlist-image="image" visibility="private" :songs="songs" /> -->
            <!--   </v-col> -->
            <!-- </template> -->
          </template>
        </v-row>
      </v-window-item>

      <v-window-item value="official">
        <v-row>
          <!-- <template v-if="recommendedSongs !== null"> -->
          <!--   <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4"> -->
          <!--     <PlaylistCard playlist-id="recommended" playlist-title="おすすめ" playlist-description="おすすめ曲" -->
          <!--       :playlist-image="recommendedPlaylistImage" visibility="public" :songs="recommendedSongs" /> -->
          <!--   </v-col> -->
          <!-- </template> -->
          <template v-if="officialPlaylists !== null">
            <template
              v-for="({playlistId, title, description, songs, image}) of getSearchResults(officialFuse, searchWord)"
              :key="playlistId">
              <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4">
                <PlaylistCard :playlist-id="playlistId as string" :playlist-title="title"
                  :playlist-description="description" :playlist-image="image" visibility="public" :songs="songs" />
              </v-col>
            </template>
          </template>
        </v-row>
      </v-window-item>

      <v-window-item value="public">
        <v-row>
          <template v-if="publicPlaylists !== null"> <!-- <=> if loaded -->
            <template v-for="({uid}, playlistId) of publicPlaylists" :key="playlistId">
              <template v-if="uid !== uidRef">
                <v-col cols="12" xs="12" sm="4" md="4" lg="4" xl="4">
                  <CustomPlaylistCard :playlist-id="playlistId as string" :uid="uid" visibility="public" />
                </v-col>
              </template>
            </template>
          </template>
        </v-row>
      </v-window-item>
    </v-window>
  </v-container>


  <template v-if="uidRef !== null">
    <PlaylistForm v-model="showPlaylistForm" :key="Number(showPlaylistForm)" />
  </template>
</template>
