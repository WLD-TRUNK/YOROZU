# CODEX_VER0 貯蓄DB `マルチセレクト用` 対応式

前提:
- `貯蓄DB` に `マルチセレクト用`（multi_select）プロパティを追加済み
- `中間DB -> 支出一覧` を使って `支出DB` から集計

---

## A. `TECH貯蓄` が選ばれている時だけ集計（固定ターゲット）

```notion-formula
if(
  empty(prop("中間DB")) or empty(prop("マルチセレクト用")),
  0,
  if(
    not format(prop("マルチセレクト用")).contains("TECH貯蓄"),
    0,
    lets(
      spendList, prop("中間DB").at(0).prop("支出一覧"),
      targetDate, if(empty(prop("日付")), "", formatDate(prop("日付"), "YYYY-MM-DD")),

      total,
        spendList.filter(
          format(current.prop("カテゴリー")) == "TECH貯蓄"
          and if(
            targetDate == "",
            true,
            formatDate(current.prop("日付"), "YYYY-MM-DD") == targetDate
          )
        ),

      total.map(current.prop("支出")).sum()
    )
  )
)
```

---

## B. `マルチセレクト用` で選んだカテゴリすべてを集計（可変ターゲット）

```notion-formula
if(
  empty(prop("中間DB")) or empty(prop("マルチセレクト用")),
  0,
  lets(
    spendList, prop("中間DB").at(0).prop("支出一覧"),
    selectedText, format(prop("マルチセレクト用")),
    targetDate, if(empty(prop("日付")), "", formatDate(prop("日付"), "YYYY-MM-DD")),

    total,
      spendList.filter(
        selectedText.contains(format(current.prop("カテゴリー")))
        and if(
          targetDate == "",
          true,
          formatDate(current.prop("日付"), "YYYY-MM-DD") == targetDate
        )
      ),

    total.map(current.prop("支出")).sum()
  )
)
```

---

## メモ
- 日付条件を月単位にする場合:
  - `YYYY-MM-DD` を `YYYY-MM` に変更。
- `TECH貯蓄` の表記は `支出DB.カテゴリー` と完全一致させる（例: `TECH費貯蓄` なら式内も同じ表記にする）。
