import sys
import urllib.parse
from typing import List, Optional

import xbmc

ADDON_ID = "script.hdmi.cec.power"
LOG_MARKER = "HDMI-CEC-POWER"


def log(message: str, level: int = xbmc.LOGINFO) -> None:
    xbmc.log(f"[{LOG_MARKER}][{ADDON_ID}] {message}", level)


def log_event(event: str, level: int = xbmc.LOGINFO, **fields: object) -> None:
    details = " ".join(f"{key}={value}" for key, value in fields.items())
    if details:
        log(f"event={event} {details}", level)
    else:
        log(f"event={event}", level)


def _normalize_action(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def parse_action(argv: List[str]) -> Optional[str]:
    """
    Parses the action from sys.argv[1:]. Supports:
      - positional:   ["on"]
      - key=value:    ["action=on"]
      - flag:         ["--action=on"]
      - query string: ["?action=on"]
    Returns None if no recognizable action is found.
    """
    for raw in argv:
        text = raw.strip().lstrip("?")
        if not text:
            continue

        if text.startswith("--action="):
            return _normalize_action(text.split("=", 1)[1])

        if "=" in text:
            parsed = urllib.parse.parse_qs(text, keep_blank_values=False)
            if "action" in parsed and parsed["action"]:
                return _normalize_action(parsed["action"][0])
            continue

        return _normalize_action(text)

    return None


def run(action: str) -> int:
    on_actions = {"on", "tv-on", "wake", "active", "activate", "activate-source"}
    off_actions = {"off", "tv-off", "standby", "sleep"}

    if action in on_actions:
        log_event("cec_command", action=action, command="CECActivateSource")
        xbmc.executebuiltin("CECActivateSource")
        xbmc.executebuiltin("Notification(HDMI CEC,Power ON command sent,3000)")
        return 0

    if action in off_actions:
        log_event("cec_command", action=action, command="CECStandby")
        xbmc.executebuiltin("CECStandby")
        xbmc.executebuiltin("Notification(HDMI CEC,Power OFF command sent,3000)")
        return 0

    log_event("invalid_action", xbmc.LOGERROR, action=action, supported="on,off")
    xbmc.executebuiltin("Notification(HDMI CEC,Invalid action. Use on/off,4000)")
    return 1


def main() -> None:
    log_event("startup", argv="|".join(sys.argv))
    action = parse_action(sys.argv[1:])
    if action is None:
        log_event("missing_action", xbmc.LOGERROR)
        xbmc.executebuiltin("Notification(HDMI CEC,No action provided. Use on or off,4000)")
        raise SystemExit(1)
    log_event("parsed_action", action=action)
    exit_code = run(action)
    log_event("exit", code=exit_code)
    if exit_code != 0:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
