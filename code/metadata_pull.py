import sys
import SFSession as sess
import SFMetadata as meta
import configparser
from collections import defaultdict, OrderedDict

#runpath = sys.argv[1]
#env = sys.argv[2]


def getVarFromFile(filepath):
    config = configparser.ConfigParser()
    config.readfp(open(filepath))
    username = config.get('LOGIN', 'sf.username')
    password = config.get('LOGIN', 'sf.password')
    serverurl = config.get('LOGIN', 'sf.serverurl')
    return username, password, serverurl

def getCompFromFile(runpath):
    config = configparser.ConfigParser()
    filepath = runpath+'\src\\reference\\component_list.txt'
    config.read(filepath)
    use = config.get('COMPONENTS', 'use')
    component_list = ((config.get('COMPONENTS', use)[1:-1]).replace('\'','').replace('\n','')).split(',')
    return component_list

def metadata_pull(runpath,env,component_list):

    filepath = runpath+'/src/login_details/'+env+'.properties'

    username, password, serverurl = getVarFromFile(filepath)

    prod_url = 'login.salesforce.com'
	
    c_is_sandbox = True

    if( prod_url in serverurl):
        c_is_sandbox = False

    s = sess.SfdcSession(
        username = username,
        password = password,
        is_sandbox = True
    )
    s.login()

    metadata = meta.SfdcMetadataApi(s)

    all_components = defaultdict(list)


    for component in component_list:   
        l = []
        listContent = metadata.listMetadata(component, '37.0')
        if(isinstance(listContent, list)):       
            for each in listContent:
                for k, v in each.items():
                    if(k == 'fullName'):
                        l.append(v)
        elif(isinstance(listContent, dict)):       
            l.append(listContent['fullName'])
        elif(isinstance(listContent, str)):
            l.append(listContent)
        l.sort()
        all_components[component] = l

    component_dictionary = OrderedDict(sorted(all_components.items()))
    return component_dictionary