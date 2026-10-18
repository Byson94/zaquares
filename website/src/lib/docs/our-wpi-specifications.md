---
title: Our WPI Definition & Specifications
description: How our WPI model will be implemented and used across this research.
date: 2026-09-26
---

We consider a nonlinear Water Pollution Index calibrated to a specific region, such that it works reliably
and accurately for that specific region. We calibrate our WPI to Kerala, utilizing Surface Water Quality datasets from 
the Indian [National Water Data Portal](https://nwdp.nwic.gov.in/). This dataset is broken down, and is thoroughly analyzed
for the creation of our WPI definition. This data can be obtained from our [GitHub repository](https://github.com/Byson94/zaquares/tree/main/data/kerala_water_quality).

This document is kept blunt on purpose in the light of the research paper. The research paper shall be approached for the full details.

## Problems & Approach

We decided to break the task of creating a WPI definition down into the following:

- Decide on the parameters.
- Find the [min, max, center] of each parameter.
- Create a conversion function for each parameter.
- And finally, aggregate each parameter to obtain the WPI.

We decided to go with a set 8 parameters, 7 of which are scored and aggregated. They include, potential of Hydrogen (pH), Dissolved Oxygen (mg/L), Nitrate N (mgN/L), Ammonia N (mgN/L), Chloride (mg/L), Turbidity (NTU), Electric Conductivity (μS/cm), and Temperature (ºC). We considered these parameters based on other prominent water pollution indices and our dataset.

With proper analysis of the dataset, we discovered the min, max, and center of each parameter by considering the maximum natural occourance and 50th, 90th, and 95th percentile values in the dataset.

| Parameter | Min | Max | Center |
| --------- | ---- | ---- | ------ |
| potential of Hydrogen (pH) | 0 | 14 | 7.5 |
| Dissolved Oxygen (mg/L) | 0 | 25 | 7 |
| Nitrate N (mgN/L) | 0 | 1.5 | 0.47 |
| Ammonia N (mgN/L) | 0 | 1 | 0.02 |
| Chloride (mg/L) | 0 | 19 | 6 | 
| Turbidity | 0 | 23 | 1.1 | 
| Electric Conductivity | 0 | 152.5 | 52.1 |
| Temperature | 0 | 40 | 26 |

Using this data, we can create piecewise functions that will handle conversion of parameters into quality values.
Each function will be nonlinear to respect the nonlinear nature of parameters, mostly following a generic structure as,

$$
f(x) = 100 \left(1 - \left( \dfrac{x - y}{z - y} \right)^2 \right)^k ,
$$

where $x$ is the value of the parameter, $y$ is the center, $z$ is the maximum value, and $k$ is the outer exponent to curve the growth.
The minimum value is omitted since it is $0$. It is not guaranteed that we will use the exact same structure, but this is the core idea.

With that settled, we now only have to aggregate the data and form the final WPI equation. We plan on doing so through the summation of the quality value multiplied by weight value. Given $i$ indicates a parameter, $q$ is the vector of quality values, and $w$ is the vector of weights ($\sum w = 1$), the WPI can be formulated as,

$$
\text{WPI} = \sum_{i = 0}^n q_i w_i .
$$

We are also considering using geometric means since it handles the eclipsing problem better, however, it will be explored when we reach the final phase of building the WPI definition.
