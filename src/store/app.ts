// Utilities
import {defineStore} from "pinia";
import {User, getAuth} from "firebase/auth";
import {Ref, ref} from "vue";
import {Song} from "@/common";


export const useAppStore = defineStore("app", () => {
  const user: Ref<User | null> = ref(null);
  getAuth().onAuthStateChanged((user_) => {
    if (user_ !== null) {
      user.value = user_;
    }
  });

  function setUser(user_: User | null) {
    user.value = user_;
  }

  const playingPlayList: Ref<({uuid: string} & Song)[]> = ref([]);
  const indexPlayList: Ref<number | null> = ref(null);
  function setPlayList(uuids: ({uuid: string} & Song)[]) {
    indexPlayList.value = null;
    playingPlayList.value = uuids;
  }
  function playNextPlayListSong() {
    if (indexPlayList.value === null && playingPlayList.value.length > 0) {
      indexPlayList.value = 0;
    } else if (indexPlayList.value !== null) {
      if (indexPlayList.value + 1 < playingPlayList.value.length) {
        indexPlayList.value += 1;
      } else {
        indexPlayList.value = null;
      }
    }
  }
  function playPreviousPlayListSong() {
    if (indexPlayList.value === null && playingPlayList.value.length > 0) {
      indexPlayList.value = 0;
    } else if (indexPlayList.value !== null) {
      if (indexPlayList.value - 1 >= 0) {
        indexPlayList.value -= 1;
      } else {
        indexPlayList.value = null;
      }
    }
  }
  function setPlayListIndex(index: number) {
    indexPlayList.value = index;
  }
  return {user, setUser, indexPlayList, setPlayListIndex, playingPlayList, setPlayList, playNextPlayListSong, playPreviousPlayListSong};
});
