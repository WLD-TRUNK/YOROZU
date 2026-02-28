# CODEX_VER0 貯蓄DB 自動計算式（数値維持 + 赤字エラー表示）
対象: `貯蓄DB` の formula プロパティ（2本構成）

## 目的
- `中間DB -> 支出一覧` を参照
- `貯蓄DB.名前` と一致する `支出DB.マルチセレクト用` を加算
- `【消費】` + `貯蓄DB.名前` は減算
- 同一支出行で `貯蓄名` と `【消費】貯蓄名` が同時に選ばれていたら赤字で通知
- 合計金額プロパティは数値型を維持する

## 1. 合計金額（数値プロパティ）
プロパティ例: `貯蓄残高_計算`
```notion-formula
if(
  empty(prop("中間DB")) or empty(prop("名前")),
  0,
  lets(
    spendList, prop("中間DB").at(0).prop("支出一覧"),
    targetName, format(prop("名前")),
    consumeName, "【消費】" + targetName,

    matched,
      spendList.filter(
        lets(
          picks, "," + replaceAll(format(current.prop("マルチセレクト用")), ", ", ",") + ",",
          picks.contains("," + targetName + ",") or picks.contains("," + consumeName + ",")
        )
      ),

    signed,
      matched.map(
        lets(
          picks, "," + replaceAll(format(current.prop("マルチセレクト用")), ", ", ",") + ",",
          amount, if(empty(current.prop("支出")), 0, current.prop("支出")),
          if(
            picks.contains("," + consumeName + ","),
            -1 * amount,
            amount
          )
        )
      ),

    signed.sum()
  )
)
```

## 2. エラー表示（テキストプロパティ）
プロパティ例: `選択整合性エラー`
```notion-formula
if(
  empty(prop("中間DB")) or empty(prop("名前")),
  "",
  lets(
    spendList, prop("中間DB").at(0).prop("支出一覧"),
    targetName, format(prop("名前")),
    consumeName, "【消費】" + targetName,

    errorCount,
      spendList.filter(
        lets(
          picks, "," + replaceAll(format(current.prop("マルチセレクト用")), ", ", ",") + ",",
          picks.contains("," + targetName + ",")
          and picks.contains("," + consumeName + ",")
        )
      ).length(),

    if(
      errorCount > 0,
      style("●", "red", "b"),
      ""
    )
  )
)
```

## 補足
- `マルチセレクト用` は文字列化して厳密一致判定しています（部分一致誤爆を回避）。
- `支出` が空の行は `0` として扱います。
- Notion仕様上、`style()` を使うと text 型になるため、数値型と装飾表示は同一プロパティで両立できません。
- 赤文字通知は `●` のみ表示にしてあります（文言は出しません）。
