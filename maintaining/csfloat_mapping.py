import json
import urllib.request

SKINS_URL = (
    "https://raw.githubusercontent.com/ByMykel/CSGO-API"
    "/main/public/api/en/skins.json"
)
OUTPUT_PATH = "data/csfloat_mapping.json"


def fetch_raw() -> list[dict]:
    print(f"Fetching {SKINS_URL}")
    with urllib.request.urlopen(SKINS_URL, timeout=60) as resp:
        return json.loads(resp.read().decode())

def build_mapping(skins: list[dict]) -> dict:
    paint_index: dict[int, dict] = {}

    for skin in skins:
        p_index = skin.get("paint_index")
        if p_index is None:
            continue

        weapon = skin.get("weapon") or {}
        weapon_type = weapon.get("id")

        pattern = skin.get("pattern") or {}
        finish_name = pattern.get("name")

        if weapon_type and finish_name:
            paint_index[int(p_index)] = {
                "weapon_type": weapon_type,
                "finish_name": finish_name,
            }

    return {"paint_index": dict(sorted(paint_index.items()))}

def save(mapping: dict, path: str = OUTPUT_PATH) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4, ensure_ascii=False)
    print(f"Saved: {path}")
    print(f"  paint_index entries: {len(mapping['paint_index'])}")

if __name__ == "__main__":
    raw = fetch_raw()
    mapping = build_mapping(raw)
    save(mapping)