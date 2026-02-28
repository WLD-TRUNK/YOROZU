# YOROZU

![ヘッダー](assets/header.png)

YOROZU は、AIエージェントが複数リポジトリを統合管理するための司令塔です。
この README は `.agent/` の全体像と動線をまとめます。詳細は配下ディレクトリの README を参照してください。

## 読む順

1. `.agent/README.md`（本ファイル）
2. `YOROZU_PROJECT/*/README.md`（各ツールの詳細）
3. `.agent/workflows/`（実行手順）

## 優先順位（動線の絶対順）

1) **ルール（常時適用）**: `.agent/rules/`
2) **スキル（必要時ロード）**: `.agent/skills/`
3) **ワークフロー（/で起動）**: `.agent/workflows/`
4) **ツール配下の .agent**: 各ツールのローカル規約（例: `YOROZU_PROJECT/DAY_REPORT/.agent`）
5) **実行スクリプト/CLI**: `*.py`, `*.ps1`, `*.js`
6) **データ/成果物**: JSON/画像/ログ

## 最短動線（目的別）

1) **新規リポジトリ作成**
   - `.agent/rules/REPO_CREATION.md` → `/create-yorozu-project-complete`

2) **アプリ実装**
   - `/build-app-simple` → 必要に応じ `/update-yorozu-identity`

3) **リリース作成**
   - `/create-release` → `.agent/templates/RELEASE_NOTES_TEMPLATE.md` + `.agent/assets/HEADER_PROMPT.txt`

4) **日報記録**
   - `YOROZU_PROJECT/DAY_REPORT/.agent/workflows/LOG_DAILY_REPORT.md` → `LOGGER.py` または `MAIN.py`

5) **日報保守/診断**
   - `YOROZU_PROJECT/DAY_REPORT/maintenance/TOOLBOX.py` を最優先

6) **Notion知識化**
   - `YOROZU_PROJECT/NOTION_KNOWLEDGE_VAULT/README.md` の標準手順 → `YOROZU_PROJECT/NOTION_KNOWLEDGE_VAULT/scripts/INGEST_ARTICLE.py`

7) **動画解析**
   - `YOROZU_PROJECT/VIDEO_ANALYSIS/scripts/DOWNLOAD_AND_CAPTURE.py`

8) **TIMER_F 実行**
   - `YOROZU_PROJECT/TIMER_F/INDEX.html` をブラウザで開く

9) **構成図更新**
   - `/visualize-architecture` → `.agent/assets/architecture/YOROZU_ARCHITECTURE.drawio` → `.agent/assets/architecture/YOROZU_ARCHITECTURE.svg`

10) **マルチレポ集約管理**
   - `YOROZU_PROJECT/CONTROL_HUB/README.md`

## 構成

```
YOROZU/
├── .agent/                       # 司令塔（ルール / スキル / ワークフロー）
│   ├── assets/                   # 共有素材（構成図は assets/architecture/）
│   ├── rules/                    # ルール
│   ├── workflows/                # ワークフロー
│   ├── skills/                   # スキル
│   ├── scripts/                  # 共通スクリプト
│   └── secure/                   # 機密保管（Git管理外）
└── YOROZU_PROJECT/               # 独立リポジトリ群
    ├── CONTROL_HUB/              # 集約サーバー
    ├── DAY_REPORT/               # 日報
    ├── NOTION_KNOWLEDGE_VAULT/   # Notion知識化
    ├── VIDEO_ANALYSIS/           # 動画解析
    └── TIMER_F/                  # タイマー
```

## ワークフロー一覧

- `workflows/CREATE_YOROZU_PROJECT_COMPLETE.md`
- `workflows/CREATE_REPO_FROM_FOLDER.md`
- `workflows/CREATE_PROMPT_REPO.md`
- `workflows/BUILD_APP_SIMPLE.md`
- `workflows/GIT_AUTO_COMMIT.md`
- `workflows/CHECK_NAMING.md`
- `workflows/UPDATE_YOROZU_IDENTITY.md`
- `workflows/GENERATE_HEADER_IMAGE.md`
- `workflows/CREATE_RELEASE.md`
- `workflows/REVIEW_REPO_QUALITY.md`
- `workflows/VISUALIZE_ARCHITECTURE.md`

## スキル一覧（抜粋）

- `skills/notion-formula/SKILL.md`（Notion数式のMD限定運用）
- `skills/design-ui/SKILL.md`
- `skills/eng-architect/SKILL.md`
- `skills/eng-backend/SKILL.md`
- `skills/eng-frontend/SKILL.md`
- `skills/marketing-growth/SKILL.md`
- `skills/ops-support/SKILL.md`
- `skills/pm-shipper/SKILL.md`
- `skills/qa-tester/SKILL.md`

## ルール一覧

- `rules/STRICT_JAPANESE.md`（日本語出力ポリシー）
- `rules/REPO_CREATION.md`（命名・作成ルール）
- `rules/STRUCTURE_POLICY.md`（配置ルール）

## 命名ルールの例外（固定名）

以下は標準名として固定運用するため、`UPPER_SNAKE_CASE` の対象外です。

- `README.md`
- `SKILL.md`
- `DESIGN.md`
- `LICENSE`
- `CHANGELOG.md`
- `__init__.py`
- `docker-compose.yml`
- `docker-compose.yaml`
- `package.json`

## 仕様

- `ANTIGRAVITY_AGENT_CONTROL_SPEC.md`

## ガバナンスの影響（要約）

- 品質と一貫性は上がるが、スピードと柔軟性は下がる。
- 日本語強制により可読性は上がるが、短文で済む場面でも長くなりやすい。
- 雅（Miyabi）は見栄えと品位を優先するため、過剰設計になりやすい。

## 注意（運用の前提）

- `YOROZU_PROJECT/` は独立リポジトリ運用が前提。
- `runs/`, `logs/`, `__pycache__/` などの生成物は Git 管理外で運用する。

## 参照（詳細）

- `YOROZU_PROJECT/CONTROL_HUB/README.md`
- `YOROZU_PROJECT/DAY_REPORT/README.md`
- `YOROZU_PROJECT/NOTION_KNOWLEDGE_VAULT/README.md`
- `YOROZU_PROJECT/VIDEO_ANALYSIS/README.md`
- `YOROZU_PROJECT/TIMER_F/README.md`
