# CODEX_VER1 B/S状況 実環境診断と修正式（2026-02-17）

## 実環境で確認した対象
- ルートページ: `CODEX_VER.1【2024年最新版】Notion家計簿`
  - page_id: `2f2d8928-02b6-8098-b6e4-c96afa72c460`
- B/S_DB: `308d8928-02b6-803d-8280-c04c7d05157b`
- 中間DB: `2f2d8928-02b6-81f0-8d7c-ebba1e830552`
- 貯蓄DB: `308d8928-02b6-803d-8b99-c37cdcd73d29`
- ローンDB: `308d8928-02b6-806e-821a-f0720e5700a8`
- ローン返済DB: `308d8928-02b6-8063-8440-ec947acb8f9a`

## 実環境での原因（確定）
1. `B/S_DB` 側の relation 名は `🚧 中間DB` だが、既存式は `prop("中間DB")` を参照している。
2. `中間DB` 側の relation 名は `💰 貯蓄DB` / `🏦 ローンDB` だが、既存式は `bridge.prop("貯蓄DB")` / `bridge.prop("ローンDB")` を参照している。
3. データ接続も未完了。
   - `B/S_DB` の全8行で `🚧 中間DB` が未リンク（0件）
   - `中間DB` の `マスター` 行で `💰 貯蓄DB` / `🏦 ローンDB` / `🏦 ローン返済DB` / `✍️ B/S_DB` がすべて0件
   - `B/S_DB.カテゴリー` も未設定行が多い

上記のため、式が解決できない/値が返らない状態になります。

---

## B/S_DB `B/S状況` 修正式（実環境名対応）
以下を `B/S_DB.B/S状況` にそのまま貼ってください。

```notion-formula
if(
  empty(prop("🚧 中間DB")),
  "",
  lets(
    bridge, prop("🚧 中間DB").at(0),
    rowName, format(prop("名前")),
    rowCategoryRaw, format(prop("カテゴリー")),
    rowCategory, if(empty(prop("カテゴリー")), rowName, rowCategoryRaw),
    nameCategoryMatched, rowName == rowCategory,
    isSavingRow, contains(rowName, "貯蓄"),
    saveLabel, if(nameCategoryMatched, "貯：", style("貯：", "red", "b")),
    remainLabel, if(nameCategoryMatched, "残：", style("残：", "red", "b")),
    scale, 10,
    saveBar, style("　", prop("背景色")),
    repayBar, style("　", prop("背景色")),
    principalBar, style("　", "gray_background"),

    saveAmount,
      bridge.prop("💰 貯蓄DB")
        .filter(format(current.prop("名前")) == rowName)
        .map(toNumber(current.prop("貯蓄状況")))
        .sum(),

    loanRows,
      bridge.prop("🏦 ローンDB")
        .filter(format(current.prop("決済手段")) == rowCategory),

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

---

## 先に必須の接続作業
1. `B/S_DB` の全行で `🚧 中間DB` に `マスター` を紐づける。
2. `中間DB.マスター` に以下を紐づける。
   - `💰 貯蓄DB`: 対象行すべて
   - `🏦 ローンDB`: 対象行すべて
   - `🏦 ローン返済DB`: 返済行すべて
   - `✍️ B/S_DB`: B/S行すべて
3. `B/S_DB.カテゴリー` は `名前` と同じ値を入れる（空欄運用しない）。

この3点を先にやらないと、式自体が正しくても表示は空になります。
