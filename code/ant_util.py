#from subprocess import call
#import subprocess
import sys
import time
import shutil
import os as os


def retrieve_multiple_envs(run_path,source,target):
    #call(["cd","C:\mydata\Zurich Salesforce\Zurich Ant Deployment\Zurich Salesforce\All Components"])
    #subprocess.check_call(["ant", "retrieve"],cwd=in_path)

    os.chdir(run_path+'\\src')
    #manipulate build.xml to get the source property file
    f = open(run_path+'\\src\/reference\/reference_build.xml','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("[CUSTOM]",source)
    newdata = newdata.replace("[SOURCE]",source)
    newdata = newdata.replace("[TARGET]",target)
    f = open(run_path+'\\src\/build.xml','w')
    f.write(newdata)
    f.close()

    if os.path.exists(run_path+'\\src\/reference\\'+source+'_matching_package.xml'):
        src = os.system('ant retrieveSourceEnv')
        if src != 0: 
           print('Error on ant retrieve matching from source environment')
           sys.exit(1)
    if os.path.exists(run_path+'\\src\/reference\\'+source+'_additional_package.xml'):
        src_add = os.system('ant retrieveSourceAdd')
        if src_add != 0: 
            print('Error on ant retrieve additional from source environment')
            sys.exit(1)
    #manipulate build.xml to get the target property file
    f = open(run_path+'\\src\/build.xml','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace((source+".properties"),(target+".properties"))
    f = open(run_path+'\\src\/build.xml','w')
    f.write(newdata)
    f.close()
    if os.path.exists(run_path+'\\src\/reference\\'+target+'_matching_package.xml'):
        tgt = os.system('ant retrieveTargetEnv')
        if tgt != 0: 
            print('Error on ant retrieve matching from target environment')
            sys.exit(1)
    if os.path.exists(run_path+'\\src\/reference\\'+target+'_additional_package.xml'):
        tgt_add = os.system('ant retrieveTargetAdd')
        if tgt_add != 0: 
            print('Error on ant retrieve additional from target environment')
            sys.exit(1)
    os.remove(run_path+'\\src\/build.xml')
    os.remove(run_path+'\\src\/reference\\'+source+'_matching_package.xml')
    os.remove(run_path+'\\src\/reference\\'+target+'_matching_package.xml')
    if os.path.exists(run_path+'\\src\/reference\\'+source+'_additional_package.xml'):
        os.remove(run_path+'\\src\/reference\\'+source+'_additional_package.xml')
    if os.path.exists(run_path+'\\src\/reference\\'+target+'_additional_package.xml'):
        os.remove(run_path+'\\src\/reference\\'+target+'_additional_package.xml')

    #build string for each dict and push it into different files
    result_path = run_path+'\\retrieve_compare\\'+source+' vs '+target
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    minor_result_path = result_path+'\\'+time.strftime("%d-%b-%Y")
    if not os.path.exists(minor_result_path):
        os.makedirs(minor_result_path)
    sub_result_path = minor_result_path+'\\retrieve'
    if not os.path.exists(sub_result_path):
        os.makedirs(sub_result_path)
    src_match_from = run_path+'\\src\\'+source+'_matching'
    dst = sub_result_path
    tgt_match_from = run_path+'\\src\\'+target+'_matching'
    #tgt_match_to = 	
    src_addtional_from = run_path+'\\src\\'+source+'_additional'
    #src_addtional_to = 
    tgt_addtional_from = run_path+'\\src\\'+target+'_additional'
    #tgt_addtional_to = 	
    
    if os.path.exists(src_match_from):
        shutil.move(src_match_from, dst)
    if os.path.exists(tgt_match_from):
        shutil.move(tgt_match_from, dst)
    if os.path.exists(src_addtional_from):
        shutil.move(src_addtional_from, dst)
    if os.path.exists(tgt_addtional_from):
        shutil.move(tgt_addtional_from, dst)

    o_src_match = sub_result_path+'\\'+source+'_matching'
    o_target_match = sub_result_path+'\\'+target+'_matching'
    return o_src_match,o_target_match


def retrieve_specific_env(run_path,source):
    #call(["cd","C:\mydata\Zurich Salesforce\Zurich Ant Deployment\Zurich Salesforce\All Components"])
    #subprocess.check_call(["ant", "retrieve"],cwd=in_path)

    os.chdir(run_path+'\\src')
    #manipulate build.xml to get the source property file
    f = open(run_path+'\\src\/reference\/reference_build.xml','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("[CUSTOM]",source)
    newdata = newdata.replace("[SOURCE]",source)
    f = open(run_path+'\\src\/build.xml','w')
    f.write(newdata)
    f.close()

    if os.path.exists(run_path+'\\src\/reference\\'+source+'_completepull_package.xml'):
        src = os.system('ant retrieve')
        if src != 0: 
           print('Error on ant retrieve matching from source environment')
           sys.exit(1)
    os.remove(run_path+'\\src\/build.xml')
    os.remove(run_path+'\\src\/reference\\'+source+'_completepull_package.xml')

    #build string for each dict and push it into different files
    result_path = run_path+'\\complete_pull\\'+source
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    sub_result_path = result_path+'\\'+time.strftime("%d-%b-%Y")
    if not os.path.exists(sub_result_path):
        os.makedirs(sub_result_path)
    src_retrieve_path = run_path+'\\src\\'+source+'_CompletePull'
    dst = sub_result_path	
    
    if os.path.exists(src_retrieve_path):
        shutil.move(src_retrieve_path, dst)