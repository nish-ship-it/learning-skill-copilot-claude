"""
ml_pipeline.py — Simple ML pipeline for income bracket prediction.

This file is intentionally simple so the Copilot skills in this repo
have something realistic to explain, explore, and improve.

Usage:
    python examples/src/ml_pipeline.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


DATA_PATH = "examples/data/sample.csv"
TARGET_COL = "income_bracket"
RANDOM_STATE = 42


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df = df.copy()

    # Encode categorical columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols = [c for c in cat_cols if c != TARGET_COL]

    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    # Encode target
    df[TARGET_COL] = (df[TARGET_COL] == ">50K").astype(int)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]
    return X, y


def train(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def evaluate(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}\n")
    print(classification_report(y_test, y_pred, target_names=["<=50K", ">50K"]))


def main() -> None:
    df = load_data(DATA_PATH)
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns\n")

    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = train(X_train, y_train)
    evaluate(model, X_test, y_test)


if __name__ == "__main__":
    main()
