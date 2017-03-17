'''
Test class for DASParser class.
'''

import unittest
from ..DASParser import DASParser

class TestDASParser(unittest.TestCase):

    def setUp(self):

        # Create the test DAS string
        self.DASstr = '''
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

        self.DAS = {'lat' : ['String name "Latitude"','String units "deg"','Float32 minval -90','Float32 maxval 90'],
                    'long' : ['String name "Longitude"','String units "deg"','Float32 minval 0','Float32 maxval 360'],
                    'depth' : ['String name "Water Depth"','String units "m"','Int32 posup -1']
                    }

    def tearDown(self):
        pass

    def test_Constructor(self):
        self.dasParser = DASParser()
        
    def test_Parse(self):
        self.test_Constructor()
        self.dasParser.Parse(self.DASstr)
        self.assertEqual(self.DAS,self.dasParser.Data)


if __name__ == "__main__":
    unittest.main()
