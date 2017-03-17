from .Parser import Parser
from .Definitions import Definitions

class DDSParser(Parser):

    '''
    Dataset Descriptor Response (DDS) parser class.
    
    Given a DDS string read from a URL, it parses the string to set up a DDS dictionary. The dictionary is of form:
    {name : [type, [dims], [assocNames]]}
    where name is the variable name,
    dims is a list of dimensions,
    assocNames is a list of associated names.
    
    See Handler class for comments on constructor handling.
    
    A single data set is included, i.e. if the URL describes more than one, only the first will be included.
    '''

    def __init__(self):
        
        super().__init__()
        self.Type = 'Dataset Descriptor Structure (DDS)'

        self.atomicDefs = list(Definitions.atomics.keys())
        self.constructorDefs = Definitions.constructors

        self.datasetName = 'Undefined'

    def Parse(self,DDSstr):

        self.FindStart(DDSstr,Definitions.dataset)

        # Main loop
        while (not self.Finished) and (self.lnum < len(self.dataLines) - 1) and (len(self.indts) > 0):
            doLine = self.CheckLine()
            if doLine: self.ProcessLine()

        if self.Finished: self.datasetName = self.dataLines[self.lnum].split()[-1][:-1] # Exclude trailing semicolon

    def ProcessLine(self):
        varType = None
        nextLine = self.dataLines[self.lnum]
        segs = nextLine.split()
        for d in self.atomicDefs:
            if segs[0] == d:
                varType = d
                self.ReadAtomic(nextLine,varType)
                break
        if varType == None: # Not an atomic type
            for d in self.constructorDefs:
                if segs[0] == d:
                    varType = d
                    self.ReadConstructor(nextLine,varType)
                    break

    def ReadAtomic(self,line,varType):
        varName = line.split()[1].split('[')[0] # Will still work even if dimensionless
        segs = line.split('=')
        numDims = len(segs) - 1
        if numDims == 0: varName = varName[:-1] # Remove trailing semicolon
        dims = [None]*numDims
        assocNames = [None]*numDims
        for s in range(numDims):
            assocNames[s] = segs[s].split('[')[-1][:-1] # Remove trailing space
            dims[s] = int(segs[s+1].split(']')[0])
        self.Data[varName]=[varType,dims,assocNames]

    def ReadConstructor(self,line,varType): # Not implemented (all variables handled as atomics)
        pass

    def PrintDDS(self,datasetName = None,DDS = None): # Dataset name and DDS can be passed in externally for convenience
        if datasetName is None: datasetName = self.datasetName
        if DDS is None: DDS = self.Data
        self.PrintData(self.Type,DDS)
        print('Dataset name :',datasetName,'\n')
        for var in DDS.keys():
            print('Variable name :',var)
            print('Type :',DDS[var][0])
            print('Dimensions :',DDS[var][1])
            print('Associated names :',DDS[var][2],'\n')

    def PrintDDSToFile(self,fileName,datasetName = None,DDS = None): # Dataset name and DDS can be passed in externally for convenience
        if datasetName is None: datasetName = self.datasetName
        if DDS is None: DDS = self.Data
        self.PrintDataToFile(self.Type,DDS,fileName)
        fileName.write('Dataset name : ' + datasetName + '\n\n')
        for var in DDS.keys():
            fileName.write('Variable name : ' + var + '\n')
            fileName.write('Type : ' + DDS[var][0] + '\n')
            fileName.write('Dimensions : ' + str(DDS[var][1]) + '\n')
            fileName.write('Associated names : ' + str(DDS[var][2]) + '\n\n')
