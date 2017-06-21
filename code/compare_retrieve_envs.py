import sys
import os as os
import os.path as op
import ant_util as au
import sync_util as su
import compare_components as cc
import build_package as bp
import metadata_pull as mp

#get cmd line arguments
run_path = sys.argv[1]
source = sys.argv[2]
target = sys.argv[3]


component_list = mp.getCompFromFile(run_path)


#metadata pull source & target
source_components = mp.metadata_pull(run_path,source,component_list)
target_components = mp.metadata_pull(run_path,target,component_list)

if not source_components:
    if not source_components:
        print('No metadata available for the listed components in both the environments')
else:
	#compare source & target metadata and store result
	matching, source_additional, target_additional = cc.compare(run_path,source,target,source_components,target_components,component_list)

	#build package for source & target
	bp.buildpackage(run_path,matching,source,'matching')
	bp.buildpackage(run_path,matching,target,'matching')
	if source_additional:
		bp.buildpackage(run_path,source_additional,source,'additional')
	if target_additional:
		bp.buildpackage(run_path,target_additional,target,'additional')


	#ant run
	src_path,target_path = au.retrieve_multiple_envs(run_path,source,target)

	#compare matching retrieve
	su.sync_compare(run_path,source,target,src_path,target_path)