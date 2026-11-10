import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def test_single_accepted_donor():
    cohorts = [{"clinic_registered": True,
                "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_list():
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort(None, 450)


def test_unregistered_clinic():
    cohorts = [{"clinic_registered": False,
                "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
                "fast_track": True}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 0, "status": "ZERO_YIELD"}


def test_underage_and_underweight_donors():
    cohorts = [{"clinic_registered": True, "donors": [
        {"age": 16, "weight_kg": 60, "hb": 14.0},
        {"age": 25, "weight_kg": 49, "hb": 14.0}]}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_low_hb():
    cohorts = [{"clinic_registered": True, "type": "high_altitude", "donors": [
        {"age": 25, "weight_kg": 65, "hb": 14.0},
        {"age": 25, "weight_kg": 65, "hb": 12.0},
        {"age": 25, "weight_kg": 65, "hb": 15.0}]}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hb_then_accepted_donor():
    cohorts = [{"clinic_registered": True, "donors": [
        {"age": 25, "weight_kg": 65, "hb": 18.1},
        {"age": 25, "weight_kg": 65, "hb": 14.0}]}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 450, "status": "ACCEPTED"}


def test_fast_track_cohort():
    cohorts = [{"clinic_registered": True, "fast_track": True,
                "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]}]
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": 500, "status": "ACCEPTED"}


def test_two_consecutive_low_rpms():
    assert verify_storage_centrifuge([[3200, 2900, 2800]]) == "ABORT_SPIN"


def test_stable_runs_with_recovery():
    assert verify_storage_centrifuge([[2900, 3000, 2800], [3100]]) == "STABLE"
