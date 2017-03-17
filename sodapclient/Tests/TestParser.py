'''
Test class for Parser class.
'''

import unittest
from ..Parser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):

    # Create the test string
        self.startStr = 'StartsHere'
        self.dataStr = '''

blah...
{

    indent stuff...

'''+self.startStr+'''{
    DataType1 x[x = 123];
    DataType2 y[y = 456];

    Grid {
     ARRAY:
       DataType3 z[x = 123][y = 456];
     MAPS:
       DataType1 x[x = 123];

       DataType2 y[y = 456];
    } z;

} TestString;

blah...



'''

        self.dataLines = ['blah...','{','    indent stuff...',self.startStr+'{',
                           '    DataType1 x[x = 123];','    DataType2 y[y = 456];',
                           '    Grid {','     ARRAY:','       DataType3 z[x = 123][y = 456];',
                           '     MAPS:','       DataType1 x[x = 123];','       DataType2 y[y = 456];',
                           '    } z;','} TestString;','blah...']

    def tearDown(self):
        pass

    def test_Constructor(self):
        self.parser = Parser()

    def test_FindIndentLevel(self):
        self.test_Constructor()
        indt = self.parser.FindIndentLevel('     abc...  ')
        self.assertEqual(indt,5)
        
    def test_FindStart(self):
        self.test_Constructor()
        self.parser.FindStart(self.dataStr, self.startStr)
        self.assertEqual(self.parser.dataLines,self.dataLines)
        self.assertEqual(self.parser.lnum,3)
        self.assertEqual(self.parser.indts,[0])

    def test_CheckLine(self):
        self.test_FindStart()

        doLine = self.parser.CheckLine()
        self.assertEqual(doLine,True)
        self.assertEqual(self.parser.indts,[0,4])
        self.assertEqual(self.parser.Finished,False)

        doLine = self.parser.CheckLine()
        self.assertEqual(doLine,True)
        self.assertEqual(self.parser.indts,[0,4])
        self.assertEqual(self.parser.Finished,False)

        self.parser.lnum = len(self.parser.dataLines) - 3
        doLine = self.parser.CheckLine()
        self.assertEqual(doLine,False)
        self.assertEqual(self.parser.indts,[0])
        self.assertEqual(self.parser.Finished,True)
        
if __name__ == "__main__":
    unittest.main()
