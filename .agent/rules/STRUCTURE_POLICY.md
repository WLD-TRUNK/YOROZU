---
description: YOROZUワークスペースの公式ディレクトリ構造と配置ルール（何をどこに置くか）
---

# ディレクトリ構造・配置ポリシー

**YOROZU** ワークスペースにおける「何がどこにあるべきか（正解）」を定義するルールです。すべての新規作成・移動はこの構造に従う必要があります。

## 1. ルート構成

| ディレクトリ | 役割 | カテゴリ |
| :--- | :--- | :--- |
| **`.agent/`** | **管理者（統括）** | **知能パッケージ**。ルール、スキル、ワークフローの集約先。 |
| **`YOROZU_PROJECT/`** | **作業者（実行）** | **工場**。生成されたプロジェクトやツールを配置する場所。 |
| **`docs/`** | **一時置き場** | **一時作業用**。恒久資料は `.agent/` または `README` / `workflows` に集約し、作業後に移動・削除する。 |

---

## 2. エージェントパッケージ（`.agent/`）

エージェントの能力と判断基準はここに集約されます。情報は README またはワークフローに集約します。

- **`rules/`**: **判断基準**。行動前に参照すべき規約（言語ポリシー、リポジトリルールなど）。
- **`workflows/`**: **標準手順**。タスク実行のための具体的なステップ定義。
- **`skills/`**: **専門能力**。特定ドメインに関する知識と実践パターン。
    - **配置ルール**: スキル定義ファイルは `skills/{skill-name}/SKILL.md` に配置する。
    - **スコープ方針**: 原則はワークスペース（`.agent/skills/`）のみ使用し、グローバルスキルは例外的に採用する。
    - **拡張構成**: 必要に応じて `resources/`, `scripts/`, `templates/`, `examples/` を同梱する。
- **`assets/`**: **共通資産**。ヘッダー画像やプロンプトなどの共有素材。
- **`assets/architecture/`**: **構成図**。Draw.io と SVG の保存先。
- **`scripts/`**: **共通ツール**。画像生成などの汎用スクリプト。
- **`secure/`**: **機密保管**。認証情報や秘匿設定を置く専用領域（Git管理外）。

---

## 3. プロジェクトファクトリー（`YOROZU_PROJECT/`）

ここには、各サブプロジェクトが**独立したパッケージ**として配置されます。すべて単独リポジトリとして管理し、集約サーバーは専用プロジェクトに分離します。

- **原則**: サブディレクトリは親や兄弟に依存しない単独完結の構成とする。
- **命名**: `UPPER_SNAKE_CASE` を厳守する。
- **構造例**:
    - `DAY_REPORT/`: 独立したレポートモジュール。
    - `VIDEO_ANALYSIS/`: 独立したPythonツール。
    - `NOTION_KNOWLEDGE_VAULT/`: 独立した知識化ツール。
    - `CONTROL_HUB/`: 独立リポを横断管理する集約サーバー。

---

## 4. 命名ルール（ファイル/スクリプト）

- **対象**: ユーザー/AI が作成・編集するドキュメント、スクリプト、テンプレート、規約ファイルなど。
- **範囲**: `.agent/` と `YOROZU_PROJECT/` 全体を対象とし、ツールの固定名が必要な場合は例外として扱う。
- **形式**: 原則 `UPPER_SNAKE_CASE`（例: `DATA_EXPORT.md`, `RUN_SUMMARY.py`, `BATCH_UPLOAD.ps1`）。
- **例外（標準名）**: `README.md`, `SKILL.md`, `DESIGN.md`, `LICENSE`, `CHANGELOG.md`, `__init__.py`, `docker-compose.yml`, `docker-compose.yaml`, `package.json` など、固定名で運用するものは例外。
- **自動生成/インストール**: パッケージマネージャやビルドツールが生成・導入するものはツール規約に従い **小文字** のまま扱い、名前変更しない（例: `.venv/`, `node_modules/`, `dist/`, `build/`, `pnpm-lock.yaml`）。
- **改名の原則**: 既存ファイルの改名は参照修正が必須のため、影響範囲を確認してから実施する。

---

## 5. 正規フロー（認可済み動線）

以下の動線が「YOROZU標準」として認可されています。

### デイリーレポートフロー
- **トリガー**: `YOROZU_PROJECT/CONTROL_HUB/MCP_SERVER.py`（エントリーポイント）
- **ロジック**: `YOROZU_PROJECT/DAY_REPORT/SHEETS_HANDLER.py`
- **出力**: Google Sheets（ACTION_VIEW）

### ブランディングフロー
- **トリガー**: ワークフロー（例: `/update-yorozu-identity`）
- **ツール**: `.agent/scripts/GENERATE_IMAGE.js`, `.agent/scripts/ADD_TEXT_TO_HEADER.ps1`
- **出力**: `.agent/assets/header.png`, `README.md`
