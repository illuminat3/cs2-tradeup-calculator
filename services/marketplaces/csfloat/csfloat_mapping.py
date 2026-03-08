import json
from dtos.counter_strike_enums import weapon_type
from dtos.skin_info import skin


class csfloat_mapping:
    def __init__(self, csfloat_mapping_filepath: str):
        self.csfloat_mapping_filepath = csfloat_mapping_filepath
        self.load_mapping()

    def load_mapping(self) -> dict[str, dict]:
        with open(self.csfloat_mapping_filepath, "r", encoding="utf-8") as f:
            self._mapping = json.load(f)
        return self._mapping

    def get_paint_index(self, s: skin) -> str | None:
        paint_index_map: dict[str, dict] = self._mapping.get("paint_index", {})
        for index, entry in paint_index_map.items():
            if (
                entry["weapon_type"] == s.weapon_type.value
                and entry["finish_name"].lower() == s.finish_name.lower()
            ):
                return index
        return None