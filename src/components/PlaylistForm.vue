<script lang="ts" setup>
import {ref} from 'vue';
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

function convertRelPathToPublicPath(path: string): string {
  return new URL(path, import.meta.url).pathname.replace(/^\/public/, "");
}

const image = ref(convertRelPathToPublicPath("../../public/image/16x9/angel-smile.png"));
const images = import.meta.glob("../../public/image/16x9/*.png");
</script>

<template>
  <v-dialog v-model="show" width="80%">
    <v-card>
      <v-text-field v-model="title" label="タイトル" single-line />
      <v-textarea v-model="description" label="概要" :max-rows="50" />
      <v-switch color="primary" v-model="visibilityRef" true-value="public" false-value="private">
        <template v-slot:label>
          <span :class="visibilityRef ? 'text-black' : 'text-grey-darken-3'">公開する(公開機能未実装)</span>
        </template>
      </v-switch>

      <v-select :v-model="image" label="画像"
        :items="Object.keys(images).map(path => ({image: convertRelPathToPublicPath(path)}))"
        :menu-props="{closeOnContentClick: true}">
        <template v-slot:item="{item}">
          <v-list-item @click="image = item.raw.image">
            <v-img :src="convertRelPathToPublicPath(item.raw.image)" aspect-ratio="16/9" :width="200" cover />
          </v-list-item>
        </template>
      </v-select>

      <div>
        <v-img :src="image" aspect-ratio="16/9" :width="200" cover />
      </div>

      <v-card-actions>
        <v-btn color="primary" block @click="() => {
          show = false;
          addOrUpdatePlayList({
            playlistId,
            title,
            description,
            imageURL: convertRelPathToPublicPath(image),
            songs: songs ?? [],
            visibility: visibilityRef
          });
        }">
          <template v-if="props.playlistId !== undefined">
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
