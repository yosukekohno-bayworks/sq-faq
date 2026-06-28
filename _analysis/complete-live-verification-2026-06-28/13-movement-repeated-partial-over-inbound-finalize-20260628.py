#!/usr/bin/env python3
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/kounoyousuke/App Building/SQ/faq")
SCRIPT = ROOT / "_analysis" / "complete-live-verification-2026-06-28" / "13-movement-repeated-partial-over-inbound-20260628.py"

spec = importlib.util.spec_from_file_location("movement_repeat", SCRIPT)
movement_repeat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(movement_repeat)


def main():
    payload = json.loads(movement_repeat.OUT_JSON.read_text())
    inbound_route = payload.get("inboundRoute")
    movement_route = payload.get("steps", {}).get("createMovement", {}).get("route")
    if not inbound_route or not movement_route:
        raise RuntimeError("inboundRoute or movement route missing in evidence JSON")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(movement_repeat.CDP)
        page = browser.contexts[0].new_page()
        page.set_default_timeout(25000)
        try:
            payload.setdefault("steps", {})["manualCompleteInboundFinalRetry"] = movement_repeat.manual_complete_inbound(page, inbound_route)
            payload["steps"]["manualCompleteInbound"] = payload["steps"]["manualCompleteInboundFinalRetry"]
            payload["steps"]["movementAfterManualComplete"] = movement_repeat.inspect_movement(page, movement_route, "after_manual_complete_retry")
            payload["finalizedAt"] = datetime.now(timezone.utc).isoformat()
        finally:
            page.close()
            browser.close()

    payload["facts"] = movement_repeat.extract_facts(payload)
    movement_repeat.save_payload(payload)
    movement_repeat.write_md(payload)
    print(
        json.dumps(
            {
                "json": str(movement_repeat.OUT_JSON),
                "md": str(movement_repeat.OUT_MD),
                "finalizedAt": payload.get("finalizedAt"),
                "facts": payload.get("facts"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
