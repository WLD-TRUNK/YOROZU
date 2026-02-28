# カテゴリー別集計_P 修正メモ (2026-02-08)

## 現在方針
- 値を書き込む運用は停止。
- `1月`〜`12月` / `合計` / `予算` は **formula型** に戻し済み。
- 複雑な relation 参照式は API 経由で `Type error with formula` になるため、最終貼り付けは Notion UI で実施する。

## 式ファイル
- `一時出力フォルダ/CODEX_KAKEIBO_VER0_CATEGORY_WEEKLY_FORMULA.md`
  - 月別式テンプレート
  - 合計（年合計）式
  - 予算（週次チケット＋右バー）式

## 補足
- `一時出力フォルダ/sync_category_kakeibo.py` は値同期スクリプト（式運用では実行不要）。
