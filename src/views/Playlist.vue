<script lang="ts" setup>
import {Song} from "@/@types/global/song";
import PlaylistCard from "@/components/PlaylistCard.vue";
import PlaylistForm from "@/components/PlaylistForm.vue";
import CustomPlayListCard from "@/components/CustomPlayListCard.vue";
import {favoriteSongs, publicPlaylists, privatePlaylists, songs, uidRef} from "@/common";
import {ref} from "vue";
import {Ref} from "vue";

const params = new URLSearchParams(location.search);
const q = params.get("q");
const searchWord = ref(q || "");

const filterSongs = (allSongs: Record<string, Song>, filter: (all: Record<string, Song>, uuid: string) => boolean): (Song & {uuid: string})[] => {
  const filteredSongs = Object.keys(allSongs).reduce((result: Record<string, Song>, uuid) => {
    if (filter(allSongs, uuid)) {
      result[uuid] = allSongs[uuid];
    }
    return result;
  }, {});

  let result: (Song & {uuid: string})[] = [];
  for (const [uuid, song] of Object.entries(filteredSongs)[Symbol.iterator]()) {
    result.push({
      uuid,
      ...song
    });
  }
  return result;
}

const showPlayListForm = ref(false);

const tab: Ref<"private" | "official" | "public"> = ref(uidRef.value !== null ? "private" : "official");
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
          <v-btn icon="mdi-plus" elevation="8" @click="showPlayListForm = true" />
        </v-col>
      </template>
    </v-row>
  </v-container>

  <v-window v-model="tab">
    <v-window-item value="private">
      <template v-if="privatePlaylists !== null"> <!-- <=> if loaded -->
        <template v-for="(_, playlistId) of privatePlaylists" :key="playlistId">
          <CustomPlayListCard :playlist-id="playlistId as string" :uid="uidRef!" visibility="private" />
        </template>
      </template>
      <template v-if="favoriteSongs !== null">
        <PlaylistCard playlist-title="お気に入り" playlist-description="お気に入り登録した曲リスト" visibility="public"
          :songs="filterSongs(songs, (_, uuid) => favoriteSongs?.has(uuid) ?? false)" />
      </template>
    </v-window-item>

    <v-window-item value="official">
      <PlaylistCard playlist-title="おすすめ" playlist-description="おすすめ曲" visibility="public"
        :songs="filterSongs(songs, (songs, uuid) => songs[uuid].recommended ?? false)" />
    </v-window-item>

    <v-window-item value="public">
      <template v-if="publicPlaylists !== null"> <!-- <=> if loaded -->
        <template v-if="Object.values(publicPlaylists).filter(({uid}) => uid !== uidRef).length !== 0">
        </template>
        <template v-for="({uid}, playlistId) of publicPlaylists" :key="playlistId">
          <CustomPlayListCard :playlist-id="playlistId as string" :uid="uid" visibility="public" />
        </template>
      </template>
    </v-window-item>
  </v-window>


  <template v-if="uidRef !== null">
    <PlaylistForm v-model="showPlayListForm" />
  </template>
</template>
