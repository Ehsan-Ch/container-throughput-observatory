import json
from analysis import ROOT, experiment


def render():
    source = (ROOT / "explorer.html").read_text(encoding="utf-8")
    data = json.dumps(experiment(), separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")
    if source.count("<!-- REPORT -->") != 1:
        raise ValueError("Missing or repeated report placeholder")
    return source.replace("<!-- REPORT -->", data)


if __name__ == "__main__":
    (ROOT / "index.html").write_text(render(), encoding="utf-8", newline="\n")
