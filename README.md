# Compute-GFDL-ESM2M-Thaw-Depths
This script computes permafrost thaw depths, carbon loss and tundra area change based on monthly model output files.

## How to run
Run the script: <br />
``` python scripts/compute_gfdlesm2m_thawdepth.py _$path_ _$sim_ _$year_start_ _$year_end_ ``` <br />
<br />
As an example with $path = /oceandata02/model_data/ESM2M_CSCS/, $sim = AERA3_T30_TYPE2_ENS1, $year_start = 2026, $year_end = 2100 <br />
<br />
``` python scripts/compute_gfdlesm2m_thawdepth.py /oceandata02/model_data/ESM2M_CSCS/ AERA3_T30_TYPE2_ENS1 2026 2100  ``` <br />

