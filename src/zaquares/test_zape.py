import os
import itertools
import numpy as np
import pandas as pd
from zaquares.zape import get_model
from zaquares.score_dataset import parameter_score_relation

PARAM_NAMES = ["pH", "DO", "NO3", "NH3", "Cl", "Tur", "EC", "T"]
NAME_TO_IDX = {n: i for i, n in enumerate(PARAM_NAMES)}
OUT_DIR = "data/zape"


def mask(X, cols):
    Xm = X.copy()
    if cols:
        Xm[:, cols] = np.nan
    return Xm


def evaluate(model, X, y, cols):
    pred = model.predict(mask(X, cols))
    return pred, np.abs(pred - y)


def main():
    model = get_model()
    assert model is not None, "get_model returned None"

    param_score = parameter_score_relation()
    X_test = np.array(param_score[0], dtype=np.float32)
    y_test = np.array(param_score[1], dtype=np.float32)

    assert X_test.ndim == 2 and X_test.shape[1] == 8, f"bad X shape {X_test.shape}"
    assert y_test.shape == (X_test.shape[0],), f"bad y shape {y_test.shape}"

    print(f"Test rows: {len(y_test)}\n")

    # Handle 255 scenarios
    summary, errors = [], []
    sid = 0
    for size in range(len(PARAM_NAMES)):
        for combo in itertools.combinations(PARAM_NAMES, size):
            cols = [NAME_TO_IDX[n] for n in combo]
            pred, err = evaluate(model, X_test, y_test, cols)

            row = {"scenario_id": sid, "size": size, "hidden": ";".join(combo)}
            row.update({n: int(n in combo) for n in PARAM_NAMES})
            row.update(mean=float(err.mean()),
                       median=float(np.median(err)),
                       max=float(err.max()))
            summary.append(row)

            errors.append(pd.DataFrame({
                "scenario_id": sid,
                "row": np.arange(len(y_test)),
                "y_true": y_test,
                "y_pred": pred,
                "abs_err": err,
            }))
            sid += 1

    df = pd.DataFrame(summary)
    df_err = pd.concat(errors, ignore_index=True)

    # Baseline
    b = df[df["size"] == 0].iloc[0]
    print(f"{'no hidden':30s}  mean={b['mean']:7.4f}  median={b['median']:7.4f}  max={b['max']:7.4f}")

    # Single feature hidden
    print("\nSingle feature hidden:")
    for _, r in df[df["size"] == 1].iterrows():
        print(f"  {r['hidden']:4s} hidden                     "
              f"mean={r['mean']:7.4f}  median={r['median']:7.4f}  max={r['max']:7.4f}")

    # By size
    print("\nAll subsets, by size:")
    g = df.groupby("size")["mean"].agg(["count", "mean", "median", "max"])
    for size, r in g.iterrows():
        print(f"  size={size}  n={int(r['count']):3d}  "
              f"mean(MAE)={r['mean']:7.4f}  "
              f"median(MAE)={r['median']:7.4f}  "
              f"worst MAE={r['max']:7.4f}")

    # Extremes
    ranked = df.sort_values("mean")
    print("\nExtremes across all 255 scenarios:")
    print("  Best 5:")
    for _, r in ranked.head(5).iterrows():
        print(f"    {str(tuple(r['hidden'].split(';')) if r['hidden'] else ()):40s}  "
              f"mean={r['mean']:7.4f}  median={r['median']:7.4f}")
    print("  Worst 5:")
    for _, r in ranked.tail(5).iloc[::-1].iterrows():
        print(f"    {str(tuple(r['hidden'].split(';'))):40s}  "
              f"mean={r['mean']:7.4f}  median={r['median']:7.4f}")

    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(f"{OUT_DIR}/test-results.csv", index=False)
    df_err.to_csv(f"{OUT_DIR}/test-errors.csv", index=False)
    print(f"\nSaved {OUT_DIR}/test-results.csv ({len(df)} rows)")
    print(f"Saved {OUT_DIR}/test-errors.csv ({len(df_err)} rows)")


if __name__ == "__main__":
    main()
