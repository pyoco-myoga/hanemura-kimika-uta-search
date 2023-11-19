<script lang="ts" setup>
import {ref} from 'vue';
import * as database from "firebase/database";
import {addOrUpdatePlayList} from '@/common';
import {v4 as uuidv4} from 'uuid';

const show = defineModel<boolean>({required: true});

const props = defineProps<{
  playlistId?: string;
  title?: string;
  description?: string;
  visibility?: "private" | "public";
  songs?: string[];
}>();

const playlistId = ref(props.playlistId ?? uuidv4());
const title = ref(props.title ?? "");
const description = ref(props.description ?? "");
const visibilityRef = ref(props.visibility ?? "private");

</script>

<template>
  <v-dialog v-model="show" width="80%">
    <v-card>
      <v-text-field v-model="title" label="タイトル" />
      <v-textarea v-model="description" label="概要" />
      <v-switch color="primary" v-model="visibilityRef" true-value="public" false-value="private">
        <template v-slot:label>
          <span :class="visibilityRef ? 'text-black' : 'text-grey-darken-3'">公開する</span>
        </template>
      </v-switch>
      <v-card-actions>
        <v-btn color="primary" block
          @click="() => {show = false; addOrUpdatePlayList(playlistId, title, description, songs ?? [], visibilityRef)}">
          <template v-if="playlistId !== undefined">
            更新
          </template>
          <template v-else>
            作成
          </template>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
