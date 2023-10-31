
# 羽村きみか うたさーち


## Features
- あいまい検索
- ログイン機能
- お気に入り

## TODO
- クオリティアノテーション
- プレイリスト
    - デフォルトプレイリスト
    - プレイリスト作成
    - プレイリスト公開
    - プレイリスト再生
    - ランダム再生

## Firebase Realtime Database

```json
{
    users: {
        $uid: {
            favorite: Array<曲ID>,  // ただし、実質Set
            playlists: {
                $playlist_id: {
                    songs: Array<曲ID>,
                    public: boolean,
                }
            },
        }
    },
}
```

## Search
- あいまい検索
- お気に入り(ログイン時)
- 埋め込みYoutube
- Youtubeリンク
- 遅延レンダリング
- オプションフィルタ


## PlayList
- お気に入り登録プレイリスト
- おすすめ曲プレイリスト
- 公開プレイリスト
- カスタムプレイリスト(ログイン時)

