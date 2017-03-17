class Parser:

    '''
    Serves as base class for DDSParser and DASParser classes.
    '''

    def __init__(self):

        self.Type = 'Undefined'; # Name of parsed dataset (e.g. DDS, DAS)
        self.Data = {} # Data dictionary
        self.indts = [] # Indentation list
        self.dataLines = [] # List of lines in data to be parsed
        self.lnum = 0 # Current line number
        self.Finished = False # Flag to indicate parsing complete

    def FindStart(self,DataStr,StartStr):

        # Remove any empty lines
        tempLines = DataStr.split('\n')
        for l in tempLines:
            if len(l) > 0: self.dataLines.append(l)

        # Loop to find start of dataset
        while StartStr not in self.dataLines[self.lnum]:
            if self.lnum == len(self.dataLines) - 1:
                print('Parser: No datasets found, stopping.')
                break
            self.lnum += 1

        if self.lnum < len(self.dataLines) - 1: # Get root indentation level and store in list
            self.indts.append(self.FindIndentLevel(self.dataLines[self.lnum]))
    
    def FindIndentLevel(self,line):

        i = 0
        if len(line) > 0:
            el = line.split()[0] # First element
            while line[i:i+len(el)] != el: i += 1
        return i

    def CheckLine(self):

        doLine = True

        self.lnum += 1
        indt = self.FindIndentLevel(self.dataLines[self.lnum])

        if indt > self.indts[-1]: # Indentation increased: expecting new variable
            self.indts.append(indt)
        elif indt < self.indts[-1]: # Indentation decreased: end of current body
            while (len(self.indts) > 0) & (indt < self.indts[-1]): self.indts.pop()
            doLine = False
            if len(self.indts) == 1: # Back to the root level so must be finished
                self.Finished = True

        return doLine

    def PrintData(self,Type,Data): # Type and Data can be passed in externally for convenience
        print('Type :',Type,'\n')
        if len(Data) == 0:
            print('Structure is not defined')

    def PrintDataToFile(self,Type,Data,fi): # Type, Data and file object can be passed in externally for convenience
        fi.write('Type :' + Type + '\n\n')
        if len(Data) == 0:
            fi.write('Structure is not defined\n')
