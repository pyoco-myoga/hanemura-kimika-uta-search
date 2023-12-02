
<script lang="ts" setup>
import {
  TwitterAuthProvider,
  browserSessionPersistence,
  getAuth,
  getRedirectResult,
  onAuthStateChanged,
  setPersistence,
  signInWithPopup,
  signInWithRedirect,
} from "firebase/auth";
import {ref, Ref} from "vue";
import {useAppStore} from "@/store/app";
import {useRouter} from "vue-router";

const store = useAppStore();
const drawer: Ref<boolean | null> = ref(null);

const provider = new TwitterAuthProvider();
onAuthStateChanged(getAuth(), user => {
  console.log("onStateChange", user);
});
const loginEventListener = async () => {
  try {
    await setPersistence(getAuth(), browserSessionPersistence);
    await signInWithRedirect(getAuth(), provider);
    const result = await getRedirectResult(getAuth());
    // const result = await signInWithPopup(getAuth(), provider);
    if (result === null) {
      return;
    }
    store.setUser(result.user);
    console.log("event", store.user);
  } catch (err) {
    console.error(err);
  }
};
const logoutEventListener = async () => {
  try {
    store.setUser(null);
    await getAuth().signOut();
  } catch (err) {
    console.log(err);
  }
}

const router = useRouter()
const gotoSearchPage = () => {
  router.push({name: "Search"});
}
const gotoPlayListPage = () => {
  router.push({name: "Playlist"});
}
</script>

<template>
  <v-app-bar image="/image/background/head.png">
    <v-app-bar-nav-icon v-on:click.stop="drawer = !drawer" />
    <v-app-bar-title>羽村きみか うたさーち</v-app-bar-title>
    <template v-if="store.user === null">
      <v-btn @click="loginEventListener">ログイン</v-btn>
    </template>
    <template v-else>
      <v-menu>
        <template v-slot:activator="{props}">
          <v-btn class="ma-3" icon v-bind="props">
            <template v-if="store.user.photoURL !== null">
              <v-avatar :image="`https://gettwittericon-zmgcsnz2sq-uc.a.run.app/?url=${store.user.photoURL}`" />
            </template>
            <template v-else>
              <v-avatar color="surface-variant" />
            </template>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="logoutEventListener">
            ログアウト
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>

  <v-navigation-drawer image="/image/background/atsu.png" v-model="drawer" fixed app>
    <v-list>
      <v-list-item @click="gotoSearchPage">
        <template v-slot:prepend>
          <v-icon icon="mdi-magnify" />
        </template>
        <v-list-item-title> Search </v-list-item-title>
      </v-list-item>
      <v-list-item @click="gotoPlayListPage">
        <template v-slot:prepend>
          <v-icon icon="mdi-music" />
        </template>
        <v-list-item-title> PlayList </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
