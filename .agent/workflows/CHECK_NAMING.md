---
description: 命名規則（UPPER_SNAKE_CASEと例外）を自動チェックする
---
# ✅ 命名ルールチェック

このワークフローは、ユーザー/AI作成ファイルの命名が `UPPER_SNAKE_CASE` に従っているか確認します。対象は `.agent/` と `YOROZU_PROJECT/` 全体です（ツールにより固定名が必要な場合は例外として扱います）。

## 手順1: 実行
- PowerShell で以下を実行します。
  - `powershell -ExecutionPolicy Bypass -File .agent/scripts/CHECK_NAMING.ps1`
  - 出力は `OK` / `NG` と件数（`COUNT` / `NG_COUNT`）です。

## 手順2: 修正
- 違反一覧が出た場合は、**ユーザー/AI作成ファイルのみ**を `UPPER_SNAKE_CASE` にリネームします。
- 例外扱いにする場合は、`.agent/rules/STRUCTURE_POLICY.md` と `.agent/README.md` に明記します。

## 手順3: 参照更新
- リネームしたファイルへの参照（README/ワークフロー/コード内パス）を必ず更新します。

## 手順4: 再実行
- 再度スクリプトを実行し、違反が 0 件であることを確認します。
