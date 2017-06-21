""" Class to work with Salesforce Metadata API """
from base64 import b64encode, b64decode
from xml.etree import ElementTree as ET
import xmltodict

#import sfdclib.messages as msg


class SfdcMetadataApi:
    """ Class to work with Salesforce Metadata API """
    _METADATA_API_BASE_URI = "/services/Soap/m/{version}"
    _XML_NAMESPACES = {
        'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
        'mt': 'http://soap.sforce.com/2006/04/metadata'
    }

    def __init__(self, session):
        if not session.is_connected():
            raise Exception("Session must be connected prior to instantiating this class")
        self._session = session
        self._deploy_zip = None

    def _get_api_url(self):
        return "%s%s" % (
            self._session.get_server_url(),
            self._METADATA_API_BASE_URI.format(**{'version': self._session.get_api_version()}))

    def retrieve(self, options):
        """ Submits retrieve request """
        # Compose unpackaged XML
        unpackaged = ''
        for metadata_type in options['unpackaged']:
            members = options['unpackaged'][metadata_type]
            unpackaged += '<types>'
            for member in members:
                unpackaged += '<members>{0}</members>'.format(member)
            unpackaged += '<name>{0}</name></types>'.format(metadata_type)
        return unpackaged
		
    def listMetadata(self, metaType, asOfVersion):
        headers = {'content-type': 'text/xml', 'SOAPAction': 'retrieve'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">
         <soapenv:Header>
            <met:CallOptions>
            </met:CallOptions>
            <met:SessionHeader>
               <met:sessionId>""" + self._session.get_session_id() + """</met:sessionId>
            </met:SessionHeader>
         </soapenv:Header>
         <soapenv:Body>
            <met:listMetadata>
               <!--Zero or more repetitions:-->
               <met:queries>
                  <!--Optional:-->
                  <!--<met:folder>null</met:folder>-->
                  <met:type>""" + metaType + """</met:type>
               </met:queries>
               <met:asOfVersion>""" + asOfVersion + """</met:asOfVersion>
            </met:listMetadata>
         </soapenv:Body>
      </soapenv:Envelope>"""
        response = self._session.post(self._get_api_url(), data=body, headers=headers)
        listOfResult = xmltodict.parse(response.content)
        if('soapenv:Fault' in (listOfResult['soapenv:Envelope']['soapenv:Body'])):
            output = 'REMOVE: ' + listOfResult['soapenv:Envelope']['soapenv:Body']['soapenv:Fault']['faultstring']
        else:
            if(isinstance((listOfResult['soapenv:Envelope']['soapenv:Body'][u'listMetadataResponse']),(list,dict))):
                output = listOfResult['soapenv:Envelope']['soapenv:Body'][u'listMetadataResponse'][u'result']
            else:
                output = 'REMOVE: No Components available'
        return output