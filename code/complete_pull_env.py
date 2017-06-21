import sys
import os as os
import os.path as op
import ant_util as au
import compare_components as cc
import build_package as bp
import metadata_pull as mp

#get cmd line arguments
run_path = sys.argv[1]
source = sys.argv[2]

component_list = mp.getCompFromFile(run_path)


#metadata pull source
source_components = mp.metadata_pull(run_path,source,component_list)

if source_components:
    #build package for source
    bp.buildpackage(run_path,source_components,source,'completepull')

    #ant run
    au.retrieve_specific_env(run_path,source)
else:
    print('No metadata available for the listed components')