import math

def validate_domain(name, val, l, m):
    if val < l or val > m:
        return ValueError(f"{name} out of [{l}, {m}] bounds")

def score_pH(x):
    return 100 * (1 - abs((x - 7.5) / 7.5) ** 2) ** 4

def DO_sat(xT):
    TK = xT + 273.15
    return math.exp(
        -139.34411 + (1.575701 * 10 ** 5) / TK
        - (6.642308 * 10 ** 7) / TK ** 2
        + (1.243800 * 10 ** 10) / TK ** 3
        - (8.621949 * 10 ** 11) / TK ** 4
    )

def score_DO(xDO, xT):
    sat = DO_sat(xT)
    if xDO >= 2 * sat:
        return 0
    return 100 * (1 - ((xDO - sat) / sat) ** 2) ** 4

def score_NH3(x):
    if x <= 0:
        return 100
    elif x >= 1:
        return 0
    else: 
        return 100 * (1 - x ** 2) ** 30

def score_NO3(x):
    if x <= 0.47:
        return 100
    elif x >= 1.5:
        return 0
    else:
        return 100 * (1 - ((x - 0.47) / (1.5 - 0.47)) ** 2) ** 4

def score_Cl(x):
    if x <= 6:
        return 100
    elif x >= 19:
        return 0
    else:
        return 100 * (1 - ((x - 6) / (19 - 6)) ** 2) ** 4

def score_Tur(x):
    if x <= 1.1:
        return 100
    elif x >= 23:
        return 0
    else:
        return 100 * (1 - ((x - 1.1) / (23 - 1.1)) ** 2) ** 1.54

def score_EC(x):
    if x <= 52.1:
        return 100
    elif x >= 151.2:
        return 0
    else:
        return 100 * (1 - ((x - 52.1) / (151.2 - 52.1)) ** 2) ** 6

# Order: pH, DO, NO3, NH3, Cl, Tur, EC
# Condition: Must add up to 1
WEIGHTS = [0.08571428571428572, 0.22857142857142856, 0.2, 0.17142857142857143, 0.11428571428571428, 0.05714285714285714, 0.14285714285714285]

def compute_from_raw(qarr):
    if not math.isclose(sum(WEIGHTS), 1.0):
        raise ValueError("bug: weights do not add up to 1")

    return 100 - sum(wi * qi for wi, qi in zip(WEIGHTS, qarr))

def ComputeWPI(xpH, xDO, xNO3, xNH3, xCl, xTur, xEC, xT):
    qarr = [
        score_pH(validate_domain("pH", xpH, 0, 14)),
        score_DO(validate_domain("DO", xDO, 0, 25), validate_domain("T", xT, 0, 40)),
        score_NO3(validate_domain("NO3", xNO3, 0, 50)),
        score_NH3(validate_domain("NH3", xNH3, 0, 20)),
        score_Cl(validate_domain("Cl", xCl, 0, 1000)),
        score_Tur(validate_domain("Tur", xTur, 0, 10000)),
        score_EC(validate_domain("EC", xEC, 0, 5000))
    ]
    return compute_from_raw(qarr)

# CLI Interface
def main():
    print("Zaquares WPI")
    print("------------")

    xpH = float(input("pH: "))
    xDO = float(input("DO: "))
    xNO3 = float(input("NO3: "))
    xNH3 = float(input("NH3: "))
    xCl = float(input("Cl: "))
    xTur = float(input("Tur: "))
    xEC = float(input("EC: "))
    xT = float(input("T: "))
    print()

    score = ComputeWPI(xpH, xDO, xNO3, xNH3, xCl, xTur, xEC, xT)
    print("Score:", round(score))

if __name__ == "__main__":
    main()
