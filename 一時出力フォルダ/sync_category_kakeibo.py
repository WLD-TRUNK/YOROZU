import json
import math
from datetime import date, datetime, timedelta

import requests

# NOTE:
# This script writes computed values into page properties.
# If you operate purely with Notion formulas, do not run this file.

MCP_URL = "http://localhost:3000/mcp"
AUTH_TOKEN = "local-mcp-secret"

CATEGORY_DS = "2f2d8928-02b6-8186-8a24-000b2130c151"
SPEND_DS = "2f2d8928-02b6-81e4-bd59-000b982df8db"

# Category DB property IDs
P_NAME = "title"
P_YEAR = "hyQt"
P_MONTH = "elgH"
P_BUDGET_AMOUNT = "S%60rk"
P_BUDGET_TEXT = "D%5EC%3C"
P_TOTAL = "OZUb"
P_YEAR_CACHE = "Fhm%7C"

MONTH_IDS = {
    1: "rIBa",
    2: "bZkR",
    3: "gBbJ",
    4: "YrJ%7B",
    5: "Z%7Dnw",
    6: "DGf%3F",
    7: "oqc%5E",
    8: "%40%3C%5EN",
    9: "jrSs",
    10: "rS~%60",
    11: "HppF",
    12: "HnLk",
}

# Spend DB property IDs
SP_DATE = "%5CFpc"
SP_CATEGORY = "yFUG"
SP_AMOUNT = "xlVt"


class NotionMCP:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {AUTH_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            }
        )

    def _post(self, payload: dict, timeout: int = 120) -> dict:
        resp = self.session.post(MCP_URL, json=payload, timeout=timeout)
        resp.raise_for_status()
        sid = resp.headers.get("mcp-session-id")
        if sid and "mcp-session-id" not in self.session.headers:
            self.session.headers["mcp-session-id"] = sid

        body = resp.text
        if "text/event-stream" in resp.headers.get("Content-Type", ""):
            data_lines = []
            for line in body.splitlines():
                if line.startswith("data: "):
                    data_lines.append(line[6:])
                elif line.strip() and not line.startswith("event:") and not line.startswith(":"):
                    data_lines.append(line)
            body = "\n".join(data_lines).strip()

        return json.loads(body, strict=False) if body else {}

    def init(self) -> None:
        self._post(
            {
                "jsonrpc": "2.0",
                "id": "init",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "sync-category-kakeibo", "version": "1.0"},
                },
            }
        )
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def call_tool(self, name: str, arguments: dict) -> dict:
        result = self._post(
            {
                "jsonrpc": "2.0",
                "id": "tool",
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        )
        content = result.get("result", {}).get("content", [])
        if content and content[0].get("type") == "text":
            return json.loads(content[0]["text"], strict=False)
        return result


def prop_by_id(props: dict, pid: str) -> dict:
    for value in props.values():
        if value.get("id") == pid:
            return value
    return {}


def parse_rollup_first_number(prop: dict) -> int | None:
    arr = (prop.get("rollup") or {}).get("array") or []
    if not arr:
        return None

    item = arr[0]
    if item.get("number") is not None:
        try:
            return int(item["number"])
        except Exception:
            pass

    select = item.get("select") or {}
    if select.get("name"):
        digits = "".join(ch for ch in str(select["name"]) if ch.isdigit())
        if digits:
            return int(digits)

    title = item.get("title") or []
    if title:
        text = "".join(t.get("plain_text", "") for t in title)
        digits = "".join(ch for ch in text if ch.isdigit())
        if digits:
            return int(digits)

    rich_text = item.get("rich_text") or []
    if rich_text:
        text = "".join(t.get("plain_text", "") for t in rich_text)
        digits = "".join(ch for ch in text if ch.isdigit())
        if digits:
            return int(digits)

    return None


def parse_title(prop: dict) -> str:
    return "".join(t.get("plain_text", "") for t in (prop.get("title") or []))


def week_index_sunday_start(d: date) -> int:
    month_start = d.replace(day=1)
    e = month_start.isoweekday()  # Mon=1 .. Sun=7 (same as Notion E)
    offset = 0 if e == 7 else e
    week0_start = month_start - timedelta(days=offset)
    return ((d - week0_start).days // 7) + 1


def week_count(year: int, month: int) -> int:
    month_start = date(year, month, 1)
    e = month_start.isoweekday()
    offset = 0 if e == 7 else e
    week0_start = month_start - timedelta(days=offset)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    month_end = next_month - timedelta(days=1)
    return ((month_end - week0_start).days // 7) + 1


def bar_width(used: int, budget: int, scale: int = 10) -> int:
    if budget <= 0:
        return 0
    ratio = used / budget
    if ratio <= 0:
        return 0
    if ratio >= 1:
        return scale
    return int(math.ceil(ratio * scale))


def main() -> None:
    mcp = NotionMCP()
    mcp.init()

    # Load all spend rows once.
    spend_rows = []
    cursor = None
    while True:
        args = {"data_source_id": SPEND_DS, "page_size": 100}
        if cursor:
            args["start_cursor"] = cursor
        data = mcp.call_tool("API-query-data-source", args)
        spend_rows.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    monthly_totals = {}  # (year, month, category) -> amount
    weekly_totals = {}  # (year, month, category, week) -> amount

    for row in spend_rows:
        props = row.get("properties", {})
        dprop = prop_by_id(props, SP_DATE)
        cprop = prop_by_id(props, SP_CATEGORY)
        aprop = prop_by_id(props, SP_AMOUNT)

        ds = (dprop.get("date") or {}).get("start")
        if not ds:
            continue
        d = datetime.strptime(ds[:10], "%Y-%m-%d").date()
        category = ((cprop.get("select") or {}).get("name")) or ""
        if not category:
            continue
        amount = int(aprop.get("number") or 0)

        mkey = (d.year, d.month, category)
        monthly_totals[mkey] = monthly_totals.get(mkey, 0) + amount

        wk = week_index_sunday_start(d)
        wkey = (d.year, d.month, category, wk)
        weekly_totals[wkey] = weekly_totals.get(wkey, 0) + amount

    # Update category rows.
    category_data = mcp.call_tool("API-query-data-source", {"data_source_id": CATEGORY_DS, "page_size": 100})
    rows = category_data.get("results", [])

    for row in rows:
        props = row["properties"]
        page_id = row["id"]
        category = parse_title(prop_by_id(props, P_NAME))
        year = parse_rollup_first_number(prop_by_id(props, P_YEAR))
        month = parse_rollup_first_number(prop_by_id(props, P_MONTH))
        budget_amount = int(prop_by_id(props, P_BUDGET_AMOUNT).get("number") or 0)

        month_values = {}
        if year:
            for m in range(1, 13):
                month_values[m] = int(monthly_totals.get((year, m, category), 0))
        else:
            for m in range(1, 13):
                month_values[m] = 0

        # "合計" is yearly total for the selected year/category.
        total = sum(month_values.values())
        budget_text = ""

        if year and month and 1 <= month <= 12:
            wk_count = week_count(year, month)
            w = {i: int(weekly_totals.get((year, month, category, i), 0)) for i in range(1, 7)}

            # January can include February week 1 in the final week bucket.
            if month == 1:
                feb_w1 = int(weekly_totals.get((year, 2, category, 1), 0))
                if wk_count == 4:
                    w[4] += feb_w1
                elif wk_count == 5:
                    w[5] += feb_w1
                elif wk_count == 6:
                    w[6] += feb_w1

            lines = []
            for i in range(1, wk_count + 1):
                used = w.get(i, 0)
                remain = budget_amount - used
                used_ticket = int(math.ceil(max(used, 0) / 500)) if used > 0 else 0
                remain_ticket = int(math.ceil(max(remain, 0) / 500)) if remain > 0 else 0
                bar = "█" * bar_width(used, budget_amount, 10)
                # Ticket block first, bar on the right.
                lines.append(f"W{i}  使用🎟️{used_ticket}  残🎟️{remain_ticket}  {bar}")

            budget_text = f"{year}{month:02d} / {wk_count}W\n" + "\n".join(lines)

        patch_props = {
            P_TOTAL: {"number": total},
            P_YEAR_CACHE: {"number": year if year else None},
            P_BUDGET_TEXT: {
                "rich_text": ([{"type": "text", "text": {"content": budget_text[:2000]}}] if budget_text else [])
            },
        }
        for m, pid in MONTH_IDS.items():
            patch_props[pid] = {"number": month_values[m]}

        mcp.call_tool("API-patch-page", {"page_id": page_id, "properties": patch_props})

        safe_category = category.encode("unicode_escape").decode("ascii")
        print(f"updated: {safe_category} (year={year}, month={month}, total={total})")


if __name__ == "__main__":
    main()
