'''
Test class for Parser class.
'''

import unittest
from ..VariableLoader import VariableLoader
import numpy

class TestVariableLoader(unittest.TestCase):

    def setUp(self):

        self.url = 'http://myserver.org/mydata' # NB: Handler would have removed .html if present
        self.datasetName = 'TestDataset'
        self.DDS = {'lat' : ['Float32', [10], ['lat']],
                    'long' : ['Float32', [20], ['long']],
                    'depth' : ['Int16', [10,20], ['lat','long']]
                    }
        self.depth = numpy.ndarray(shape=[10,20],dtype='int32') # Using int32 for DDS Int16 (see Definitions.py)
        a = [i for i in range(self.depth.shape[1])]
        for n in range(self.depth.shape[0]):
            self.depth[n] = a
            self.depth[n] *= n

        self.dimSels = numpy.ndarray(shape=(2,3),dtype='int')
        self.dimSels[0,:] = [0,4,9]
        self.dimSels[1,:] = [0,2,19]

        self.depthSel = self.depth[self.dimSels[0,0]:self.dimSels[0,2]:self.dimSels[0,1],
                                   self.dimSels[1,0]:self.dimSels[1,2]:self.dimSels[1,1]]

        self.varData = '...blah ... xx Int16 depth[lat = 3][long = 10] xx ..Data:\nxxxxyyyy'.encode('utf-8')\
        + self.depthSel.tobytes()

        self.byteOrdStr = '<'

    def tearDown(self):
        pass

    def test_Constructor(self):
        varLoader = VariableLoader(self.url,self.datasetName,self.DDS)
        return varLoader

    def test_VariableNameValidity(self):
        varLoader = self.test_Constructor()
        requrl = varLoader.GetRequestURL('height', [])
        self.assertEqual(requrl, None)

    def test_NumberOfDims(self):
        varLoader = self.test_Constructor()
        dimSels = numpy.ndarray(shape=(1,3),dtype='int32')
        requrl = varLoader.GetRequestURL('depth',dimSels)
        self.assertEqual(requrl, None)

    def test_dimSelection(self):
        varLoader = self.test_Constructor()
        dimSels = self.dimSels
        dimSels[1,2] = 20
        requrl = varLoader.GetRequestURL('depth',dimSels)
        self.assertEqual(requrl, None)

    def test_urlConstruction(self):
        varLoader = self.test_Constructor()
        requrl = varLoader.GetRequestURL('depth',self.dimSels)
        self.assertEqual(requrl, self.url + '.dods?depth[0:4:9][0:2:19]')

    def test_loadVariable(self):
        varLoader = self.test_Constructor()
        var = varLoader.LoadVariable('depth', self.varData, self.dimSels, self.byteOrdStr)
        self.assertTrue(numpy.array_equal(var, self.depthSel))

if __name__ == "__main__":
    unittest.main()
