import itertools
import numpy as np
from zaquares.zape import get_model
from zaquares.score_dataset import parameter_score_relation

PARAM_NAMES = ["pH", "DO", "NO3", "NH3", "Cl", "Tur", "EC", "T"]
NAME_TO_IDX = {n: i for i, n in enumerate(PARAM_NAMES)}

def mask(X, cols):
    Xm = X.copy()
    if cols:
        Xm[:, cols] = np.nan
    return Xm


def evaluate(model, X, y, cols):
    pred = model.predict(mask(X, cols))
    err = np.abs(pred - y)
    return err.mean(), np.median(err), err.max()

def main():
    model = get_model()
    assert model is not None, "get_model returned None"

    param_score = parameter_score_relation()
    X_test = np.array(param_score[0], dtype=np.float32)
    y_test = np.array(param_score[1], dtype=np.float32)

    assert X_test.ndim == 2 and X_test.shape[1] == 8, f"bad X shape {X_test.shape}"
    assert y_test.shape == (X_test.shape[0],), f"bad y shape {y_test.shape}"

    print(f"Test rows: {len(y_test)}\n")

    # Baseline: no missing 
    m, md, mx = evaluate(model, X_test, y_test, [])
    print(f"{'no hidden':30s}  mean={m:7.4f}  median={md:7.4f}  max={mx:7.4f}")

    # Each single feature hidden
    print("\nSingle feature hidden:")
    for name in PARAM_NAMES:
        m, md, mx = evaluate(model, X_test, y_test, [NAME_TO_IDX[name]])
        print(f"  {name:4s} hidden                     mean={m:7.4f}  median={md:7.4f}  max={mx:7.4f}")

    # Every combination, summarized by size
    print("\nAll subsets, by size:")
    for size in range(0, 8):
        means, medians, maxes = [], [], []
        for combo in itertools.combinations(PARAM_NAMES, size):
            cols = [NAME_TO_IDX[n] for n in combo]
            m, md, mx = evaluate(model, X_test, y_test, cols)
            means.append(m)
            medians.append(md)
            maxes.append(mx)
        print(
            f"  size={size}  n={len(means):3d}  "
            f"mean(MAE)={np.mean(means):7.4f}  "
            f"median(MAE)={np.median(means):7.4f}  "
            f"worst MAE={np.max(means):7.4f}"
        )

    print("\nExtremes across all 255 scenarios:")
    results = []
    for size in range(0, 8):
        for combo in itertools.combinations(PARAM_NAMES, size):
            cols = [NAME_TO_IDX[n] for n in combo]
            m, md, mx = evaluate(model, X_test, y_test, cols)
            results.append((m, md, combo))

    results.sort(key=lambda r: r[0])
    print("  Best 5:")
    for m, md, combo in results[:5]:
        print(f"    {str(combo):40s}  mean={m:7.4f}  median={md:7.4f}")
    print("  Worst 5:")
    for m, md, combo in results[-5:][::-1]:
        print(f"    {str(combo):40s}  mean={m:7.4f}  median={md:7.4f}")


if __name__ == "__main__":
    main()
