from .Definitions import Definitions
import numpy

class VariableLoader:

    '''
    Variable loader class. Does some checks and returns the requested variable as a NumPy array.
    '''

    def __init__(self,url,datasetName,DDS):

        # Get available DDS definitions
        self.url = url
        self.datasetName = datasetName
        self.DDS = DDS

    def GetRequestURL(self,varName,dimSels):

        '''
        The dimension selections (dimSels) variable must be a numpy ndarray, type int, size N by 3.
        Each row corresponds to one variable dimension, with columns containing the min, step and max indexes
        '''
        # Check variable exists and dimensions are not exceeded

        if varName not in self.DDS:
            print('VariableLoader: Requested variable not in DDS, stopping.')
            return None

        varDims = self.DDS[varName][1]
        numDims = len(varDims)
        if (numDims > 0) and (dimSels.shape[0] != numDims):
            print('VariableLoader: Requested number of dimensions incorrect, stopping.')
            return None

        # Extract dimension selections and check they're valid.

        dimsOK = True
        for d in range(numDims):
            if (dimSels[d,0] < 0) | (dimSels[d,1] < 0) | (dimSels[d,2] < 0): dimsOK = False
            if (dimSels[d,0] > varDims[d] - 1) | (dimSels[d,2] > varDims[d] - 1): dimsOK = False
            if (dimSels[d,2] < dimSels[d,0]): dimsOK = False
            if (dimSels[d,0] != dimSels[d,2]) and (dimSels[d,1] > dimSels[d,2]): dimsOK = False

        if not dimsOK:
            print('VariableLoader: At least one dimension selection request is not valid, stopping.')
            return None
        
        # Construct the request url
        
        requrl = self.url + '.dods?' + varName
        for d in range(numDims):
            dimstr = '[' + str(dimSels[d,0]) + ':' + str(dimSels[d,1]) + ':' + str(dimSels[d,2]) + ']'
            requrl += dimstr
            
        return requrl

    def LoadVariable(self,varName,varData,dimSels,byteOrdStr,checkType=True):

        '''
        Load the requested variable and return as a NumPy array.
        '''

        dims = False
        if dimSels.shape[1] == 3: dims = True # Otherwise size is [1,1] and contains number of elements in dimensionless data

        if dims:
            boffs = 8 # Byte offset for the two occurrences of the number of elements (int32)
        else:
            boffs = 4 # Offset for dimensionless data

        # Find the header portion of the byte stream (until the 'Data' identifier)

        dataId = 'Data:\n'.encode('utf-8')
        idLen = len(dataId)
        dataLen = len(varData)

        i = 0
        while (i < dataLen-idLen-1) and (varData[i:i+idLen] != dataId): i += 1
        if varData[i:i+idLen] != dataId:
            print('VariableLoader: Data start identifier not found, stopping.')
            return None

        dataStartInd = i + idLen
        dataStartInd += boffs

        # Check the varData byte stream contains the correct variable type
        hdrStr = varData[:dataStartInd - boffs].decode('utf-8')
        varType = self.DDS[varName][0]
        if checkType:
            if varType not in hdrStr:
                print('VariableLoader: Variable type in requested data header does not match DDS, stopping.')
                return None
            
        # Check the varData byte stream contains the correct variable dimensions

        assocNames = self.DDS[varName][2]
        dimStr = varName
        numEls = []
        if dims:
            for d in range(dimSels.shape[0]):
                count = 1
                ind = dimSels[d,0]
                while (ind < dimSels[d,2]):
                    ind += dimSels[d,1]
                    count += 1
                if (ind > dimSels[d,2]): count -= 1
                numEls.append(count)
                dimStr += '[' + assocNames[d] + ' = ' + str(numEls[d]) + ']'
        else:
            numEls = dimSels[0,0] # Number of elements to retrieve

        if dimStr not in hdrStr:
            print('VariableLoader: Variable dimensions in requested data header do not match DDS, stopping.')
            return None

        # All OK - load the variable

        npType = Definitions.atomics[varType]
        dataType = npType

        if len(byteOrdStr) > 0:
            dataType = npType.newbyteorder(byteOrdStr)

        lvar = numpy.frombuffer(varData,dtype=dataType,count=numpy.prod(numEls),offset=dataStartInd)
        if dims:
            var = lvar.reshape(tuple(numEls))
        else:
            var = lvar

        return var
