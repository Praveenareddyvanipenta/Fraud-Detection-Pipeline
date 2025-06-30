
"""train_model.py
Train an Isolation Forest anomaly model on historical transaction data.

Usage:
  python train_model.py --input data/historical_txns.json                             --output models/anomaly_model.pkl                             --contamination 0.02
"""
import argparse, pandas as pd, joblib, pathlib
from sklearn.ensemble import IsolationForest

def load_data(path: str, sample: bool = False) -> pd.DataFrame:
    if sample:
        # Generate sample data on the fly
        import numpy as np
        return pd.DataFrame({'amount': np.random.exponential(scale=75, size=500)})
    return pd.read_json(path, lines=True)

def train(df: pd.DataFrame, contamination: float) -> IsolationForest:
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(df[['amount']])
    return model

def main():
    parser = argparse.ArgumentParser(description="Train anomaly detection model")
    parser.add_argument('--input', '-i', help='Path to JSONL file with historical txns')
    parser.add_argument('--output', '-o', default='models/anomaly_model.pkl', help='Path to save model')
    parser.add_argument('--contamination', '-c', type=float, default=0.02, help='Expected fraud rate')
    parser.add_argument('--sample-data', action='store_true', help='Use random sample data instead of file')
    args = parser.parse_args()

    df = load_data(args.input, sample=args.sample_data)
    model = train(df, args.contamination)

    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output)
    print(f"Model saved to {args.output}")

if __name__ == '__main__':
    main()
