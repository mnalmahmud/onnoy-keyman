"""Generate data for Onnoy's custom web visualizer (not a typing engine)."""
import json
from ..hardware import BROWSER

def render(mapping):
    return json.dumps({
        "name":"Onnoy",
        "layers":["base","shift","altgr","shift_altgr"],
        "keys": {BROWSER[key]:list(vals) for key,vals in mapping.items()},
    },ensure_ascii=False,indent=2)+"\n"
