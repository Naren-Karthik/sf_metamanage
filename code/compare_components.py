import os
import time
from collections import defaultdict, OrderedDict

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def matched(self):
        return self.intersect
    def src_additional(self):
        return self.set_current - self.intersect 
    def tgt_additional(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
    
class ListDiffer(object):
    def __init__(self, list1, list2):
        self.set_list1, self.set_list2 = set(list1), set(list2)
        self.intersect = self.set_list1.intersection(self.set_list2)
    def matched(self):
        return self.intersect
    def src_additional(self):
        return self.set_list1 - self.intersect 
    def tgt_additional(self):
        return self.set_list2 - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.list2[o] != self.list1[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.list2[o] == self.list1[o])
        

def compare(run_path,source,target,source_dict,target_dict,component_list):
    
    wildcard_component = {'ActionLinkGroupTemplate': 'Y','ApexClass': 'Y','ApexComponent': 'Y','ApexPage': 'Y','ApexTrigger': 'Y','AppMenu': 'Y','ApprovalProcess': 'Y','ArticleType': 'Y','AssignmentRules': 'Y',
        'AuthProvider': 'Y','AuraDefinitionBundle': 'Y','AutoResponseRules': 'Y','BaseSharingRule': 'Y','CallCenter': 'Y','Certificate': 'Y','CleanDataService': 'Y','Community (Zone)': 'Y','CommunityTemplateDefinition': 'Y',
        'CommunityThemeDefinition': 'Y','CompactLayout': 'Y','ConnectedApp': 'Y','ContentAsset': 'Y','CorsWhitelistOrigin': 'Y','CriteriaBasedSharingRule': 'Y','CustomApplication': 'Y','CustomApplicationComponent': 'Y',
        'CustomFeedFilter': 'Y','Custom Metadata Types (CustomObject)': 'Y','CustomMetadata': 'Y','CustomLabels': 'Y','CustomObjectTranslation': 'Y','CustomPageWebLink': 'Y','CustomPermission': 'Y','CustomSite': 'Y',
        'CustomTab': 'Y','DataCategoryGroup': 'Y','DelegateGroup': 'Y','DuplicateRule': 'Y','EntitlementProcess': 'Y','EntitlementTemplate': 'Y','EventDelivery': 'Y','EventSubscription': 'Y','ExternalDataSource': 'Y',
        'FieldSet': 'Y','FlexiPage': 'Y','Flow': 'Y','FlowDefinition': 'Y','GlobalValueSet': 'Y','GlobalValueSetTranslation': 'Y','Group': 'Y','HomePageComponent': 'Y','HomePageLayout': 'Y','InstalledPackage': 'Y',
        'KeywordList': 'Y','Layout': 'Y','LiveChatAgentConfig': 'Y','LiveChatButton': 'Y','LiveChatDeployment': 'Y','LiveChatSensitiveDataRule': 'Y','ManagedTopics': 'Y','MatchingRule': 'Y','MilestoneType': 'Y',
        'ModerationRule': 'Y','NamedCredential': 'Y','Network': 'Y','OwnerSharingRule': 'Y','PathAssistant': 'Y','PermissionSet': 'Y','PlatformCachePartition': 'Y','Portal': 'Y','PostTemplate': 'Y','Profile': 'Y','Queue': 'Y',
        'QuickAction': 'Y','ReportType': 'Y','Role': 'Y','SamlSsoConfig': 'Y','Scontrol': 'Y','SharingRules': 'Y','SharingSet': 'Y','SiteDotCom': 'Y','Skill': 'Y','StandardValueSetTranslation': 'Y','StaticResource': 'Y',
        'SynonymDictionary': 'Y','Territory': 'Y','Territory2': 'Y','Territory2Model': 'Y','Territory2Rule': 'Y','Territory2Type': 'Y','TransactionSecurityPolicy': 'Y','Translations': 'Y','WaveApplication': 'Y',
        'WaveDashboard': 'Y','WaveDataflow': 'Y','WaveDataset': 'Y','WaveLens': 'Y','WaveTemplateBundle': 'Y','Workflow': 'Y'}
		
    matching = defaultdict(list)
    source_additional = defaultdict(list)
    target_additional = defaultdict(list)
    #print(source_dict)
    #print(target_dict)
    
    #compare keys 
    d = DictDiffer(source_dict,target_dict)
    #For mismatching keys put in source_additional and target_additional
    for s in d.src_additional():
        if(len(source_dict[s]) == 1):
            if('REMOVE: ' not in str(source_dict[s])):
                source_additional[s] = source_dict[s]
        elif(len(source_dict[s]) > 1):
            sa = []
            for r in source_dict[s]:
                if('REMOVE: ' not in str(r)):
                    sa.append(r)
            sa.sort()
            source_additional[s] = sa
    for s in d.tgt_additional():
        if(len(target_dict[s]) == 1):
            if('REMOVE: ' not in str(target_dict[s])):
                target_additional[s] = target_dict[s]
        elif(len(source_dict[s]) > 1):
            ta = []
            for r in target_dict[s]:
                if('REMOVE: ' not in str(r)):
                    ta.append(r)
            ta.sort()
            target_additional[s] = ta
    #For matching keys check each value in the lists of values for each keys
    for s in d.matched():
        m = []
        sa = []
        ta = []
        slist = []
        tlist = []        
        slist = source_dict[s]
        tlist = target_dict[s]
        l = ListDiffer(slist,tlist)
        #For matching values put it in matching dict
        for v in l.matched():
            if('REMOVE: ' not in str(v)):
                m.append(v)
        #For not additional values check if it is in source or target and put it in accordingly
        for v in l.src_additional():
            if('REMOVE: ' not in str(v)):
                sa.append(v)
        for v in l.tgt_additional():
            if('REMOVE: ' not in str(v)):
                ta.append(v)
        m.sort()
        sa.sort()
        ta.sort()
        if(len(m) > 0):
            matching[s] = m
        if(len(sa) > 0):
            source_additional[s] = sa
        if(len(ta) > 0):
            target_additional[s] = ta

    '''for comp in component_list:
        if((comp in matching and comp not in source_additional and comp in wildcard_component) or (comp in matching and comp not in target_additional and comp in wildcard_component)):
            del matching[comp]
            matching[comp] = ['*']'''

    o_matching = OrderedDict(sorted(matching.items()))
    o_source_additional = OrderedDict(sorted(source_additional.items()))
    o_target_additional = OrderedDict(sorted(target_additional.items()))    
	
    #build string for each dict and push it into different files
    result_path = run_path+'\\retrieve_compare\\'+source+' vs '+target
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    minor_result_path = result_path+'\\'+time.strftime("%d-%b-%Y")
    if not os.path.exists(minor_result_path):
        os.makedirs(minor_result_path)
    sub_result_path = minor_result_path+'\\Comparison Result - '+source+' vs '+target
    if not os.path.exists(sub_result_path):
        os.makedirs(sub_result_path)
	
    match_filepath = sub_result_path+'\\'+source+' vs '+target+'_match.txt'
    if not o_matching:
        m_unpackaged = 'No matching components between '+source+' and '+target+'.'
    else:
        m_unpackaged = 'Matching components in '+source+' & '+target+'\n'
        for k in o_matching:
            m_unpackaged += '--------------------------------------------------------------------------------------\n'
            m_unpackaged += k+'\n'
            m_unpackaged += '--------------------------------------------------------------------------------------\n'
            for v in o_matching[k]:
                m_unpackaged += v+'\n'
            m_unpackaged += '\n--------------------------------------------------------------------------------------'
    f = open(match_filepath,'w')
    f.write(m_unpackaged)
    f.close()

    src_addl_filepath = sub_result_path+'\\'+source+'_additional.txt'
    if not o_source_additional:
        sa_unpackaged = 'No additional components in '+source+'.'
    else:
        sa_unpackaged = 'Additional components in '+source+'\n'
        for k in o_source_additional:
            sa_unpackaged += '--------------------------------------------------------------------------------------\n'
            sa_unpackaged += k+'\n'
            sa_unpackaged += '--------------------------------------------------------------------------------------\n'
            for v in o_source_additional[k]:
                sa_unpackaged += v+'\n'
            sa_unpackaged += '\n--------------------------------------------------------------------------------------'
    f = open(src_addl_filepath,'w')
    f.write(sa_unpackaged)
    f.close()
    
    tgt_addl_filepath = sub_result_path+'\\'+target+'_additional.txt'
    if not o_target_additional:
        ta_unpackaged = 'No additional components in '+target+'.'
    else:
        ta_unpackaged = 'Additional components in '+target+'\n'
        for k in o_target_additional:
            ta_unpackaged += '--------------------------------------------------------------------------------------\n'
            ta_unpackaged += k+'\n'
            ta_unpackaged += '--------------------------------------------------------------------------------------\n'
            for v in o_target_additional[k]:
                ta_unpackaged += v+'\n'
            ta_unpackaged += '\n--------------------------------------------------------------------------------------'
    f = open(tgt_addl_filepath,'w')
    f.write(ta_unpackaged)
    f.close()
	
    return o_matching, o_source_additional, o_target_additional