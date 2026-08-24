import i164_fixed_benchmark_core as i164


def test_fixed_benchmark_digest_is_stable():
    assert i164.BENCHMARK_ID == "python-local-fixed-json-transform-v1"
    assert i164.EXPECTED_OUTPUT_DIGEST == "30b102b8e451d052387927e05e57ee4e5e7e046b0c3e15869a1684a9d52fa419"
    assert i164.benchmark_transform() == i164.EXPECTED_OUTPUT


def test_transform_normalizes_order_and_rejects_invalid_rows():
    payload = {
        "schema_version": 1,
        "records": [
            {"id": "b", "value": 2},
            {"id": "a", "value": 1},
        ],
    }
    result = i164.benchmark_transform(payload)
    assert [row["id"] for row in result["records"]] == ["a", "b"]
    assert result["sum"] == 3

    for bad in (
        {"schema_version": 2, "records": [{"id": "a", "value": 1}]},
        {"schema_version": 1, "records": []},
        {"schema_version": 1, "records": [{"id": "a", "value": True}]},
        {"schema_version": 1, "records": [{"id": "a", "value": 1}, {"id": "a", "value": 2}]},
    ):
        try:
            i164.benchmark_transform(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")
