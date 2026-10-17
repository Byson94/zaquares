import os
import random
import itertools
import numpy as np
import xgboost as xgb
from zaquares.wpi import ComputeWPI

PARAM_NAMES = ["pH", "DO", "NO3", "NH3", "Cl", "Tur", "EC", "T"]
NAME_TO_IDX = {name: i for i, name in enumerate(PARAM_NAMES)}

def generate_data(seed=58):
    # Range format: [min, max, center]
    # Order: pH, DO, NO3, NH3, Cl, Tur, EC, T

    high_ranges = [
        [2.0, 9.0, 7.0],
        [3.0, 12.0, 8.0],
        [0.0, 25.0, 0.47],
        [0.0, 8.0, 0.05],
        [0.0, 50.0, 6.0],
        [0.0, 50.0, 1.1],
        [0.0, 200.0, 52.1],
        [5.0, 32.0, 26.0]
    ]

    mid_ranges = [
        [6.0, 9.0, 7.0],
        [4.0, 11.0, 7.0],
        [0.0, 2.0, 0.47],
        [0.0, 0.5, 0.05],
        [0.0, 20.0, 6.0],
        [0.0, 25.0, 1.1],
        [0.0, 150.0, 52.1],
        [10.0, 32.0, 26.0]
    ]

    low_ranges = [
        [5.5, 8.5, 7.0],
        [6.0, 11.0, 7.0],
        [0.0, 2.0, 0.3],
        [0.0, 0.3, 0.02], 
        [0.0, 10.0, 5.0],
        [0.0, 15.0, 1.0], 
        [0.0, 120.0, 50.0],
        [18.0, 32.0, 22.0], 
    ]

    lowest_ranges = [
        [6.5, 8.5, 7.0],
        [6.0, 12.0, 7.0],
        [0.0, 0.8, 0.3],
        [0.0, 0.1, 0.02], 
        [2.0, 8.0, 5.0],
        [0.0, 8.0, 1.0], 
        [0.0, 80.0, 50.0],
        [20.0, 30.0, 24.0], 
    ]

    X = []
    y = []

    n_high = 1500
    n_mid = 2000
    n_low = 2000
    n_lowest = 1000

    # Determinisitic seed
    random.seed(seed)

    # High (High WPI)
    for _ in range(n_high):
        params = tuple(random.triangular(lo, hi, c) for lo, hi, c in high_ranges)
        X.append(params)
        y.append(ComputeWPI(*params))

    # Normal (Mid WPI)
    for _ in range(n_mid):
        params = tuple(random.triangular(lo, hi, c) for lo, hi, c in mid_ranges)
        X.append(params)
        y.append(ComputeWPI(*params))

    # Lower (Low WPI)
    for _ in range(n_low):
        params = tuple(random.triangular(lo, hi, c) for lo, hi, c in low_ranges)
        X.append(params)
        y.append(ComputeWPI(*params))

    # Lowest (Lowest WPI)
    for _ in range(n_lowest):
        params = tuple(random.triangular(lo, hi, c) for lo, hi, c in lowest_ranges)
        X.append(params)
        y.append(ComputeWPI(*params))

    return [X, y]

def analyze_data(data):
    # Data in format [[()], []]
    params = data[0]
    wpi = data[1]

    for idx, param in enumerate(params):
        print(f"{param} -> {wpi[idx]}")

def calibrate_per_param(model, alpha=0.10):
    calibration_data = generate_data(seed=2819)
    X_cal = np.array(calibration_data[0], dtype=np.float32)
    y_cal = np.array(calibration_data[1], dtype=np.float32)

    preds = model.predict(X_cal)
    q_empty = float(np.quantile(np.abs(preds - y_cal), 1 - alpha))

    q_by_param = {}
    for p in range(len(PARAM_NAMES)):
        Xm = X_cal.copy()
        Xm[:, p] = np.nan
        preds = model.predict(Xm)
        q_by_param[p] = float(np.quantile(np.abs(preds - y_cal), 1 - alpha))

    return q_empty, q_by_param

def train():
    print("Generating data...")
    generated_data = generate_data()

    X = np.array(generated_data[0], dtype=np.float32)
    y = np.array(generated_data[1], dtype=np.float32)

    # Create every combination of missing parameters
    all_scenarios = []
    for size in range(0, len(PARAM_NAMES)):
        for combo in itertools.combinations(PARAM_NAMES, size):
            all_scenarios.append(combo)


    EXTRA = {0: 99, 1: 24, 2: 9}
    X_blocks = []
    y_blocks = []

    print("Creating scenarios...")
    for scenario in all_scenarios:
        cols = [NAME_TO_IDX[n] for n in scenario]
        X_masked = X.copy()
        if cols:
            X_masked[:, cols] = np.nan
        X_blocks.append(X_masked)
        y_blocks.append(y)

        for _ in range(EXTRA.get(len(scenario), 0)):
            X_blocks.append(X_masked)
            y_blocks.append(y)

    X_train = np.concatenate(X_blocks, axis=0)
    y_train = np.concatenate(y_blocks, axis=0)

    # Train model
    print("Training model...")
    model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        objective="reg:squarederror",
    )
    model.fit(X_train, y_train)
    model.save_model("zape.ubj")

    print("Calibrating...")
    q_empty, q_by_param = calibrate_per_param(model, alpha=0.10)
    q_array = np.array([q_empty] + [q_by_param[p] for p in range(len(PARAM_NAMES))])
    np.save("zape_q.npy", q_array)

    return model

def get_model():
    if os.path.isfile("zape.ubj"):
        print("[Loading model]")
        model = xgb.XGBRegressor()
        model.load_model("zape.ubj")
        return model
    else:
        print("[Starting training process]")
        return train()

def get_calibration():
    if os.path.isfile("zape_q.npy"):
        print("[Loading calibration]")
        q_array = np.load("zape_q.npy")
        return q_array
    else:
        raise RuntimeError("'zape_q.npy' is missing. Is model properly trained?")

def main():
    model = get_model()
    calibration = get_calibration()
    
    xpH = float(input("pH: "))
    xDO = float(input("DO: "))
    xNO3 = float(input("NO3: ")) # Nitrate N
    xNH3 = float(input("NH3: ")) # Ammonia N
    xCl = float(input("Cl: "))
    xTur = float(input("Tur: "))
    xEC = float(input("EC: "))
    xT = float(input("T: "))
    hide = [int(n) for n in input("Hide?: ").replace(" ", "").split(",") if n.strip().isdigit()]
    print()

    inputs = [xpH, xDO, xNO3, xNH3, xCl, xTur, xEC, xT]
    score = ComputeWPI(*inputs)

    model_inputs = inputs.copy()

    for h in hide:
        if not 0 <= h < len(inputs):
            print(f"hide must be 0..{len(inputs) - 1}")
        else:
            model_inputs[h] = np.nan

    data = np.array([model_inputs], dtype=np.float32)
    cal_data = generate_data(seed=958)
    predicted = float(model.predict(data)[0])

    q_empty = float(calibration[0])
    q_by_param = {p: float(calibration[p + 1]) for p in range(len(PARAM_NAMES))}

    if not hide:
        q_hat = q_empty
    else:
        q_hat = float(np.sqrt(sum(q_by_param[p] ** 2 for p in hide)))

    print("Score    :", score)
    print("Predicted:", predicted)
    print(f"90% Confidence: [{predicted - q_hat:.2f}, {predicted + q_hat:.2f}]")
    print("Abs error:", abs(predicted - score))

if __name__ == "__main__":
    main()
