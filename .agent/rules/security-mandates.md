---
trigger: always_on
slug: security-mandates
---
# Security Mandates

- **No Hardcoded Secrets**: コード内にAPIキーやパスワードを直接記述してはならない。必ず os.getenv() や環境変数を使用すること。
- **SQL Injection**: SQLクエリには必ずパラメータ化されたクエリを使用すること。
- **Sanitization**: フロントエンドにおいてユーザー入力をレンダリングする際は、必ずサニタイズ処理を行うこと。
