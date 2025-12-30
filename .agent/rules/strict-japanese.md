---
slug: strict-japanese
description: Enforce Japanese output for all artifacts and documentation.
trigger: always
---
# 完全日本語出力ルール

ユーザーとのチャットだけでなく、**作成するすべての成果物（ドキュメント、コミットログ、コード内コメント等）において日本語を使用すること**を強制します。

### 具体的な適用範囲
1. **ドキュメント全般**
   - README.md
   - walkthrough.md
   - implementation_plan.md
   - その他、ユーザー向けの説明ファイル
2. **Gitコミットメッセージ**
3. **コード内のコメント/docstring**
   - 変数名や関数名は英語でOK

### 例外
- ユーザーから明示的に英語での出力を指示された場合。
