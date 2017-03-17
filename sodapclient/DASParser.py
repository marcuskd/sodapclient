from .Parser import Parser
from .Definitions import Definitions

class DASParser(Parser):

    '''
    DASParser class. Extracts and stores the attributes within a DAS string.
    '''

    def __init__(self):

        super().__init__()
        self.Type = 'Dataset Attribute Structure (DAS)'

    def Parse(self,DASstr):

        self.FindStart(DASstr,Definitions.attributes)
        
        attrInd = -1 # Attribute index counter
        
        # Main loop
        while (not self.Finished) & (self.lnum < len(self.dataLines) - 1) & (len(self.indts) > 0):
            doLine = self.CheckLine()
            if doLine: # New Attribute
                    attrInd += 1
                    attrName = self.dataLines[self.lnum].split()[0]
                    attrdata = []
                    while (self.CheckLine()):
                        attrdata.append(self.dataLines[self.lnum].lstrip()[:-1]) # Remove trailing semicolon
                    self.Data[attrName] = attrdata

    def PrintDAS(self,DAS = None):
        if DAS is None: DAS = self.Data
        self.PrintData(self.Type,DAS)
        for var in DAS.keys():
            print('Variable :',var)
            print('Attributes...')
            for l in DAS[var]:
                print(l)
            print()

    def PrintDASToFile(self,fileName,DAS):
        if DAS is None: DAS = self.Data
        self.PrintDataToFile(self.Type,DAS,fileName)
        for var in DAS.keys():
            fileName.write('Variable : ' + var + '\n')
            fileName.write('Attributes...\n')
            for l in DAS[var]:
                fileName.write(l + '\n')
            fileName.write('\n')
