import os
import pwd

pcmdipath  = "/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/"
target_path = "/p/tmp/mengel/cmip5_to_ant/p004_8kmprojections/"
target_grid_folder = "/p/projects/pism/mengel/pism_input/cdo_remapgrids/"

grid_id = "initmip8km"

# if preprocessing is done, you can merge different scenarios with this option
only_merge_scenarios = True
# use this option with create_cdo_mergescen.py
scenarios_to_merge = ['historical','rcp26']
datafolder_to_merge = "concat"
file_identifier = "initmip8km"

# write additional info to .sh file, so it can be submitted to slurm cluster.
cluster_regridding = True
use_cdo_extrapolation = True

""" cmpip5 model, scenario and run choices """

models = [ 'ACCESS1-0','ACCESS1-3','bcc-csm1-1','bcc-csm1-1-m','BNU-ESM','CanESM2',
'CCSM4','CESM1-BGC','CESM1-CAM5','CESM1-FASTCHEM','CESM1-WACCM','CNRM-CM5',
'CSIRO-Mk3-6-0','EC-EARTH','FGOALS-g2','FGOALS-s2','FIO-ESM','GFDL-CM3','GFDL-ESM2G',
'GFDL-ESM2M','HadGEM2-CC','HadGEM2-ES','inmcm4','IPSL-CM5A-LR','IPSL-CM5A-MR',
'IPSL-CM5B-LR','MIROC4h','MIROC5','MIROC-ESM','MIROC-ESM-CHEM','MPI-ESM-LR',
'MPI-ESM-MR','MPI-ESM-P','MRI-CGCM3','NorESM1-M','NorESM1-ME']

models = ['IPSL-CM5A-LR','CSIRO-Mk3-6-0','GFDL-CM3']
# models = ['CCSM4','CESM1-BGC','CESM1-CAM5','CESM1-FASTCHEM','CESM1-WACCM','CNRM-CM5']

scenarios = ['piControl','historical','rcp26','rcp45','rcp60','rcp85']
scenarios = ['rcp26','rcp85']

variable = "tas"
time_res = "Amon"
cmip5_runid = "r1i1p1"

# in m, only relevant for 3d fields, in ascending order
depth_range_to_average = [400, 800]

# no edits below this line needed.
project_root = os.path.dirname(os.path.abspath(__file__))
user = pwd.getpwuid(os.getuid()).pw_name
