---
title: The Machine Learning Model and Information
description: Documenting how the ML model is implemented and trained.
date: 2026-10-02
---

The current WPI Definition requires all the previously listed parameters to be present to produce a valid WPI score. The scarce parameters from the unmonitored water bodies are insufficient for our WPI Definition. This section proposes a Machine Learning (ML) model trained on a labeled set of results from our WPI definition. For the model, we chose XGBoost, a scalable tree boosting algorithm that that is efficient in spotting nonlinear patterns between data and the result. Additionally, we build a confidence metric for the model that indicates the 90% confidence of the model in the estimated score being between $[x, y]$. The larger the gap between $x$ and $y$ is, the more limited information the supplied parameters provided. This contributes in understanding when and when not to trust the model with its estimations.

Since our WPI definition is deterministic we can synthetically generate the data required for the models training. It is generated in four sections: the high ranges, mid ranges, low ranges, and lowest ranges, with each range approaching the ideal parameter values more. The high range has $1500$ samples, the mid and low ranges has $2000$ samples each, and the lowest range has $1000$ samples, with a total of $6500$ samples. 

This data is then processed to create scenarios where some parameter values are hidden. This is applied to every combination of missing parameters, excluding the combination where all parameters are hidden, for a total of $255$ unique combinations.

This training data is then fed into the XGBoost Regressor model with $300$ estimators, $0.05$ learning rate, and a max depth of $4$. The calibration process is then executed which handles the confidence metric based on what parameter is missing.


