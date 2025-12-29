# Daily Reporting Rule

このルールは、YOROZU環境下でのエージェントの行動ログ記録を義務付けるものです。

## 1. 原則 (Principles)
エージェントは、タスク完了後に **Problem-Solution形式** でログを記録しなければなりません。
「何をしたか」だけでなく、「なぜその作業が必要だったのか（課題）」を記録し、ナレッジベースとして活用できるようにします。

## 2. 実行方法 (Usage)
`ash
python c:\Users\WLD.TRUNK\workspace_G\WLDNIA_2ND_BRAIN\YOROZU\YOROZU_PROJECT\DAY_REPORT\logger.py "{Task}" "{Problem}" "{Action}" --env "{Env}" --project "{Project}" --status "{Status}"
`

## 3. 引数の定義 (Arguments)

### 必須 (Positional)
1. **Task**: タスク名（例: "Logger Implementation"）
   - 目標となる作業の短いタイトル。
2. **Problem (Why)**: 課題背景（例: "既存の日報手動作成が手間で、フォーマットもバラバラだった"）
   - その作業を行うに至った動機や直面していた問題。
3. **Action (How)**: 解決策行動（例: "CLIツールを作成し、Why/Action分離型のスキーマを強制した"）
   - 具体的に何をして問題を解決したか。

### オプション (Optional)
- **--env / -e**: 環境設定技術（例: "Python, Google API"）
   - 使用した技術、ライブラリ、設定ファイルなど。デフォルト: "-"
- **--project / -p**: プロジェクト名（例: "DAY_REPORT"）
   - デフォルト: "YOROZU"
- **--status / -s**: ステータス（例: "Pending"）
   - デフォルト: "Done"

## 4. エラーハンドリング
ログ記録に失敗しても、ユーザータスク自体を中断させないでください。
