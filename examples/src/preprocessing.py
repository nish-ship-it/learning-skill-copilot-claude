"""Stage 2: Preprocessing
Imputation, encoding, scaling — returns train/test splits ready for modelling.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

NUMERIC_COLS = ["age", "income", "education_years", "hours_per_week"]
CATEGORICAL_COLS = ["occupation", "marital_status", "gender", "native_country"]
TARGET_COL = "income_bracket"
TEST_SIZE = 0.20
RANDOM_STATE = 42


def preprocess(df: pd.DataFrame):
    """Return (X_train, X_test, y_train, y_test, feature_names, artifacts).

    artifacts contains fitted transformers for later serialisation.
    """
    df = df.copy()

    # --- Imputation ---
    num_imputer = SimpleImputer(strategy="median")
    df[NUMERIC_COLS] = num_imputer.fit_transform(df[NUMERIC_COLS])

    # --- Encode categoricals ---
    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # --- Encode target ---
    target_le = LabelEncoder()
    y = target_le.fit_transform(df[TARGET_COL])
    X = df.drop(columns=[TARGET_COL])

    # --- Scale numerics ---
    scaler = StandardScaler()
    X[NUMERIC_COLS] = scaler.fit_transform(X[NUMERIC_COLS])

    feature_names = list(X.columns)
    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    artifacts = {
        "num_imputer": num_imputer,
        "encoders": encoders,
        "target_encoder": target_le,
        "scaler": scaler,
        "feature_names": feature_names,
    }
    return X_train, X_test, y_train, y_test, feature_names, artifacts


def load_and_preprocess(csv_path: str):
    print(f"\n{'='*50}")
    print("STAGE 2: PREPROCESSING")
    print(f"{'='*50}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows × {len(df.columns)} cols")
    print(f"Missing before imputation: {df.isnull().sum().sum()} cells")

    X_train, X_test, y_train, y_test, feature_names, artifacts = preprocess(df)

    print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")
    print(f"Features ({len(feature_names)}): {feature_names}")
    print(f"Class balance in train — "
          f">50K: {y_train.sum()} | <=50K: {len(y_train)-y_train.sum()}")
    return X_train, X_test, y_train, y_test, feature_names, artifacts


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/data/sample.csv"
    load_and_preprocess(path)
