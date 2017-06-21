def buildpackage(run_path,components,env,q_str):

    unpackaged = '<?xml version="1.0" encoding="UTF-8"?>\n<Package xmlns="http://soap.sforce.com/2006/04/metadata">\n\n'
    #print(components)
    if not components:
        print('No component to build package')
    else:
        for k in components:
            if(len(components[k]) > 1):
                unpackaged += '<types>\n'
                for v in components[k]:
                    if('REMOVE:' not in v):
                        unpackaged += '<members>{0}</members>'.format(v)+'\n'
                unpackaged += '<name>{0}</name>'.format(k)+'\n'
                unpackaged += '</types>\n'
                unpackaged += '\n'
            elif(len(components[k]) == 1):
                if('REMOVE:' not in str(components[k])):
                    unpackaged += '<types>\n'
                    unpackaged += '<members>{0}</members>'.format(components[k][0])+'\n'
                    unpackaged += '<name>{0}</name>'.format(k)+'\n'
                    unpackaged += '</types>\n'
                    unpackaged += '\n'             
        unpackaged +=  '''<version>37.0</version></Package>'''
        filepath = run_path+'\\src\/reference\\'+env+'_'+q_str+'_package.xml'
        f = open(filepath,'w')
        f.write(unpackaged)
        f.close()