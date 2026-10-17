import matplotlib.pyplot as plt
from zaquares.zape import get_model

def gen_zape_importance():
    import xgboost as xgb
    
    model = get_model()
    booster = model.get_booster()
    booster.feature_names = ["pH", "DO", "NO3", "NH3", "Cl", "Tur", "EC", "T"]

    xgb.plot_importance(model)

    plt.tight_layout()
    plt.savefig("data/zape/importance.png", dpi=150, bbox_inches="tight")
    plt.close()

def main():
    gen_zape_importance()

if __name__ == "__main__":
    main()
