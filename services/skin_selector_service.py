from dtos.listing import listing

class skin_selector_service:
	def _adjusted_float(self, l: listing) -> float:
		float_range = l.skin.max_float - l.skin.min_float
		if float_range == 0:
			return 0.0
		return (l.skin.float_value - l.skin.min_float) / float_range

	def _max_group_float_sum(self, target_float: float, current_float_sum: float, current_count: int, count: int) -> float:
		return target_float * (current_count + count) - current_float_sum

	def _initial_selection(self, available_sorted_by_float: list[listing], count: int) -> list[listing]:
		return available_sorted_by_float[:count]

	def _find_swap_target(self, candidates_pool: list[listing]) -> listing:
		return max(candidates_pool, key=lambda l: l.price)

	def _try_swap(self, candidates_pool: list[listing], cheaper_candidate: listing, group_float_sum: float, max_float_sum: float) -> tuple[list[listing], float]:
		swap_target = self._find_swap_target(candidates_pool)

		if cheaper_candidate.price >= swap_target.price:
			return candidates_pool, group_float_sum

		new_float_sum = group_float_sum - self._adjusted_float(swap_target) + self._adjusted_float(cheaper_candidate)

		if new_float_sum <= max_float_sum:
			candidates_pool.remove(swap_target)
			candidates_pool.append(cheaper_candidate)
			return candidates_pool, new_float_sum

		return candidates_pool, group_float_sum

	def select_skins_for_tradeup(self, listings: dict[int, list[listing]], target_float: float) -> list[listing]:
		used_urls: set[str] = set()
		selected: list[listing] = []
		current_float_sum = 0.0
		current_count = 0

		sorted_groups = sorted(listings.items(), key=lambda kv: len(kv[1]) / kv[0] if kv[0] > 0 else float('inf'))

		for count, candidates in sorted_groups:
			available = [l for l in candidates if l.url not in used_urls]
			available_sorted_by_float = sorted(available, key=self._adjusted_float)

			if len(available_sorted_by_float) < count:
				raise ValueError(f"Not enough unique listings for count {count}")

			max_float_sum = self._max_group_float_sum(target_float, current_float_sum, current_count, count)
			candidates_pool = self._initial_selection(available_sorted_by_float, count)
			group_float_sum = sum(self._adjusted_float(l) for l in candidates_pool)

			if group_float_sum > max_float_sum:
				raise ValueError(f"Cannot satisfy float constraint for count {count}")

			remaining_pool = sorted(available_sorted_by_float[count:], key=lambda l: l.price)

			for cheaper_candidate in remaining_pool:
				if cheaper_candidate.price >= self._find_swap_target(candidates_pool).price:
					break
				candidates_pool, group_float_sum = self._try_swap(candidates_pool, cheaper_candidate, group_float_sum, max_float_sum)

			for l in candidates_pool:
				used_urls.add(l.url)
				selected.append(l)

			current_float_sum += group_float_sum
			current_count += count

		return selected