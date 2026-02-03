# Compute-GFDL-ESM2M-Thaw-Depths
This script computes permafrost thaw depths, carbon loss and tundra area change based on monthly model output files.

## Installation
1. The script uses packages installed:
   - matplotlib
   - numpy
   - NetCDF4
   - xarray <br />
If they are missing, these can be installed via pip or conda. 

2. Clone source code

## How to run
The script requires following inputs: 1. path to model folder (without simulation ID), 2. simulation ID (e.g., AERA3_T30_TYPE2_ENS1), 3. first year of the simulation (e.g. 2026) and 4. last year of simulation wantd in the analysis (e.g., 2300)  

Run the script: <br />
``` python scripts/compute_gfdlesm2m_thawdepth.py _$path_ _$sim_ _$year_start_ _$year_end_ ``` <br />
<br />
As an example: <br />
<br />
``` python scripts/compute_gfdlesm2m_thawdepth.py /oceandata02/model_data/ESM2M_CSCS/ AERA3_T30_TYPE2_ENS1 2026 2300  ``` <br />

