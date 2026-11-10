import pytest
from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry


inputs = st.one_of(st.text(), st.none(), st.integers(), st.floats(),
                   st.lists(st.integers()), st.dictionaries(st.text(), st.integers()))


@given(inputs)
def test_validate_blood_type_no_crash(s):
    try:
        result = validate_blood_type(s)
    except Exception as e:
        pytest.fail(f"Blood type crashed on {s!r}: {type(e).__name__}", pytrace=False)
    assert isinstance(result, str)


@given(inputs)
def test_calculate_pulse_pressure_safe(s):
    try:
        result = calculate_pulse_pressure(s)
    except Exception as e:
        pytest.fail(f"BP calculation crashed on {s!r}: {type(e).__name__}", pytrace=False)
    assert isinstance(result, str)


@given(inputs)
def test_parse_donor_registry_safe(s):
    try:
        result = parse_donor_registry(s)
    except Exception as e:
        pytest.fail(f"Registry crashed on {s!r}: {type(e).__name__}", pytrace=False)
    assert isinstance(result, str)


@given(st.sampled_from(["A", "B", "AB", "O"]), st.sampled_from(["+", "-"]),
       st.booleans(), st.sampled_from(["", " ", "\t"]))
def test_valid_blood_types(antigen, rh, lowercase, padding):
    code = antigen.lower() if lowercase else antigen
    expected = antigen + (" Positive" if rh == "+" else " Negative")
    assert validate_blood_type(padding + code + rh + padding) == expected


@given(st.integers(min_value=1, max_value=200),
       st.integers(min_value=1, max_value=200))
def test_valid_pulse_pressure(diastolic, difference):
    systolic = diastolic + difference
    expected = f"Diff: {difference}, Ratio: {round(systolic / diastolic, 2)}"
    assert calculate_pulse_pressure(f" {systolic} / {diastolic} ") == expected


@given(st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=1, max_size=15),
       st.sampled_from([49.9, 50.0, 65.0, 90.0]),
       st.sampled_from([12.4, 12.5, 14.0, 18.0]))
def test_valid_donor_records(donor_id, weight, hb):
    status = "Eligible" if weight >= 50 and hb >= 12.5 else "Deferred"
    record = f" {donor_id} |{weight}|{hb}"
    assert parse_donor_registry(record) == f"Donor {donor_id}: {status}"


@given(st.sampled_from(["", " ", "A", "A?", "X+", "+", "AB++", "A B+", None, 12]))
def test_invalid_blood_types(s):
    assert validate_blood_type(s) == "Invalid blood type"


@given(st.sampled_from(["", "120", "120/0", "0/80", "80/120", "120/-80",
                       "120/80/60", "one/80", "120.5/80", None, 120]))
def test_invalid_pulse_pressure(s):
    assert calculate_pulse_pressure(s) == "Invalid blood pressure"


@given(st.sampled_from(["", "D1", "D1|65", "D1|65|14|extra", " |65|14",
                       "D1|nan|14", "D1|inf|14", "D1|65|nan", "D1|65|inf",
                       "D1|-65|14", "D1|65|0", "D1|heavy|14", None, 12]))
def test_invalid_donor_records(s):
    assert parse_donor_registry(s) == "Invalid donor record"
