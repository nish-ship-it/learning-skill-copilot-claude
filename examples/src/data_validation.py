"""Stage 1: Data Validation
Checks schema, null rates, value ranges, and class balance before training.
"""
import sys
import pandas as pd

SCHEMA = {
    "age": "numeric",
    "income": "numeric",
    "education_years": "numeric",
    "hours_per_week": "numeric",
    "occupation": "categorical",
    "marital_status": "categorical",
    "gender": "categorical",
    "native_country": "categorical",
    "income_bracket": "categorical",
}
REQUIRED_COLS = list(SCHEMA.keys())
TARGET_COL = "income_bracket"
TARGET_VALUES = {">50K", "<=50K"}
MAX_NULL_RATE = 0.20  # fail if any column exceeds 20% nulls


def validate(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    results = {"passed": True, "warnings": [], "errors": []}

    # 1. Schema check
    missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing_cols:
        results["errors"].append(f"Missing columns: {missing_cols}")
        results["passed"] = False

    # 2. Null rate check
    null_rates = df.isnull().mean()
    for col, rate in null_rates.items():
        if rate > MAX_NULL_RATE:
            results["errors"].append(f"{col} null rate {rate:.1%} exceeds {MAX_NULL_RATE:.0%}")
            results["passed"] = False
        elif rate > 0:
            results["warnings"].append(f"{col} has {rate:.1%} nulls ({int(rate * len(df))} rows)")

    # 3. Target value check
    if TARGET_COL in df.columns:
        unexpected = set(df[TARGET_COL].dropna().unique()) - TARGET_VALUES
        if unexpected:
            results["errors"].append(f"Unknown target values: {unexpected}")
            results["passed"] = False

    # 4. Class balance
    if TARGET_COL in df.columns:
        dist = df[TARGET_COL].value_counts(normalize=True)
        minority_rate = dist.min()
        if minority_rate < 0.10:
            results["warnings"].append(
                f"Severe class imbalance: minority class is {minority_rate:.1%} of data"
            )
        results["class_distribution"] = dist.to_dict()

    results["rows"] = len(df)
    results["columns"] = len(df.columns)
    results["null_rates"] = null_rates[null_rates > 0].to_dict()
    return results


def main(csv_path: str):
    print(f"\n{'='*50}")
    print("STAGE 1: DATA VALIDATION")
    print(f"{'='*50}")
    print(f"File: {csv_path}")

    r = validate(csv_path)
    print(f"\nRows: {r['rows']}, Columns: {r['columns']}")

    if r.get("null_rates"):
        print("\nNull rates:")
        for col, rate in r["null_rates"].items():
            print(f"  {col}: {rate:.1%}")

    if r.get("class_distribution"):
        print("\nClass distribution:")
        for label, pct in r["class_distribution"].items():
            print(f"  {label}: {pct:.1%}")

    if r["warnings"]:
        print("\nWarnings:")
        for w in r["warnings"]:
            print(f"  ⚠ {w}")

    if r["errors"]:
        print("\nErrors:")
        for e in r["errors"]:
            print(f"  ✗ {e}")

    status = "PASSED ✓" if r["passed"] else "FAILED ✗"
    print(f"\nValidation: {status}")
    return r


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/data/sample.csv"
    result = main(path)
    sys.exit(0 if result["passed"] else 1)
