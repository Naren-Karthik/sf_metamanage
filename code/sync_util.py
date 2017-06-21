import re
import sys
import time
import os as os
import os.path as op
import difflib
from collections import defaultdict, OrderedDict

def checkifone(string, char):
    return len(string.split(char)) == 2;

def get_file_dict(root_path):
    #for root, dirs, files in os.walk(root_path):
    dirs = [f for f in os.listdir(root_path) if(op.isdir(op.join(root_path, f)))]
    file_dict = defaultdict(list)
    for name in dirs:
        dir_path = root_path+'/'+str(name)+'/'
        file_list = [f for f in os.listdir(dir_path) if (op.isfile(op.join(dir_path, f)) and not(str(f).lower().endswith('.xml') or checkifone(str(f).lower(),'__')))]
        file_list.sort()
        file_dict[name] = file_list
    o_file_dict = OrderedDict(sorted(file_dict.items()))
    return o_file_dict
               
def compare_files(file1,file2):
    lines = []
    match = True
    
    try:
        lines1 = file1.read().strip().splitlines()

        lines2 = file2.read().strip().splitlines()

        for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
            lines.append(line)
            if(len(lines) > 0):
                match = False
                break
    except:
        #do nothing
        match = True
    return match

def sync_compare(run_path,source,target,src_path,target_path):

    comp_dict = get_file_dict(src_path)
    in_sync_dict = defaultdict(list)
    out_sync_dict = defaultdict(list)
    
    for comp_name in comp_dict:
        in_sync_list = []
        out_sync_list = []
        for comp in comp_dict[comp_name]:
            file1 = open(src_path+'/'+comp_name+'/'+comp,'r',encoding='utf8')
            file2 = open(target_path+'/'+comp_name+'/'+comp,'r',encoding='utf8')
            CONDITION = compare_files(file1,file2)
            file1.close()
            file2.close()
            if(CONDITION):
                in_sync_list.append(comp)
            else:
                out_sync_list.append(comp)
        in_sync_list.sort()
        out_sync_list.sort()
        in_sync_dict[comp_name] = in_sync_list
        out_sync_dict[comp_name] = out_sync_list
    o_in_sync_dict = OrderedDict(sorted(in_sync_dict.items()))
    o_out_sync_dict = OrderedDict(sorted(out_sync_dict.items()))

    result_path = run_path+'\\retrieve_compare\\'+source+' vs '+target
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    minor_result_path = result_path+'\\'+time.strftime("%d-%b-%Y")
    if not os.path.exists(minor_result_path):
        os.makedirs(minor_result_path)
    sub_result_path = minor_result_path+'\\Comparison Result - '+source+' vs '+target
    if not os.path.exists(sub_result_path):
        os.makedirs(sub_result_path)

    in_sync_path = sub_result_path+'\\'+source+' vs '+target+'_match & In-sync.txt'
    if not o_in_sync_dict:
        m_unpackaged = 'No matching components between '+source+' and '+target+'.'
    else:
        m_unpackaged = 'Matching & In-sync components in '+source+' & '+target+'\n'
        for k in o_in_sync_dict:
            if(len(o_in_sync_dict[k]) > 0):
                m_unpackaged += '--------------------------------------------------------------------------------------\n'
                m_unpackaged += k+'\n'
                m_unpackaged += '--------------------------------------------------------------------------------------\n'
                for v in o_in_sync_dict[k]:
                    m_unpackaged += v+'\n'
                m_unpackaged += '\n--------------------------------------------------------------------------------------'
    f = open(in_sync_path,'w')
    f.write(m_unpackaged)
    f.close()

    out_sync_path = sub_result_path+'\\'+source+' vs '+target+'_match & Out-of-sync.txt'
    if not o_out_sync_dict:
        m_unpackaged = 'No matching components between '+source+' and '+target+'.'
    else:
        m_unpackaged = 'Matching & Out-of-sync components in '+source+' & '+target+'\n'
        for k in o_out_sync_dict:
            if(len(o_out_sync_dict[k]) > 0):
                m_unpackaged += '--------------------------------------------------------------------------------------\n'
                m_unpackaged += k+'\n'
                m_unpackaged += '--------------------------------------------------------------------------------------\n'
                for v in o_out_sync_dict[k]:
                    m_unpackaged += v+'\n'
                m_unpackaged += '\n--------------------------------------------------------------------------------------'
    f = open(out_sync_path,'w')
    f.write(m_unpackaged)
    f.close()

    match_filepath = sub_result_path+'\\'+source+' vs '+target+'_match.txt'
    os.remove(match_filepath)
    print('Done')
