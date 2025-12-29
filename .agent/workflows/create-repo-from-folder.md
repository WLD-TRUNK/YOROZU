---
description: 既存のフォルダをYOROZU_PROJECT配下のGitHubリポジトリに変換します
---
# 📂 フォルダからリポジトリを作成

このワークフローは、既存のフォルダをGitHubリポジトリに変換します。

## Step 1: 分析と名前提案 // turbo
- **場所確認**: 現在のディレクトリが `YOROZU_PROJECT` 内にあるか確認します。
  - `YOROZU_PROJECT` 外の場合はユーザーに警告し、確認または移動を求めます。
- **コンテンツ分析**: フォルダ内のファイル（README, ソースコード等）を読み込み、このプロジェクトが何をするものなのか理解します。
- **リネーム提案**: 現在のフォルダ名は「適当なもの」であるという前提に立ち、プロジェクトの本質を表す最適なリポジトリ名を考案します。
  - たとえ現在の名前が `kebab-case` であっても、より適切な名前があれば提案します（例: `test` -> `ai-agent-controller`）。
  - ユーザーに改名を確認し、承認されたらフォルダ名を変更します。

## Step 2: Gitの初期化 // turbo
- `git init` を実行します。
- `.gitignore` を作成し、以下の項目を必ず除外設定に追加します：
  - `YOROZU_PROJECT/` (親プロジェクトの管理フォルダ)
  - `ANTIGRAVITY_AGENT_CONTROL_SPEC.MD` (エージェント仕様書)
  - `*_SPEC.MD`
  - その他OS標準の除外ファイル（.DS_Store, Thumbs.db等）

## Step 3: 初回コミット // turbo
- `git add .` を実行してファイルをステージングします。
- `git commit -m "Initial commit"` でコミットします。

## Step 4: GitHubリポジトリの作成 // turbo
- `gh repo create` を実行します。
  - デフォルトで **Private** リポジトリとして作成します（`--private`）。
  - ソースは現在のディレクトリ（`--source=.`）。
  - リモート名は `origin`。

## Step 5: ブランチ設定とプッシュ // turbo
- デフォルトブランチを `main` に設定します。
  - `git branch -m master main`
- `git push -u origin main` を実行します。
- 必要に応じて GitHub 上のデフォルトブランチ設定も `main` に更新し、古い `master` ブランチがあれば削除します。

