'''TestDASParser class definition'''

import unittest
from ..DASParser import DASParser


class TestDASParser(unittest.TestCase):
    '''
    Test class for DASParser class.
    '''

    def setUp(self):

        # Create the test das string
        self.das_str = '''
Attributes {
    lat {
        String name "Latitude";
        String units "deg";
        Float32 minval -90;
        Float32 maxval 90;
    }
    long {
        String name "Longitude";
        String units "deg";
        Float32 minval 0;
        Float32 maxval 360;
    }
    depth {
        String name "Water Depth";
        String units "m";
        Int32 posup -1;
    }
}
'''

        self.das = {'lat': ['String name "Latitude"', 'String units "deg"',
                            'Float32 minval -90', 'Float32 maxval 90'],
                    'long': ['String name "Longitude"', 'String units "deg"',
                             'Float32 minval 0', 'Float32 maxval 360'],
                    'depth': ['String name "Water Depth"', 'String units "m"',
                              'Int32 posup -1']
                    }

    def tearDown(self):
        pass

    def test_constructor(self):
        ''' Test the DASParser constructor'''
        DASParser()

    def test_parse(self):
        '''Test the parse method'''
        das_parser = DASParser()
        das_parser.parse(self.das_str)
        self.assertEqual(self.das, das_parser.data)


if __name__ == "__main__":
    unittest.main()
