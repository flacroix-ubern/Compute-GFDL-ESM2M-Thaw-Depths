# Compute-GFDL-ESM2M-Thaw-Depths
This script computes permafrost thaw depths, carbon loss and tundra area change based on monthly model output files.

## How to run
Run the script:
python scripts/compute_gfdlesm2m_thawdepth.py $path $sim $year_start $year_end

As an example with $path = /oceandata02/model_data/ESM2M_CSCS/ $sim = AERA3_T30_TYPE2_ENS1 $year_start = 2026 $year_end = 2100
python scripts/compute_gfdlesm2m_thawdepth.py /oceandata02/model_data/ESM2M_CSCS/ AERA3_T30_TYPE2_ENS1 2026 2100

