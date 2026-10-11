#= Conversion Functions =#

def score_pH(x):
    if x < 0 or x > 14:
        raise ValueError("pH out of [0, 14] bounds")
    return 100 * (1 - abs((x - 7.5) / 7.5) ** 2) ** 4

def score_DO(x):
    if x >= 7:
        return 100

    return 100 * (1 - abs((x - 7) / 7) ** 2) ** 4

def score_NH3(x):
    if x < 0 or x > 1:
        raise ValueError("NH3 out of [0, 1] bounds")
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
    if x <= 1:
        return 100
    elif x >= 23:
        return 0
    else:
        return 100 * (1 - ((x - 1) / (23 - 1)) ** 2) ** 1.54

def score_EC(x):
    if x <= 52:
        return 100
    elif x >= 150:
        return 0
    else:
        return 100 * (1 - ((x - 52) / (150 - 52)) ** 2) ** 6

#= Computation & Weights =#

# Order: pH, DO, NH3, NO3, Cl, Tur, EC
# Condition: Must add up to 1
weights = [0.1, 0.2, 0.1, 0.1, 0.2, 0.1, 0.2]

def compute_from_raw(qarr):
    return sum(wi * qi for wi, qi in zip(weights, qarr))

class WPICalculator:
    def __init__(self, xpH, xDO, xNH3, xNO3, xCl, xTur, xEC, xT):
        self.xpH = xpH
        self.xDO = xDO
        self.xNH3 = xNH3
        self.xNO3 = xNO3
        self.xCl = xCl
        self.xTur = xTur
        self.xEC = xEC
        self.xT = xT
        self.qarr = []

    def compute(self):
        clamped_xpH = min(max(self.xpH, 0), 7)
        clamped_xNH3 = min(max(self.xNH3, 0), 1)
        clamped_xDO = min(max(self.xDO, 0), 7)
        self.qarr = [
            score_pH(clamped_xpH),
            score_DO(clamped_xDO),
            score_NH3(clamped_xNH3),
            score_NO3(self.xNO3),
            score_Cl(self.xCl),
            score_Tur(self.xTur),
            score_EC(self.xEC)
        ]
        return compute_from_raw(self.qarr)

#= CLI WPI Interface =#
def main():
    print("Zaquares WPI")
    print("------------")

    xpH = float(input("pH: "))
    xDO = float(input("DO: "))
    xNH3 = float(input("NH3: "))
    xNO3 = float(input("NO3: "))
    xCl = float(input("Cl: "))
    xTur = float(input("Tur: "))
    xEC = float(input("EC: "))
    xT = float(input("T: "))
    print()

    calc = WPICalculator(xpH, xDO, xNH3, xNO3, xCl, xTur, xEC, xT)
    score = calc.compute()
    print("Score:", score)
