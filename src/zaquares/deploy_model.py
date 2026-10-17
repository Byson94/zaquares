import json
import shutil
import xgboost as xgb
from zaquares.zape import get_model, get_calibration

def main():
    model = get_model()
    calibration = get_calibration()

    shutil.copy("zape.ubj", "website/static/zape.ubj")

    calibration_dict = {
        "q_empty": float(calibration[0]),
        "q_by_param": {
            p: float(calibration[p + 1]) for p in range(8)
        },
    }
    with open("website/static/zape_q.json", "w") as f:
        json.dump(calibration_dict, f, indent=2)

    print("DONE")

if __name__ == "__main__":
    main()
