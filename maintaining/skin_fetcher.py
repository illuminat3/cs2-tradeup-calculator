import json
import urllib.request
from dataclasses import dataclass
from typing import Optional
from dtos.skin_info import skin, rarity, collection, weapon_type, category

RARITY_MAP: dict[str, rarity] = {
	"rarity_common_weapon":     rarity.consumer,
	"rarity_uncommon_weapon":   rarity.industrial,
	"rarity_rare_weapon":       rarity.milspec,
	"rarity_mythical_weapon":   rarity.restricted,
	"rarity_legendary_weapon":  rarity.classified,
	"rarity_ancient_weapon":    rarity.covert,
	"rarity_contraband_weapon": rarity.gold,
}

COLLECTION_LOOKUP: dict[str, collection] = {
	c.value.lower(): c for c in collection
}

WEAPON_LOOKUP: dict[str, weapon_type] = {
	w.value: w for w in weapon_type
}

API_URL = (
	"https://raw.githubusercontent.com/ByMykel/CSGO-API"
	"/main/public/api/en/skins.json"
)

@dataclass
class ApiRef:
	id:   str
	name: str

	@classmethod
	def from_dict(cls, d: dict) -> "ApiRef":
		return cls(id=d.get("id", ""), name=d.get("name", ""))

@dataclass
class ApiCollection:
	id:    str
	name:  str
	image: str

	@classmethod
	def from_dict(cls, d: dict) -> "ApiCollection":
		return cls(
			id    = d.get("id", ""),
			name  = d.get("name", ""),
			image = d.get("image", ""),
		)

	@property
	def set_id(self) -> str:
		raw = self.id.removeprefix("collection-")
		return raw.replace("-", "_")

@dataclass
class ApiSkin:
	id:          str
	name:        str
	weapon:      ApiRef
	pattern:     ApiRef
	rarity:      ApiRef
	category:    ApiRef
	min_float:   float
	max_float:   float
	paint_index: int
	collections: list[ApiCollection]
	stattrak:    bool
	souvenir:    bool

	@classmethod
	def from_dict(cls, d: dict) -> "ApiSkin":
		return cls(
			id          = d.get("id", ""),
			name        = d.get("name", ""),
			weapon      = ApiRef.from_dict(d.get("weapon") or {}),
			pattern     = ApiRef.from_dict(d.get("pattern") or {}),
			rarity      = ApiRef.from_dict(d.get("rarity") or {}),
			category    = ApiRef.from_dict(d.get("category") or {}),
			min_float   = float(d.get("min_float") or 0.0),
			max_float   = float(d.get("max_float") or 1.0),
			paint_index = int(d.get("paint_index") or 0),
			collections = [ApiCollection.from_dict(c) for c in (d.get("collections") or [])],
			stattrak    = bool(d.get("stattrak", False)),
			souvenir    = bool(d.get("souvenir", False)),
		)

	def _resolve_category(self) -> category:
		if self.stattrak:
			return category.StatTrak
		if self.souvenir:
			return category.Souvenir
		return category.Normal

	def to_skin(self) -> Optional["skin"]:
		matched_weapon = WEAPON_LOOKUP.get(self.weapon.id)
		if matched_weapon is None:
			return None

		if "★" in self.name:
			matched_rarity = rarity.gold
		else:
			matched_rarity = RARITY_MAP.get(self.rarity.id)
			if matched_rarity is None:
				return None

		collection_name: Optional[str] = None
		if self.collections:
			set_id = self.collections[0].set_id.lower()
			matched_col = COLLECTION_LOOKUP.get(set_id)
			collection_name = matched_col.name if matched_col else set_id

		return skin(
			finish_name     = self.pattern.name,
			weapon_type     = matched_weapon,
			collection_name = collection_name,
			min_float       = self.min_float,
			max_float       = self.max_float,
			float_value     = 0.0,
			rarity          = matched_rarity,
			category        = self._resolve_category(),
			paint_index     = self.paint_index,
		)

def fetch_raw() -> list[ApiSkin]:
	print(f"Fetching {API_URL}")
	with urllib.request.urlopen(API_URL, timeout=60) as resp:
		raw: list[dict] = json.loads(resp.read().decode())
	return [ApiSkin.from_dict(d) for d in raw]

def transform(api_skins: list[ApiSkin]) -> list[dict]:
	seen:    set[str] = set()
	results: list[dict] = []
	skipped_rarity = 0
	skipped_weapon = 0
	skipped_dupe   = 0

	for api_skin in api_skins:
		dedup_key = f"{api_skin.weapon.id}::{api_skin.pattern.id}"
		if dedup_key in seen:
			skipped_dupe += 1
			continue

		s = api_skin.to_skin()

		if s is None:
			if WEAPON_LOOKUP.get(api_skin.weapon.id) is None:
				skipped_weapon += 1
			else:
				skipped_rarity += 1
			continue

		seen.add(dedup_key)

		for c in category:
			entry = {
				"finish_name":     s.finish_name,
				"weapon_type":     s.weapon_type.value,
				"collection_name": s.collection_name.value if isinstance(s.collection_name, collection) else s.collection_name,
				"min_float":       s.min_float,
				"max_float":       s.max_float,
				"float_value":     s.float_value,
				"rarity":          s.rarity.value,
				"skin_name":       s.skin_name,
				"category":        c.name,
				"paint_index":     s.paint_index,
			}
			results.append(entry)

	print(f"Found {len(results)} skins")
	return results

def save(skins: list[dict], path: str = "data/skins.json") -> None:
	with open(path, "w", encoding="utf-8") as f:
		json.dump(skins, f, indent=4, ensure_ascii=False)
	print(f"Saved: {path}")

if __name__ == "__main__":
	api_skins = fetch_raw()
	skins     = transform(api_skins)
	save(skins, "data/skins.json")
