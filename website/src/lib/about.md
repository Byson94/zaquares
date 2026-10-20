# Zaquares: A WPI Framework for Water Pollution Assessment, Estimation, and ROC Under Data Scarcity

Zaquares is a Water Pollution Assessment framework. It defines a new Water Pollution Index which is extended with an AI/ML estimation
model we created, as well as a rate of change of pollution calculator that helps identify the rate at which pollution changes.

Our WPI utilizes a total of eight parameters, including, potential of Hydrogen (pH), Dissolved Oxygen, Nitrate N (mgN/L), 
Ammonia N (mgN/L), Chloride (mg/L), Turbidity (NTU), Electric Conductivity (μS/cm), and Temperature (ºC), to score the pollution
in a water body. The quality parameter aggregation equation of our WPI is based on geometric means, which makes it natively handle
common issues indices face, such as the eclipsing problem.

Not everyone can obtain the listed 8 parameters for calculating the WPI. To combat this, we created an AI/ML model based on the
XGBoost algorithm for estimating the WPI with limited parameters. From our testings, our model reliably works for cases when only 2-3 
parameters are hidden from the model.

The Rate of Change (ROC) model we created will contribute in tracking the rate at which the pollution score, WPI, changes using calculus.
It returns a reliable vector unit of WPI change in a format such as, "+5 WPI/month", for convenience for all.
