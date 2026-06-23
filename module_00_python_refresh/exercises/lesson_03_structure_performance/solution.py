from timeit import timeit


def deduplicate_with_list(ids: list[int]) -> list[int]:
    """
    Remove duplicates from a list of IDs using only list operations.

    This is the naive approach: check if each ID exists in the result list
    before adding it. Time complexity: O(n²)
    """
    result = []
    for id_val in ids:
        if id_val not in result:  # O(n) check for each item
            result.append(id_val)
    return result


def deduplicate_with_set(ids: list[int]) -> list[int]:
    """
    Remove duplicates from a list of IDs using set.

    This is the efficient approach: convert to set and back to list.
    Time complexity: O(n)
    """
    return list(set(ids))


if __name__ == "__main__":
    # Create test data: 100K IDs with many duplicates
    test_ids = list(range(50_000)) * 2  # 100K items, lots of duplication

    # Verify both approaches give the same result
    result_list = deduplicate_with_list(test_ids)
    result_set = deduplicate_with_set(test_ids)

    print(f"List approach result count: {len(result_list)}")
    print(f"Set approach result count: {len(result_set)}")
    assert len(result_list) == len(result_set), "Results should have same length"
    assert set(result_list) == set(result_set), "Results should have same elements"

    # Measure performance
    time_list = timeit(lambda: deduplicate_with_list(test_ids), number=10)
    time_set = timeit(lambda: deduplicate_with_set(test_ids), number=10)

    print(f"\nPerformance (deduplicating 100K IDs):")
    print(f"List approach: {time_list:.4f}s")
    print(f"Set approach: {time_set:.4f}s")
    print(f"Set is ~{time_list/time_set:.0f}x faster")
