# CODEX_家計簿_ver.0 関数メモ

## 合計（ベース）
```notion-formula
lets(
  /* 中間DBから全ての支出データを取得 */
  outcome, prop("中間DB").at(0).prop("支出一覧"),

  /* 年カテゴリー単位でデータをフィルター */
  total, outcome.filter(
    formatDate(current.prop("日付"), "YYYY") == prop("年")
    and current.prop("カテゴリー") == prop("名前")
  ),

  /* 支出を合計 */
  price, total.map(current.prop("支出")),
  price.sum()
)
```

## 集計テーブル（月別バー）修正版
- チケット表示なし
- 金額表示のみ（残額・使用額）
- バーは「使うほど短くなる」（残額ベース）
- 日付ヘッダーは表示しない
- バー開始位置を固定（Figure Spaceで残/使用を固定桁に右寄せ）

```notion-formula
lets(
  /* 背景色とバー設定 */
  bar, style("　", prop("背景色")),
  pad, " ",
  perRaw, prop("年予算"),
  per, if(empty(perRaw) or perRaw <= 0, 1, perRaw),

  /* 各月の支出合計 */
  month_value, [
    prop("1月"), prop("2月"), prop("3月"), prop("4月"), prop("5月"), prop("6月"),
    prop("7月"), prop("8月"), prop("9月"), prop("10月"), prop("11月"), prop("12月")
  ],
  numbers, [1,2,3,4,5,6,7,8,9,10,11,12],

  numbers.map(
    lets(
      month, current,
      usedRaw, month_value.at(current - 1),
      used, if(empty(usedRaw), 0, usedRaw),
      remain, if(used >= per, 0, per - used),

      /* 残額比率でバー長を作る: 使うほど短くなる */
      ratio, remain / per,
      barLen, if(ratio <= 0, 0, ceil(ratio * 10)),

      /* 3桁区切り */
      usedDot, used.format()
        .replace("(\d+)(\d{3})$", "$1,$2")
        .replace("(\d+)(\d{3},\d{3})$", "$1,$2"),
      remainDot, remain.format()
        .replace("(\d+)(\d{3})$", "$1,$2")
        .replace("(\d+)(\d{3},\d{3})$", "$1,$2"),
      usedPad, repeat(pad, if(10 - length(usedDot) > 0, 10 - length(usedDot), 0)) + usedDot,
      remainPad, repeat(pad, if(10 - length(remainDot) > 0, 10 - length(remainDot), 0)) + remainDot,
      monthLabel, if(month < 10, pad + format(month), format(month)),

      monthLabel + "月  残: " + remainPad + "円  使用: " + usedPad + "円  " + repeat(bar, barLen)
    )
  )
).join("\n")
```
