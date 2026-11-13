"""Start owned local processes, verify web -> API, and optionally inspect Chromium.

Run after npm run build: uv run --locked python scripts/smoke_foundation.py
Browser: uv run --with playwright python scripts/smoke_foundation.py --browser
Requires free ports 8108 (API) and 3108 (web); never stops another project's servers.
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


def wait_for(url: str, process: subprocess.Popen) -> bytes:
    deadline = time.monotonic() + 40
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Owned server exited before readiness: {url}")
        try:
            with urlopen(url, timeout=2) as response:
                return response.read()
        except (URLError, TimeoutError):
            time.sleep(0.3)
    raise RuntimeError(f"Readiness timeout: {url}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--browser-channel", choices=["chrome", "msedge"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for port in (8108, 3108):
        with socket.socket() as connection:
            connection.bind(("127.0.0.1", port))
    next_bin = subprocess.check_output(
        ["node", "-p", "require.resolve('next/dist/bin/next', {paths: ['./apps/web']})"],
        cwd=root,
        text=True,
    ).strip()
    env = os.environ | {"NEXT_TELEMETRY_DISABLED": "1"}
    artifacts = root / ".local" / "smoke"
    artifacts.mkdir(parents=True, exist_ok=True)
    processes = []
    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    with (artifacts / "servers.log").open("w", encoding="utf-8") as log:
        try:
            api = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "agu_api.main:create_app",
                    "--factory",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8108",
                ],
                cwd=root,
                env=env,
                stdout=log,
                stderr=log,
                creationflags=flags,
            )
            processes.append(api)
            assert json.loads(wait_for("http://127.0.0.1:8108/api/v1/health", api)) == {
                "status": "ok"
            }
            web = subprocess.Popen(
                ["node", next_bin, "start", "--hostname", "127.0.0.1", "--port", "3108"],
                cwd=root / "apps/web",
                env=env,
                stdout=log,
                stderr=log,
                creationflags=flags,
            )
            processes.append(web)
            html = wait_for("http://127.0.0.1:3108", web).decode("utf-8")
            assert 'lang="vi"' in html and "Development" in html
            assert "tuyensinh.agu.edu.vn" in html
            assert json.loads(wait_for("http://127.0.0.1:3108/api/v1/health", web)) == {
                "status": "ok"
            }
            if args.browser:
                from playwright.sync_api import sync_playwright

                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(channel=args.browser_channel)
                    page = browser.new_page()
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    for width, height in ((375, 812), (812, 375), (1440, 900)):
                        page.set_viewport_size({"width": width, "height": height})
                        page.emulate_media(reduced_motion="reduce")
                        page.goto("http://127.0.0.1:3108", wait_until="networkidle")
                        assert page.locator("h1").count() == 1
                        assert page.locator("input, textarea, form").count() == 0
                        assert page.evaluate(
                            "document.documentElement.scrollWidth <= window.innerWidth"
                        )
                        page.keyboard.press("Tab")
                        assert page.locator(".skip-link").evaluate(
                            "element => element === document.activeElement"
                        )
                        page.screenshot(path=str(artifacts / f"shell-{width}.png"), full_page=True)
                    assert not errors, errors
                    browser.close()
            print("PASS: local web -> API health, shell; no provider or knowledge-serving calls")
        finally:
            for process in reversed(processes):
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__ == "__main__":
    main()
