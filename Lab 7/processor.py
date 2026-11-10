import math


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Returns an error message for invalid blood codes.
    """
    if not isinstance(blood_code, str):
        return "Invalid blood type"
    cleaned = blood_code.strip().upper()
    if cleaned not in {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}:
        return "Invalid blood type"
    antigen = cleaned[:-1]
    rh_char = cleaned[-1]
    rh_map = {"+": "Positive", "-": "Negative"}
    return f"{antigen} {rh_map[rh_char]}"

def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Accepts positive integer readings with systolic greater than diastolic.
    """
    if not isinstance(bp_string, str):
        return "Invalid blood pressure"
    try:
        sys_str, dia_str = bp_string.split('/')
        systolic = int(sys_str)
        diastolic = int(dia_str)
        if diastolic <= 0 or systolic <= diastolic:
            return "Invalid blood pressure"
        pulse_diff = systolic - diastolic
        ratio = round(systolic / diastolic, 2)
    except (ValueError, OverflowError):
        return "Invalid blood pressure"
    return f"Diff: {pulse_diff}, Ratio: {ratio}"

def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Rejects missing fields and non-finite or non-positive measurements.
    """
    if not isinstance(donor_entry, str):
        return "Invalid donor record"
    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid donor record"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid donor record"
    try:
        weight = float(fields[1])
        hemoglobin = float(fields[2])
    except (ValueError, OverflowError):
        return "Invalid donor record"
    if not math.isfinite(weight) or not math.isfinite(hemoglobin):
        return "Invalid donor record"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid donor record"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"

def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))

if __name__ == "__main__":
    main()
