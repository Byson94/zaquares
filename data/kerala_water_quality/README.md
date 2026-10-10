# Kerala Water Quality

This folder contains the summarized data from the chemical and physical parameters of water bodies in Kerala. These data are obtained and extracted from the [National Water Data Portal](https://nwdp.nwic.gov.in/), specifically Surface Water Quality Assessment conducted by CWC:

- https://nwdp.nwic.gov.in/dataset/surface-water-quality-manual-chemical-parameters-andhra-pradesh-central-water-commission-cwc/resource/fa150c6f-6e54-4946-9fb5-d81a910f32ee
- https://nwdp.nwic.gov.in/dataset/surface-water-quality-manual-physical-parameters-central-water-commission-cwc/resource/6c9da048-2821-451d-b9db-6d5633190612

The data is extracted into the following files:

- **clean.csv**: Full dataset with duplicate (station, latitude, longitude) rows collapsed to their mean.
- **stations.csv**: Per-station mean of every numeric parameter, with sample count. 
- **percentiles.csv**: Per-station percentile values (p10–p95) for each numeric parameter.
- **overall.csv**: Statewide distribution per parameter (n, mean, std, min, max, p10–p95).
