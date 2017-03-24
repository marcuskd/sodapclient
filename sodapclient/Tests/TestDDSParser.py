'''TestDDSParser class definition'''

import unittest
from sodapclient.DDSParser import DDSParser


class TestDDSParser(unittest.TestCase):
    '''
    Test class for DDSParser class.
    '''

    def setUp(self):

        # Create the test DDS string
        self.dds_str = '''
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

        self.dataset_name = 'TestDataset'
        self.dds = {'lat': ['Float32', [10], ['lat']],
                    'long': ['Float32', [20], ['long']],
                    'depth': ['Int16', [10, 20], ['lat', 'long']]
                    }

    def tearDown(self):
        pass

    def test_constructor(self):
        ''' Test the DDSParser constructor'''
        DDSParser()

    def test_parse(self):
        '''Test the parse method'''
        dds_parser = DDSParser()
        dds_parser.parse(self.dds_str)
        self.assertEqual(self.dataset_name, dds_parser.dataset_name)
        self.assertEqual(self.dds, dds_parser.data)


if __name__ == "__main__":
    unittest.main()
