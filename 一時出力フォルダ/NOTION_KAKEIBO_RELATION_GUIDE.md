# Notion家計簿 リレーション/計算式 参照ガイド

## 目的
中間DBと支出DB/収入DB/集計DB間のリレーション参照と、計算式（Notion数式）の使い方を整理する。

[as-of: 2026-01-24]

## 対象DB（ID一覧）
- 支出DB (`2f2d8928-02b6-8126-8d37-e1ebd985d759`)
- 収入DB (`2f2d8928-02b6-8116-97ba-c39ccb83f913`)
- 月別集計DB (`2f2d8928-02b6-81b3-802c-f33a84340c29`)
- カテゴリー別集計 (`2f2d8928-02b6-81c9-a0d5-e9c6b64fb352`)
- 中間DB (`2f2d8928-02b6-81f0-8d7c-ebba1e830552`)

## リレーション構成（中間DBハブ）
- 中間DB.カテゴリー別集計 → カテゴリー別集計 (2f2d8928-02b6-81c9-a0d5-e9c6b64fb352)
- 中間DB.月 → 月別集計DB (2f2d8928-02b6-81b3-802c-f33a84340c29)
- 中間DB.収入一覧 → 収入DB (2f2d8928-02b6-8116-97ba-c39ccb83f913)
- 中間DB.支出一覧 → 支出DB (2f2d8928-02b6-8126-8d37-e1ebd985d759)

### 逆方向（各DB→中間DB）
- 支出DB.中間DB → 中間DB
- 収入DB.中間DB → 中間DB
- 月別集計DB.中間DB → 中間DB
- カテゴリー別集計.中間DB → 中間DB

## 参照の基本ルール（Notion数式）
- リレーションはリスト扱い。単一参照は `prop("中間DB").at(0)` のように `.at(0)` で先頭を取る。
- リストに対して `filter` / `map` / `sum` を使い、`current` で各要素を参照する。
- 日付の比較は `formatDate` を使い、年・月は `prop("年")` + `prop("月")` でキー化している。
- 数式は Notion UI ではプロパティ名で記述する。APIが返す内部ID表記はそのまま使わない。

## 計算式（読みやすい表記）

### 支出DB

**週番号**
```notion-formula
if(
  empty(prop("日付")),
  "",
  lets(
    d, prop("日付"),

    /* その日の年の 1/1 を作る（DDD=day of year を利用して戻す） */
    jan1, dateSubtract(d, toNumber(formatDate(d, "DDD")) - 1, "days"),

    /* 「jan1 が属する週」の週頭（月曜） */
    firstWeekStart, dateSubtract(jan1, toNumber(formatDate(jan1, "E")) - 1, "days"),

    /* 週番号（1始まり） */
    w, floor(dateBetween(d, firstWeekStart, "days") / 7) + 1,

    /* 2023-W01 みたいにゼロ埋め */
    formatDate(d, "YYYY") + "-W" + if(w < 10, "0" + format(w), format(w))
  )
)
```

**チケット**
```notion-formula
ceil(prop("支出") / 500)
```

**年月キー**
```notion-formula
formatDate(prop("日付"), "YYYY-MM")
```

**月内週**
```notion-formula
lets(
  d, prop("日付"),

  /* 当月の1日 */
  monthStart, dateSubtract(d, toNumber(formatDate(d, "D")) - 1, "days"),

  /* 月曜始まり：その週の月曜(=週の先頭) */
  week0Start, dateSubtract(monthStart, toNumber(formatDate(monthStart, "E")) - 1, "days"),

  /* monthStartを含む週を「週1」とし、以降+1 */
  floor(dateBetween(d, week0Start, "days") / 7) + 1
)
```

### 月別集計DB

**支出 / 予算**
```notion-formula
floor(prop("支出合計") / prop("予算") * 100) / 100
```

**収入合計**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	income,prop("中間DB").at(0).prop("収入一覧"),
	
	/* 年月単位でデータをフィルター */
	total, income.filter(formatDate(current.prop("日付"), "YYYYMM") == prop("年") + prop("月")),
	
	/* 収入を合計 */
	price, total.map(current.prop("収入")),
	price.sum()
)
```

**支出合計**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome,prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYMM") == prop("年") + prop("月")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**支出 / 収入**
```notion-formula
floor(prop("支出合計") / prop("収入合計") * 100) / 100
```

**収入 - 支出**
```notion-formula
prop("収入合計") - prop("支出合計")
```

### カテゴリー別集計

**8月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 8 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**週予算**
```notion-formula
lets(
  outcome, prop("中間DB").at(0).prop("支出一覧"),

  ym, formatDate(now(), "YYYY-MM"),

  monthItems,
    outcome.filter(
      formatDate(current.prop("日付"), "YYYY-MM") == ym
      and current.prop("カテゴリー") == prop("名前")
    ),

  w1, monthItems.filter(current.prop("月内週") == 1).map(current.prop("チケット")).sum(),
  w2, monthItems.filter(current.prop("月内週") == 2).map(current.prop("チケット")).sum(),
  w3, monthItems.filter(current.prop("月内週") == 3).map(current.prop("チケット")).sum(),
  w4, monthItems.filter(current.prop("月内週") == 4).map(current.prop("チケット")).sum(),
  w5, monthItems.filter(current.prop("月内週") == 5).map(current.prop("チケット")).sum(),
  w6, monthItems.filter(current.prop("月内週") == 6).map(current.prop("チケット")).sum(),

  lines,
    [
      if(w1 > 0, "W1: " + w1, ""),
      if(w2 > 0, "W2: " + w2, ""),
      if(w3 > 0, "W3: " + w3, ""),
      if(w4 > 0, "W4: " + w4, ""),
      if(w5 > 0, "W5: " + w5, ""),
      if(w6 > 0, "W6: " + w6, "")
    ].filter(current != ""),

  join(lines, "\n")
)
```

**6月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 6 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**数式 1**
```notion-formula
lets(
  outcome, prop("中間DB").at(0).prop("支出一覧"),
  ym, formatDate(now(), "YYYY-MM"),

  // “今週”を月内週で判定（now() の月内週を計算）
  womNow,
    ceil(
      (
        date(now())
        + day(dateSubtract(now(), date(now()) - 1, "days"))
        - 1
      ) / 7
    ),

  monthItems,
    outcome.filter(
      formatDate(current.prop("日付"), "YYYY-MM") == ym
      and current.prop("カテゴリー") == prop("名前")
    ),

  spentThisWeek,
    monthItems
      .filter(current.prop("月内週") == womNow)
      .map(current.prop("チケット"))
      .sum(),

  prop("週予算") - spentThisWeek
)
```

**集計テーブル**
```notion-formula
lets(
  outcome, prop("中間DB").at(0).prop("支出一覧"),
  y, format(prop("年")),
  m, prop("月"),
  budget, if(empty(prop("予算金額")), 0, prop("予算金額")),

  ym, y + "-" + if(m < 10, "0" + format(m), format(m)),
  febYm, y + "-02",

  monthItems,
    outcome.filter(
      formatDate(current.prop("日付"), "YYYY-MM") == ym
      and current.prop("カテゴリー") == prop("名前")
    ),

  febItems,
    if(
      m == 1,
      outcome.filter(
        formatDate(current.prop("日付"), "YYYY-MM") == febYm
        and current.prop("カテゴリー") == prop("名前")
      ),
      []
    ),

  w1, monthItems.filter(current.prop("月内週") == 1).map(current.prop("支出")).sum(),
  w2, monthItems.filter(current.prop("月内週") == 2).map(current.prop("支出")).sum(),
  w3, monthItems.filter(current.prop("月内週") == 3).map(current.prop("支出")).sum(),
  w4, monthItems.filter(current.prop("月内週") == 4).map(current.prop("支出")).sum(),
  w5, monthItems.filter(current.prop("月内週") == 5).map(current.prop("支出")).sum(),
  w6, monthItems.filter(current.prop("月内週") == 6).map(current.prop("支出")).sum(),

  febW1, if(m == 1, febItems.filter(current.prop("月内週") == 1).map(current.prop("支出")).sum(), 0),

  w4Adj, if(m == 1 and w6 == 0 and w5 == 0, w4 + febW1, w4),
  w5Adj, if(m == 1 and w6 == 0, w5 + febW1, w5),
  w6Adj, if(m == 1 and w6 > 0, w6 + febW1, w6),

  lastWeek, if(w6 > 0, 6, if(w5 > 0, 5, if(w4 > 0, 4, 3))),

  r1, budget - w1,
  r2, budget - w2,
  r3, budget - w3,
  r4, budget - w4Adj,
  r5, budget - w5Adj,
  r6, budget - w6Adj,

  lines, [
    if(lastWeek >= 1, "W1: " + format(r1) + "円", ""),
    if(lastWeek >= 2, "W2: " + format(r2) + "円", ""),
    if(lastWeek >= 3, "W3: " + format(r3) + "円", ""),
    if(lastWeek >= 4, "W4: " + format(r4) + "円", ""),
    if(lastWeek >= 5, "W5: " + format(r5) + "円", ""),
    if(lastWeek >= 6, "W6: " + format(r6) + "円", "")
  ].filter(current != ""),

  if(empty(prop("年")) or empty(prop("月")), "", join(lines, "\n"))
)
```

**12月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(and(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 12, current.prop("カテゴリー") == prop("名前"))),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**11月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 11 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**合計**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYY") == prop("年") and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**4月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 4 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**5月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 5 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**2月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 2 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**3月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 3 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**9月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 9 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**7月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 7 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**1月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 1 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

**10月**
```notion-formula
lets(
	
	/* 中間DBから全ての支出データを取得 */
	outcome, prop("中間DB").at(0).prop("支出一覧"),
	
	/* 年月カテゴリー単位でデータをフィルター */
	total, outcome.filter(formatDate(current.prop("日付"), "YYYYM") == prop("年") + 10 and current.prop("カテゴリー") == prop("名前")),
	
	/* 支出を合計 */
	price, total.map(current.prop("支出")),
	price.sum()
)
```

## 注意事項
- `カテゴリー別集計グラフ` はAPIからアクセス不可（権限未共有の可能性）。必要なら統合に共有する。
- `月`（数値 1-12）を追加し、`年` と `月` を指定して週次計算する。1月は最終週に2月1週目の支出を合算する。
- リレーション参照を含む式はNotion APIが弾く場合があるため、式の貼り付けはNotion UIで実施する。
- CODEX_VER.1 では `グラフの幅` を `予算金額` に統一済み（集計テーブルは `予算金額` を参照する）。
- プロパティ名を変更すると式の参照先が崩れる。変更時は数式を更新する。
