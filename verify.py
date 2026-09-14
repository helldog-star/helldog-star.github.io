#!/usr/bin/env python3
"""验证正式版：内容正确性 + 关键交互 + 截图。"""
from __future__ import annotations

import pathlib

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "_shots"
OUT.mkdir(exist_ok=True)
BASE = "http://127.0.0.1:8013"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1180, "height": 1000}, device_scale_factor=1)
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(300)

    print("=== 1. 论文列表（真实作者） ===")
    pubs = pg.eval_on_selector_all(
        ".pub",
        """els => els.map(e => ({
            venue: e.querySelector('.venue').innerText.trim(),
            role: e.querySelector('.role').innerText.trim(),
            selfBold: !!e.querySelector('.pub-meta strong'),
            authorsHead: e.querySelector('.pub-meta').innerText.replace(/\\s+/g,' ').slice(0, 78)
        }))""",
    )
    for i, x in enumerate(pubs, 1):
        mark = "✓" if x["selfBold"] else "✗"
        print(f"  {i}. [{x['venue']:22s}] {x['role']:5s} 自己加粗:{mark}  {x['authorsHead']}")

    print(f"\n  共 {len(pubs)} 篇；自己名字被加粗的: {sum(1 for x in pubs if x['selfBold'])}/{len(pubs)}")

    print("\n=== 2. 项目卡片（GitHub 真实数据） ===")
    projs = pg.eval_on_selector_all(
        ".project",
        """els => els.map(e => ({
            name: e.querySelector('h3').innerText.trim(),
            meta: e.querySelector('.stars').innerText.trim(),
            href: e.querySelector('h3 a').getAttribute('href')
        }))""",
    )
    for x in projs:
        print(f"  {x['name']:12s} {x['meta']:18s} {x['href']}")

    print("\n=== 3. 链接与资源可达性 ===")
    for label, url in [
        ("CV (PDF)", "/cv.pdf"),
        ("favicon", "/favicon.svg"),
        ("portrait", "/portrait.jpg"),
        ("随笔列表", "/writing/"),
        ("随笔详情", "/writing/why-quantify-forgetting/"),
    ]:
        r = pg.request.get(BASE + url)
        print(f"  {label:12s} {url:38s} HTTP {r.status}")

    print("\n=== 4. 筛选交互 ===")
    for f, expect in (("all", 12), ("first-author", 5), ("co-author", 7), ("review", 1)):
        pg.click(f'.chip[data-filter="{f}"]')
        pg.wait_for_timeout(120)
        vis = pg.eval_on_selector_all(".pub", "els => els.filter(e => e.style.display !== 'none').length")
        ok = "✓" if vis == expect else "✗"
        print(f"  {f:14s} 可见 {vis} 篇（预期 {expect}）{ok}")
    pg.click('.chip[data-filter="all"]')

    print("\n=== 5. 截图 ===")
    for name, path in (("site-home", "/"), ("site-writing", "/writing/"),
                       ("site-post", "/writing/why-quantify-forgetting/")):
        pg.goto(BASE + path, wait_until="networkidle")
        pg.wait_for_timeout(200)
        dest = OUT / f"{name}.png"
        pg.screenshot(path=str(dest), full_page=True)
        print(f"  {dest.name}")

    b.close()
print(f"\n输出目录: {OUT}")
