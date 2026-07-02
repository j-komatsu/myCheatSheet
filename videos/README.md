# 動画（mp4）管理ガイド

NotebookLM などで作成した mp4 をカテゴリ別に整理して管理するためのフォルダです。
大きな動画ファイルでリポジトリが肥大化しないよう、mp4 は **Git LFS** で管理します。

## フォルダ構成

カテゴリごとにサブフォルダを作成し、その中に mp4 を置いてください。

```
videos/
  git/
    branch-strategy.mp4
  docker/
    compose-basics.mp4
  aws/
    vpc-overview.mp4
```

- カテゴリ名はルートの README や Wiki のカテゴリ（コマンドリファレンス、プログラミング、IT基盤・運用 など）に合わせると探しやすくなります。
- ファイル名は英数字・ハイフンで、内容が分かる名前にしてください（例: `git-branch-strategy.mp4`）。

## 動画を追加する手順

初回のみ、リポジトリで Git LFS を有効化します（`.gitattributes` に `*.mp4` が登録済みなので通常は不要ですが、ローカル環境に git-lfs が未インストールの場合は入れてください）。

```bash
git lfs install
```

動画を追加する場合:

```bash
mkdir -p videos/<カテゴリ名>
cp ~/Downloads/xxx.mp4 videos/<カテゴリ名>/
git add videos/<カテゴリ名>/xxx.mp4
git commit -m "Add xxx.mp4 to videos/<カテゴリ名>"
git push
```

`.gitattributes` により `*.mp4` は自動的に LFS オブジェクトとしてアップロードされます。

## ブラウザで視聴する方法

### 1. リポジトリ上でそのまま再生（手軽）

GitHub 上で `videos/<カテゴリ名>/` フォルダを開き、mp4 ファイルをクリックすると、GitHub 標準のビデオプレイヤーでそのまま再生できます（LFS 管理のファイルでも同様に再生可能です）。

### 2. README や Wiki に埋め込んで YouTube 風に再生（推奨）

README.md や Wiki ページの中に、サムネイル付きの埋め込みプレイヤーとして表示したい場合は、`<video>` タグでリポジトリ上の LFS 動画を直接埋め込みます。

```html
<video src="https://media.githubusercontent.com/media/j-komatsu/myCheatSheet/master/videos/<カテゴリ名>/<ファイル名>.mp4" controls width="600"></video>
```

- `media.githubusercontent.com/media/...` は GitHub が LFS の実データを配信する URL です（`raw.githubusercontent.com` だと LFS のポインタファイルしか取得できないため使えません）。
- ブランチ名（`master`）やパスは実際のファイルに合わせて置き換えてください。

もう一つの方法として、GitHub の Issue / PR / Wiki 編集画面に mp4 をドラッグ＆ドロップでアップロードする方法もあります。この場合 `https://github.com/j-komatsu/myCheatSheet/assets/.../xxxx.mp4` のような URL が自動生成され、そのURLを1行だけ貼り付けるとサムネイル付きの埋め込みプレイヤーになります。ただしこの方法はリポジトリの Git 履歴には残らず、GitHub 側のアセットストレージに保存される点に注意してください。カテゴリ別にバージョン管理したい今回の用途では、上記の `videos/` フォルダ + `<video>` タグ埋め込みの方法を推奨します。
