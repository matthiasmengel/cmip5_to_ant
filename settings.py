import os

pcmdipath  = "/p/projects/ipcc_pcmdi/ipcc_ar5_pcmdi/pcmdi_data/"
target_path = "/p/tmp/mengel/pycmip5/p002_testing/"

gridfiles = "/p/projects/pism/mengel/pism_input/cdo_remapgrids/"

target_grid = "/p/projects/pism/mengel/pism_input/cdo_remapgrids/initmip_8km.nc"

# write additional info to .sh file, so it can be submitted to slurm cluster.
cluster_regridding = True

""" cmpip5 model, scenario and run choices """

models = [ 'ACCESS1-0','ACCESS1-3','bcc-csm1-1','bcc-csm1-1-m','BNU-ESM','CanESM2',
'CCSM4','CESM1-BGC','CESM1-CAM5','CESM1-FASTCHEM','CESM1-WACCM','CNRM-CM5',
'CSIRO-Mk3-6-0','EC-EARTH','FGOALS-g2','FGOALS-s2','FIO-ESM','GFDL-CM3','GFDL-ESM2G',
'GFDL-ESM2M','HadGEM2-CC','HadGEM2-ES','inmcm4','IPSL-CM5A-LR','IPSL-CM5A-MR',
'IPSL-CM5B-LR','MIROC4h','MIROC5','MIROC-ESM','MIROC-ESM-CHEM','MPI-ESM-LR',
'MPI-ESM-MR','MPI-ESM-P','MRI-CGCM3','NorESM1-M','NorESM1-ME']

#models = ['ACCESS1-0','ACCESS1-3']
# models = ['CCSM4','CESM1-BGC','CESM1-CAM5','CESM1-FASTCHEM','CESM1-WACCM','CNRM-CM5']

#scenarios = ['piControl','historical','rcp85']
scenarios = ['rcp45','rcp45','rcp60','rcp85']
run = "r1i1p1"

variable = "thetao"
time_res = "Omon"
cmip5_runid = "r1i1p1"

# not needed in current implementation
# latitude_bounds = [-90,-60]

# in m, only relevant for 3d fields, in ascending order
depth_range_to_average = [300, 1000]

# regrid to that
target_projection = ""

project_root = os.path.dirname(os.path.abspath(__file__))
