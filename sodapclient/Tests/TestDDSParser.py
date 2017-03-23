'''
Test class for DDSParser class.
'''

import unittest
from sodapclient.DDSParser import DDSParser

class TestDDSParser(unittest.TestCase):


    def setUp(self):

        # Create the test DDS string
        self.DDSstr = '''
Dataset {
    Float32 lat[lat = 10];
    Float32 long[long = 20];
    Grid {
     ARRAY:
       Int16 depth[lat = 10][long = 20];
     MAPS:
       Float32 lat[lat = 10];
       Float32 long[long = 20];
    } depth;
} TestDataset;
'''

        self.datasetName = 'TestDataset'
        self.DDS = {'lat' : ['Float32', [10], ['lat']],
                    'long' : ['Float32', [20], ['long']],
                    'depth' : ['Int16', [10,20], ['lat','long']]
                    }

    def tearDown(self):
        pass

    def test_Constructor(self):
        self.ddsParser = DDSParser()
        
    def test_Parse(self):
        self.test_Constructor()
        self.ddsParser.Parse(self.DDSstr)
        self.assertEqual(self.datasetName,self.ddsParser.datasetName)
        self.assertEqual(self.DDS,self.ddsParser.Data)


if __name__ == "__main__":
    unittest.main()
