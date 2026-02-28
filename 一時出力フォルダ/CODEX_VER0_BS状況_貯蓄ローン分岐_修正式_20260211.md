# CODEX_VER0 B/S状況 修正式（マルチ管理向け）
作成日: 2026-02-11  
対象: `CODEX_家計簿_ver.0` / `B/S_DB` の `B/S状況` プロパティ

## 実環境確認（Notion API）
- `B/S_DB` には現在 `B/S状況 / 名前 / カテゴリー / 中間DB / 背景色` が存在
- `中間DB` 側 relation:
  - `貯蓄DB`
  - `ローンDB`
- `貯蓄DB` 側で参照する値: `貯蓄状況`
- `ローンDB` 側で参照する値: `決済手段`, `残返済金額合計_BS`

## 要件反映ロジック
1. `B/S_DB.名前` に `貯蓄` が含まれる行は、`貯蓄DB` の同名行の `貯蓄状況` を合計して表示  
2. `貯蓄` が含まれない行は、`ローンDB` の `決済手段` が一致する行の `残返済金額合計_BS` を合計して表示  
3. `B/S_DB.名前` と `B/S_DB.カテゴリー` が一致している行だけ計算する（不一致は金額0、`貯蓄：`/`残：`ラベルを赤表示）

## 1. B/S状況 数値版（従来どおり number）
```notion-formula
if(
  empty(prop("中間DB")),
  0,
  lets(
    bridge, prop("中間DB").at(0),
    rowName, format(prop("名前")),
    rowCategory, format(prop("カテゴリー")),
    nameCategoryMatched, rowName == rowCategory,
    isSavingRow, contains(rowName, "貯蓄"),

    if(
      isSavingRow,
      bridge.prop("貯蓄DB")
        .filter(nameCategoryMatched and format(current.prop("名前")) == rowName)
        .map(toNumber(current.prop("貯蓄状況")))
        .sum(),
      bridge.prop("ローンDB")
        .filter(nameCategoryMatched and format(current.prop("決済手段")) == rowCategory)
        .map(toNumber(current.prop("残返済金額合計_BS")))
        .sum()
    )
  )
)
```

## 2. B/S状況 バー表示版（text）
`B/S状況` に直接貼ると text 型表示になります。

```notion-formula
if(
  empty(prop("中間DB")),
  "",
  lets(
    bridge, prop("中間DB").at(0),
    rowName, format(prop("名前")),
    rowCategory, format(prop("カテゴリー")),
    nameCategoryMatched, rowName == rowCategory,
    isSavingRow, contains(rowName, "貯蓄"),
    saveLabel, if(nameCategoryMatched, "貯蓄：", style("貯蓄：", "red", "b")),
    remainLabel, if(nameCategoryMatched, "残：", style("残：", "red", "b")),
    scale, 10,
    saveBar, style("　", prop("背景色")),
    repayBar, style("　", prop("背景色")),
    principalBar, style("　", "gray_background"),

    saveAmount,
      bridge.prop("貯蓄DB")
        .filter(nameCategoryMatched and format(current.prop("名前")) == rowName)
        .map(toNumber(current.prop("貯蓄状況")))
        .sum(),

    loanRows,
      bridge.prop("ローンDB")
        .filter(nameCategoryMatched and format(current.prop("決済手段")) == rowCategory),

    remainAmount, loanRows.map(toNumber(current.prop("残返済金額合計_BS"))).sum(),
    principalAmount, loanRows.map(toNumber(current.prop("借入金"))).sum(),
    repaidRaw, loanRows.map(toNumber(current.prop("返済元金合計_BS"))).sum(),
    repaidAmount,
      if(
        repaidRaw < 0,
        0,
        if(repaidRaw > principalAmount, principalAmount, repaidRaw)
      ),

    saveAbs, abs(saveAmount),
    remainAbs, abs(remainAmount),
    saveLen, if(saveAbs == 0, 0, if(saveAbs >= 50000, scale, ceil(saveAbs / 5000))),
    principalLen, if(principalAmount <= 0, 0, scale),
    repaidLen,
      if(
        principalAmount <= 0,
        0,
        if(repaidAmount >= principalAmount, scale, ceil(repaidAmount / principalAmount * scale))
      ),

    saveText, format(saveAbs)
      .replace("(\\d+)(\\d{3})$", "$1,$2")
      .replace("(\\d+)(\\d{3},\\d{3})$", "$1,$2")
      .replace("(\\d+)(\\d{3},\\d{3},\\d{3})$", "$1,$2"),
    remainText, format(remainAbs)
      .replace("(\\d+)(\\d{3})$", "$1,$2")
      .replace("(\\d+)(\\d{3},\\d{3})$", "$1,$2")
      .replace("(\\d+)(\\d{3},\\d{3},\\d{3})$", "$1,$2"),

    if(
      isSavingRow,
      saveLabel + if(saveAmount < 0, "-¥", "¥") + saveText
        + "\n" + repeat(saveBar, saveLen),
      remainLabel + if(remainAmount < 0, "-¥", "¥") + remainText
        + "\n返済 " + repeat(repayBar, repaidLen)
        + "\n元本 " + repeat(principalBar, principalLen)
    )
  )
)
```

## 3. 推奨運用（数値維持したい場合）
1. `B/S状況` は「数値版」を使う  
2. 新規 text プロパティ（例: `B/S状況_バー`）を作り「バー表示版」を使う

## 補足
- 数値版は `number`、バー表示版は `text` を返します。
- 貯蓄以外の行は、`残額` を数値表示し、2段表示で `返済`（上）/`元本`（下）バーを出します。
- `B/S_DB` の既存行（`TECH費貯蓄`, `クレカ`, `ローン`, `立替金【友人】` など）に対応します。
