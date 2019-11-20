import requests
from lxml import etree
#from lxml.html import soupparser #html
import urllib.parse
import unicodedata


class Authority:
    OAUTH_HOST = 'worldcat.org'
    OAUTH_ROOT = '/identities/'
    
    def __init__(self, name):
        """
        Authority search
        
        :param name: not normalized author name
        """
        self.name = name
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
        return self
    
    def search(self):
        self.__strip_accents__()
        self.quote_name = urllib.parse.quote(self.fixed_name)
        find_response = requests.get('https://' + self.OAUTH_HOST + self.OAUTH_ROOT + 'find?fullName=' + self.quote_name + '&maxList=25')
        if find_response.status_code == 200:
            try:
                xml_tree = etree.fromstring(find_response.content)
            except:
                # in case of unescaped characters
                xml_tree = etree.fromstring(find_response.content, parser = etree.XMLParser(recover = True))
            # is there any result?
            if int(xml_tree.attrib['hitCount']) > 0:
                # is there any personal identifier?
                #if any(xml_tree.findall('.//match[nameType="personal"]')):
                if len([i for i in xml_tree.findall('.//match[nameType="personal"]')]) > 0: # to avoid lxml warning
                    # get name and uri from first correct result
                    self.finded = True
                    self.established_form = xml_tree.findall('.//match[nameType="personal"]/establishedForm')[0].text
                    self.uri = xml_tree.findall('.//match[nameType="personal"]/uri')[0].text
                else:
                    self.finded = False              
            else:
                self.finded = False
        else:
            None
        return self  
        
class AuthorityData(Authority):
    OAUTH_HOST = 'worldcat.org'
    def __init__(self, name = None, uri = None):
        super().__init__(name)
        self.uri = '/identities/' + uri if uri is not None else None
        self.tree = None
        self.languages_total = None
        self.total_holdings = None
        self.work_count = None
        self.record_count = None
        self.languages = None
        self.works = {'0' : ['title', 'language', 'holdings', 'editions', 'type']}
    
    def data(self):
        if self.finded == None and self.uri == None:
            self.search()
        
        if self.finded == True or self.uri is not None:
            response = requests.get('https://' + self.OAUTH_HOST + self.uri + '/identity.xml')
            try:
                self.tree = etree.fromstring(response.content)
            except:
                self.tree = etree.fromstring(response.content, parser = etree.XMLParser(recover = True))
            # only by uri
            if self.established_form == None:
                self.established_form = ' '.join([subname.text for subname in self.tree.find('nameInfo/rawName').getchildren()])
            # general
            self.languages_total = self.tree.find('nameInfo/languages').attrib['count']
            self.total_holdings = self.tree.find('nameInfo/totalHoldings').text
            self.work_count = self.tree.find('nameInfo/workCount').text
            self.record_count = self.tree.find('nameInfo/recordCount').text
            # specific
            self.languages = [[self.tree.findall('nameInfo/languages/lang')[i].attrib['code'],self.tree.findall('nameInfo/languages/lang')[i].attrib['count']] for i in range(len(self.tree.findall('nameInfo/languages/lang')))]
            # works
            #for i in range(len(self.tree.findall('by/citation'))):
            for i in range(len([i for i in self.tree.findall('by/citation')])): # to avoid lxml warning
                self.works[str(i + 1)] = [self.tree.findall('by/citation')[i].find('title').text,
                           self.tree.findall('by/citation')[i].find('languages').attrib['count'],
                           self.tree.findall('by/citation')[i].find('holdings').text,
                           self.tree.findall('by/citation')[i].find('numEditions').text,
                           self.tree.findall('by/citation')[i].find('recordType').text]
        return self

