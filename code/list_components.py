#!/usr/bin/python

import sys
import os as os
import os.path as op


in_path = sys.argv[1]

sub_dirs = [f for f in os.listdir(in_path) if(op.isdir(op.join(in_path, f)))]

for s in sub_dirs:
    sub_path = in_path+'/'+s+'/'
    sub_dir_list_name = s+'_list'
    sub_dir_list_name = [f for f in os.listdir(sub_path) 
                         if (op.isfile(op.join(sub_path, f)) and not(str(f).lower().endswith('.xml')))]
    sub_sub_dirs = [f for f in os.listdir(sub_path) if(op.isdir(op.join(sub_path, f)))]
    print(s)
    print('-----------------')
    for l in sub_dir_list_name:
        print(l)
    print('\n')
    for ss in sub_sub_dirs:
        sub_sub_path = sub_path+ss+'/'
        sub_sub_dir_list_name = s+' - '+ss+'_list'
        sub_sub_dir_list_name = [f for f in os.listdir(sub_sub_path) 
                                 if (op.isfile(op.join(sub_sub_path, f)) and not(str(f).lower().endswith('.xml')))]
        print((s+' >> '+ss))
        print('-----------------')
        for m in sub_sub_dir_list_name:
            print(m)
        print('\n')