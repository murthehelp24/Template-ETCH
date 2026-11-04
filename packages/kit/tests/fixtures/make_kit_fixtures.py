"""Expected values for tests/kit.test.ts, made by _build/kit.py and _build/icons.py themselves.

    python3 packages/kit/tests/fixtures/make_kit_fixtures.py   # writes kit.json next to this file

constants: every shared value of kit.py · calls: [name, args, result] for every helper function."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "_build"))
import kit as K  # noqa: E402
from icons import ICONS  # noqa: E402

TS = "2026-01-01T00:00:00.000Z"
NAMES = ["COLORS_CSS", "COLORS", "BASE", "SEC", "CON", "HEADING_STYLES", "BAND_STYLES", "SOCIAL_STYLES", "SOCIALS",
         "SOCIAL_PROPS", "CARD_STYLES", "MEDIA_STYLES", "BUTTONS_STYLES", "CHECKS_STYLES"]
constants = {n: getattr(K, n) for n in NAMES}
constants["SOCIALS"] = [list(s) for s in K.SOCIALS]
calls = []


def call(name, *args, **kw):
    calls.append([name, list(args), kw, getattr(K, name)(*args, **kw)])


call("icon", "star")
call("heading", "Eyebrow", "Title")
call("heading", "Eyebrow", "Title", "Intro")
call("heading", None, "Only a title", None, "h1")
call("heading", "E", "T", "I", center=True)
call("heading", "E", "T", tag="h3", center=True)
call("social_link", "LINE", "{props.lineUrl}", "line", "LINE")
call("social_link", "Share", "https://x.com/", "x", "X", False)
call("social_list")
call("social_list", "Follow us")
call("card", "item")
call("card", "post", "h3")
call("media_img")
call("media_img", "Photo", True)
call("buttons", "Learn more", "/about/", "Contact us", "/contact/")
call("checks", ["One", "Two"])

b = K.el("Box", "div", {"class": "main-heading"}, ["mn-heading"])
p = K.kit_payload(b, K.HEADING_STYLES)
p["timestamp"] = TS
json.dump({"timestamp": TS, "icons": ICONS, "constants": constants, "calls": calls,
           "kit_payload": {"args": [b, K.HEADING_STYLES], "result": p}},
          open(os.path.join(HERE, "kit.json"), "w"), ensure_ascii=False, indent=1)
print("ok", len(constants), "constants,", len(calls), "calls,", len(ICONS), "icons")
