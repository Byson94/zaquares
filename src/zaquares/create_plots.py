import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from zaquares.zape import get_model

def gen_ranked_dataset():
    df = pd.read_csv("data/wpi/wpi-scores.csv")
    result = (
        df.groupby("Station")
            .agg(River=("River_x", "first"), Tributary=("Tributary_x", "first"), WPI=("WPI", "median"))
            .sort_values("WPI", ascending=False)
            .reset_index()
    )
    result = result.rename(columns={"River_x": "River", "Tributary_x": "Tributary"})
    result["WPI"] = result["WPI"].round(2)

    fig, ax = plt.subplots(figsize=(6.5, 2))
    ax.axis("off")

    table = ax.table(
        cellText=result.values,
        colLabels=result.columns,
        cellLoc="center",
        loc="upper center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    for col_idx in range(len(result.columns)):
        cell = table[(0, col_idx)]
        cell.set_facecolor('#d9d9d9')
        cell.set_text_props(weight='bold', color='black')

    ax.set_title("Stations in Kerala ranked by median WPI", pad=18)
    ax.text(0.5, 1.02,
            "Median over all samples obtained at different dates per station. Higher WPI means more polluted.",
            transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8, style="italic", color="0.35")

    fig.savefig("data/wpi/ranked-dataset.pdf", dpi=150, bbox_inches="tight")
    plt.close(fig)

def gen_zape_importance():
    import xgboost as xgb
    
    model = get_model()
    booster = model.get_booster()
    booster.feature_names = ["pH", "DO", "NO3", "NH3", "Cl", "Tur", "EC", "T"]

    xgb.plot_importance(model)

    plt.tight_layout()
    plt.savefig("data/zape/param-importance.pdf", dpi=150, bbox_inches="tight")
    plt.close()

def gen_zape_best_worst_table(n=5):
    df = pd.read_csv("data/zape/test-results.csv", keep_default_na=False)
    df["hidden"] = df["hidden"].replace("", "none").str.replace(";", ", ")

    ranked = df.sort_values("mean")
    best = ranked.head(n)
    worst = ranked.tail(n).iloc[::-1]

    cell_text = [
        [b.hidden, f"{b['mean']:.2f}", w.hidden, f"{w['mean']:.2f}"]
        for (_, b), (_, w) in zip(best.iterrows(), worst.iterrows())
    ]
    columns = ["Best hidden", "MAE", "Worst hidden", "MAE"]

    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.axis("off")
    tbl = ax.table(cellText=cell_text, colLabels=columns,
                   cellLoc="left", loc="center",
                   colWidths=[0.2, 0.08, 0.5, 0.08])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)

    for col_idx in range(len(columns)):
        cell = tbl[(0, col_idx)]
        cell.set_facecolor('#d9d9d9')
        cell.set_text_props(weight='bold', color='black')

    fig.text(0.5, 0.0,
             "MAE: Mean Absolute Error. Average of |predicted WPI - true WPI| "
             "over all test rows, in WPI score. Lower is better.",
             ha="center", va="bottom", fontsize=8, style="italic", wrap=True)

    ax.set_title("Best and worst parameters to hide from the ML model")
    fig.savefig("data/zape/best-worst-params.pdf", bbox_inches="tight")
    plt.close(fig)

def gen_zape_mae_rise():
    df = pd.read_csv("data/zape/test-results.csv")
    g = df.groupby("size")["mean"].mean()
    idx = g / g.iloc[0] * 100
    step = g.diff().dropna()
    pct = g.pct_change().dropna() * 100

    fig, (ax, ax2) = plt.subplots(
        2, 1, sharex=True, figsize=(6.5, 4.5),
        gridspec_kw={"height_ratios": [3, 1]}, constrained_layout=True)

    ax.plot(idx.index, idx.values, "o-", color="tab:red")
    ax.fill_between(idx.index, idx.values, alpha=0.15, color="tab:red")
    ax.axhline(100, ls="--", lw=0.8, color="gray")
    top = float(idx.max())
    ax.set_ylim(0, top * 1.15)
    ax.set_ylabel("Error index (0 hidden = 100)")
    ax.set_title("MAE growth vs. number of hidden parameters")
    ax.grid(alpha=0.3)

    for x, p in pct.items():
        ax.annotate(f"+{p:.0f}%", (x, idx[x]),
                    textcoords="offset points", xytext=(-4, 8),
                    ha="right", fontsize=8)

    ax2.bar(step.index, step.values, color="tab:gray")
    ax2.set_ylabel("MAE (WPI)")
    ax2.set_xlabel("Number of hidden parameters")
    ax2.set_xticks(idx.index)
    ax2.grid(alpha=0.3, axis="y")

    fig.savefig("data/zape/mae-rise.pdf", bbox_inches="tight")
    plt.close(fig)

def gen_zape_headline(tols=(5, 10), max_size=4):
    res = pd.read_csv("data/zape/test-results.csv",
                      usecols=["scenario_id", "size"])
    err = pd.read_csv("data/zape/test-errors.csv",
                      usecols=["scenario_id", "abs_err"])
    e = err.merge(res, on="scenario_id")
    e = e[e["size"] <= max_size]

    scn = e["scenario_id"].to_numpy()
    size = e["size"].to_numpy()
    ae = e["abs_err"].to_numpy(dtype=float)

    # scenario -> hidden count
    scn_ids = np.unique(scn)
    scn_size = np.array([size[scn == i][0] for i in scn_ids])
    sizes = np.arange(max_size + 1)

    colors = ["tab:blue", "tab:red"]
    fig, ax = plt.subplots(figsize=(6.5, 4.2), constrained_layout=True)

    for tol, color in zip(tols, colors):
        # % of rows within tol, per scenario
        share = np.array([(ae[scn == i] <= tol).mean() * 100 for i in scn_ids])
        mean = np.array([share[scn_size == s].mean() for s in sizes])
        lo = np.array([share[scn_size == s].min() for s in sizes])
        hi = np.array([share[scn_size == s].max() for s in sizes])

        ax.fill_between(sizes, lo, hi, color=color, alpha=0.12)
        ax.plot(sizes, mean, "o-", color=color, lw=2,
                label=f"within ±{tol} WPI")
        for s in sizes[-2:]:
            ax.annotate(f"{mean[s]:.0f}%", (s, mean[s]),
                        textcoords="offset points", xytext=(0, 8),
                        ha="center", fontsize=9, color=color,
                        fontweight="bold")

    ax.axvspan(2.5, max_size + 0.5, color="gray", alpha=0.07)
    ax.set_xlim(-0.3, max_size + 0.3)
    ax.set_ylim(0, 105)
    ax.set_xticks(sizes)
    ax.set_xlabel("Number of hidden parameters")
    ax.set_ylabel("Predictions within tolerance (%)")
    ax.set_title("Model accuracy with hidden parameters")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)

    fig.text(0.5, 0.0,
             "Line: mean over all hidden combinations. "
             "Band: worst to best combination.",
             ha="center", va="top", fontsize=8, style="italic")

    fig.savefig("data/zape/headline.pdf", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)

def main():
    gen_ranked_dataset()
    gen_zape_importance()
    gen_zape_best_worst_table()
    gen_zape_mae_rise()
    gen_zape_headline()

    print("DONE!")

if __name__ == "__main__":
    main()
