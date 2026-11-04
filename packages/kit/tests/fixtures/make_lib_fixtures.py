"""Expected values for tests/lib.test.ts, made by the Python kit (_build/lib_etch.py) itself.

    python3 packages/kit/tests/fixtures/make_lib_fixtures.py   # writes lib.json next to this file

Each case is [name, args, result]; lib.test.ts calls the TypeScript function of the same name with the same
args and expects the same result. Run it again only when lib_etch.py changes on purpose."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "_build"))
import lib_etch as L  # noqa: E402

TS = "2026-01-01T00:00:00.000Z"
cases = []


def case(name, *args):
    cases.append([name, list(args), getattr(L, name)(*args)])


t = L.text("Hello")
case("text", "Hello")
case("text", "สวัสดี {props.title}")
case("block", "etch/slot-content", {"name": "default"})
case("block", "etch/slot-content", {"name": "default"}, [t, t])
case("el", "Box", "div")
case("el", "Box", "div", {"class": "a b"}, ["mn-a"], [t])
case("el", "Box", "div", {"class": "a"}, [], [t, t, t])
case("img", "Image", {"class": "x", "mediaId": ""}, ["mn-x"])
case("svg", "Icon", "data:image/svg+xml;base64,AAA")
case("svg", "Icon", "data:image/svg+xml;base64,AAA", "main-icon", ["mn-icon"])
case("svg", "Icon", "data:image/svg+xml;base64,AAA", "", [])
case("cond", "If x", "props.x", t)
case("cond", "If x", "props.x", [t, t])
case("loop", "Posts", "item", [t])
case("loop", "Posts", "item", [t], "mainRelatedPosts", "this.related", {"count": "3"})
case("slot_placeholder", "default")
case("prop", "Title", "title", "Hello")
case("prop", "Title", "title", "Hello", "Shown at the top")
case("prop", "Count", "count", 3, "", "number")
case("data_uri", '<svg viewBox="0 0 24 24"><path d="M0 0h24"/></svg>')
case("data_uri", "<svg>ไทย</svg>")
for css in ["inline-size: 1.4rem;", "padding: .5rem 2rem 0.8rem;", "gap: 12.5rem; x: 1e-5rem", "a: 0rem; b: 10rem;",
            "keep: var(--space-xs-rem); x2rem; .4rem-x; 3remx; -2rem", "เว้น 2rem ไทย2rem", "none"]:
    case("portable", css)
case("style", ".a", "margin: 1.2rem;")
case("style", ":where(:root)", "--x: 1rem;", "custom")

used = L.el("Box", "div", {"class": "a"}, ["mn-a"], [L.el("In", "span", {}, ["mn-b"])])
styles = {"mn-a": L.style(".a", "x: 1rem;"), "mn-b": L.style(".b", ""), "mn-unused": L.style(".c", "")}
comp = {"990001": {"key": "K", "blocks": [L.el("C", "div", {}, ["mn-b"])], "properties": []}}
payload_cases = []
for args in [(used, styles), (used, styles, comp), (used, styles, None, {"loopA": {"key": "loopA", "config": {}}}),
             (used, styles, {}, {})]:
    p = L.payload(*args)
    p["timestamp"] = TS
    payload_cases.append([list(args), p, json.dumps(p, ensure_ascii=False, separators=(",", ":"))])

json.dump({"timestamp": TS, "cases": cases, "payload": payload_cases},
          open(os.path.join(HERE, "lib.json"), "w"), ensure_ascii=False, indent=1)
print("ok", len(cases), "cases,", len(payload_cases), "payloads")
