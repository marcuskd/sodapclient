from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import urllib.request as ureq
from datetime import datetime

from .ProxyDict import ProxyDict
from .DDSParser import DDSParser
from .DASParser import DASParser
from .VariableLoader import VariableLoader

class Handler:

    '''
    The main sodapclient class.

    Both atomic variables and constructor variables are handled. Note that map vectors within constructors are treated
    as atomic variables. This means that existing variable names will be overwritten whenever they are repeated
    (whether atomic variables or map vectors within a constructor). E.g. if a Grid contains an atomic N-dimensional array
    it will be included in the returned DDS and the variable will be loaded but any map vectors with the same name as an
    existing atomic variable will overwrite the existing variable. Therefore the implementation will work provided
    map vectors defined within a constructor are identical to any variable with the same name defined outside the constructor.
    This should not be a limitation as all OpenDAP datasets seem to adhere to this anyway.
    '''

    def __init__(self,url,proxyFileName = None,log = False):

        self.logFile = None
        if log:
            logFileName = '/var/tmp/sodapclient-log-' + str(datetime.now().timestamp()) + '.txt'
            self.logFile = open(logFileName,'wt')
            self.logFile.write('sodapclient created at ' + str(datetime.now()) + '\n\n')

        # Set up the proxy (if required)
        if proxyFileName is not None:
            self.proxyDict = ProxyDict(proxyFileName)
            self.SetUpProxy()
            if self.logFile: self.logFile.write('Using Proxy Server.\n')

        # Check the URL is valid
        urlVal = URLValidator()
        try:
            urlVal(url)
        except ValidationError:
            msg = 'ERROR: Invalid URL format\n'
            if self.logFile: self.logFile.write(msg)
            print(msg)
            raise

        self.baseURL = url
        if self.baseURL[-4:] == 'html': # Need to remove .html extension if present
            self.baseURL = self.baseURL[:-5]

        if self.logFile: self.logFile.write('Base URL: ' + self.baseURL + '\n')

        # Set up the DDS
        self.GetDDS()

        # Set up the DAS
        self.GetDAS()

        # Set up the (initially empty) variables dictionary
        self.variables = {} # Dictionary to hold loaded variables

    def __del__(self):

        if self.logFile:
            self.logFile.write('\nHandler destroyed at ' + str(datetime.now()) + '\n\n')
            self.logFile.close()

    def SetUpProxy(self):
        proxyHandler = ureq.ProxyHandler(self.proxyDict.GetDict())
        opener = ureq.build_opener(proxyHandler)
        ureq.install_opener(opener)

    def GetDDS(self): # Get the Dataset Descriptor Structure (DDS)
        turl = self.baseURL + '.dds'
        try:
            u = ureq.urlopen(turl)
        except ureq.HTTPError:
            self.DDS = None
            return
        DDSstr = u.read().decode('utf-8')
        u.close()
        ddsParser = DDSParser()
        ddsParser.Parse(DDSstr)
        self.datasetName = ddsParser.datasetName
        self.DDS = ddsParser.Data
        if self.logFile:
            self.logFile.write('\n--- DDS ---\n\n')
            ddsParser.PrintDDSToFile(self.logFile)

    def GetDAS(self): # Get the Dataset Attribute Structure (DAS)
        turl = self.baseURL + '.das'
        try:
            u = ureq.urlopen(turl)
        except ureq.HTTPError:
            self.DAS = None
            return
        DASstr = u.read().decode('utf-8')
        u.close()
        dasParser = DASParser()
        dasParser.Parse(DASstr)
        self.DAS = dasParser.Data
        if self.logFile:
            self.logFile.write('--- DAS ---\n\n')
            dasParser.PrintDASToFile(self.logFile)
            self.logFile.write('-----------\n\n')

    def GetVariable(self,varName,dimSels,byteOrdStr,checkType=True):
        varLoader = VariableLoader(self.baseURL,self.datasetName,self.DDS)
        requrl = varLoader.GetRequestURL(varName,dimSels)
        if requrl != None:
            with ureq.urlopen(requrl) as u:
                varData = u.read()
            var = varLoader.LoadVariable(varName,varData,dimSels,byteOrdStr,checkType)
            if var is not None:
                self.variables[varName] = var

    def PrintStatus(self):
        print('HANDLER STATUS...\n')
        print('Base URL:',self.baseURL,'\n')
        print('DDS:\n')
        p = DDSParser() # Temporary object - just need printing function
        p.PrintDDS(self.datasetName,self.DDS)
        print('DAS:\n')
        p = DASParser() # Temporary object - just need printing function
        p.PrintDAS(self.DAS) # Convenience instantiation just to print DDS

    def Print(self):
        self.PrintStatus()
        print('VARIABLES...\n')
        if len(self.variables) > 0:
            print('Variables loaded:\n')
            for v in self.variables.keys():
                print('Variable name :',v)
                print('Loaded dimensions :',self.variables[v].shape)
                print('Data...')
                print(self.variables[v])
        else:
            print('No variables loaded.')
