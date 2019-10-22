import requests
from xml.etree import ElementTree
import urllib.parse
import unicodedata


class Authority:
    OAUTH_HOST = 'worldcat.org'
    OAUTH_ROOT = '/identities/'
    
    def __init__(self, author):
        """
        Authority search
        
        :param author: not normalized author name
        """
        self.name = author
        self.fixed_name = None
        self.quote_name = None
        self.finded = None
        self.established_form = None
        self.uri = None
    
    
    def __strip_accents__(self):
        try:
            self.fixed_name = unicode(self.name, 'utf-8')
        except NameError:
            pass
        
        self.fixed_name = unicodedata.normalize('NFD', self.name).encode('ascii', 'ignore').decode('utf-8')
    
    def search(self):
        self.__strip_accents__()
        self.quote_name = urllib.parse.quote(self.fixed_name)
        find_response = requests.get('https://' + self.OAUTH_HOST + self.OAUTH_ROOT + 'find?fullName=' + self.quote_name + '&maxList=100')
        xml_tree = ElementTree.fromstring(find_response.content)
        
        # is there any result?
        if(int(xml_tree.attrib['hitCount']) > 0):
            # is there any personal identifier?
            if(any(xml_tree.findall('.//match[nameType="personal"]'))):
                # get name and uri from first correct result
                self.finded = True
                self.established_form = xml_tree.findall('.//match[nameType="personal"]/establishedForm')[0].text
                self.uri = xml_tree.findall('.//match[nameType="personal"]/uri')[0].text
                
                return [self.established_form, self.uri]
            else:
                self.finded = False
                return None
        else:
            self.finded = False
            return None
        
        
class AuthorityData(Authority):
    OAUTH_HOST = 'worldcat.org'
    def __init__(self, name):
        super().__init__(name)
        self.tree = None
        self.languages_total = None
        self.total_holdings = None
        self.work_count = None
        self.record_count = None
        self.languages = None
        self.works = {'0' : ['title', 'language', 'holdings', 'editions', 'type']}
    
    def data(self):
        if(self.finded == None):
            self.search()
        
        if(self.finded == True):
            response = requests.get('https://' + self.OAUTH_HOST + self.uri + '/identity.xml')
            self.tree = ElementTree.fromstring(response.content)
            # general
            self.languages_total = self.tree.find('nameInfo/languages').attrib['count']
            self.total_holdings = self.tree.find('nameInfo/totalHoldings').text
            self.work_count = self.tree.find('nameInfo/workCount').text
            self.record_count = self.tree.find('nameInfo/recordCount').text
            # specific
            self.languages = [[self.tree.findall('nameInfo/languages/lang')[i].attrib['code'],self.tree.findall('nameInfo/languages/lang')[i].attrib['count']] for i in range(len(self.tree.findall('nameInfo/languages/lang')))]
            # works
            for i in range(len(self.tree.findall('by/citation'))):
                self.works[str(i + 1)] = [self.tree.findall('by/citation')[i].find('title').text,
                           self.tree.findall('by/citation')[i].find('languages').attrib['count'],
                           self.tree.findall('by/citation')[i].find('holdings').text,
                           self.tree.findall('by/citation')[i].find('numEditions').text,
                           self.tree.findall('by/citation')[i].find('recordType').text]
