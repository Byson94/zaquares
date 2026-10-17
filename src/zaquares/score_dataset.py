import pandas as pd
from zaquares.wpi import ComputeWPI

DATASET = "data/kerala_water_quality/full-dataset.csv"
COLS = [
    "Potential of Hydrogen (pH)", "Dissolved oxygen (mg/L)", 
    "Nitrate N (mgN/L)", "Amonia N (mgN/L)", "Chloride (mg/L)",
    "Turbidity (NTU)", "Electric Conductivity (μS/cm)",  "Temperature (ºC)",
]
METADATA = ["Station", "Data Acquisition Time", "River_x", "Basin_x", "Tributary_x"]

def get_clean_dataset():
    df = pd.read_csv(DATASET)
    df_clean = df.dropna(subset=COLS)
    sub = df_clean[METADATA+COLS]
    return sub

def parameter_score_relation():
    sub = get_clean_dataset()
    parameters = [v for v in zip(*(sub[c] for c in COLS))]
    scores = [ComputeWPI(*v) for v in zip(*(sub[c] for c in COLS))]
    return (parameters, scores)

def main():
    sub = get_clean_dataset()
    scores = [ComputeWPI(*v) for v in zip(*(sub[c] for c in COLS))]
    sub["WPI"] = scores
    out = sub[METADATA + ["WPI"]]
    out.to_csv("data/wpi/wpi-scores.csv", index=False)

if __name__ == "__main__":
    main()
