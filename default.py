import sys
import urllib.parse

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")


def log(message: str, level: int = xbmc.LOGINFO) -> None:
    xbmc.log(f"[{ADDON_ID}] {message}", level)


def _normalize_action(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def parse_action(argv: list[str]) -> str:
    """
    Supports these invocation styles:
    - Addons.ExecuteAddon params: ["on"]
    - Addons.ExecuteAddon params: ["action=on"]
    - Addons.ExecuteAddon params: ["--action=on"]
    """
    if not argv:
        return "on"

    for raw in argv:
        text = raw.strip()
        if not text:
            continue

        if text.startswith("--action="):
            return _normalize_action(text.split("=", 1)[1])

        if "=" in text:
            parsed = urllib.parse.parse_qs(text, keep_blank_values=False)
            if "action" in parsed and parsed["action"]:
                return _normalize_action(parsed["action"][0])

        return _normalize_action(text)

    return "on"


def run(action: str) -> int:
    on_actions = {"on", "tv-on", "wake", "active", "activate", "activate-source"}
    off_actions = {"off", "tv-off", "standby", "sleep"}

    if action in on_actions:
        log("Sending CEC activate source command")
        xbmc.executebuiltin("CECActivateSource")
        xbmc.executebuiltin("Notification(HDMI CEC,Power ON command sent,3000)")
        return 0

    if action in off_actions:
        log("Sending CEC standby command")
        xbmc.executebuiltin("CECStandby")
        xbmc.executebuiltin("Notification(HDMI CEC,Power OFF command sent,3000)")
        return 0

    log(
        f"Unsupported action '{action}'. Supported actions: on, off",
        xbmc.LOGERROR,
    )
    xbmc.executebuiltin("Notification(HDMI CEC,Invalid action. Use on/off,4000)")
    return 1


def main() -> None:
    args = sys.argv[1:]
    action = parse_action(args)
    log(f"Received action: {action}")
    exit_code = run(action)
    if exit_code != 0:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
