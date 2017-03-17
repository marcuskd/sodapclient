import unittest
from os import remove
from ..ProxyDict import ProxyDict

class TestProxyDict(unittest.TestCase):

    '''
    Test class for ProxyDict class.
    '''

    def setUp(self):

        # Define the text proxy details
        self.proxyConfig = {'user' : 'Me',
                           'password' : 'abracadabra',
                           'server' : 'magic.co.uk',
                           'port' : '1234',
                           'methods' : ['http','https','ftp','socks']}

        # Write the test proxy details to the file
        self.proxyFileName = 'ProxyDictTests.txt'
        fi = open(self.proxyFileName,'wt')
        fi.write('user'+':'+self.proxyConfig['user']+'\n')
        fi.write('password'+':'+self.proxyConfig['password']+'\n')
        fi.write('server'+':'+self.proxyConfig['server']+'\n')
        fi.write('port'+':'+str(self.proxyConfig['port'])+'\n')
        fi.write('methods'+':')
        for m in range(len(self.proxyConfig['methods'])): # Loop is a bit clunky but needed to avoid trailing comma
            if m < len(self.proxyConfig['methods']) - 1:
                fi.write(self.proxyConfig['methods'][m]+',')
            else:
                fi.write(self.proxyConfig['methods'][m]+'\n')
        fi.close()

    def tearDown(self):
        remove(self.proxyFileName)

    def test_Constructor(self):
        self.pd = ProxyDict(self.proxyFileName)
        self.assertEqual(self.proxyConfig,self.pd.proxyConfig)
        
    def test_GetDict(self):
        # Define the dictionary which should be returned
        proxyTestDict = {'http':'http://Me:abracadabra@magic.co.uk:1234/',
                         'https':'https://Me:abracadabra@magic.co.uk:1234/',
                         'ftp':'ftp://Me:abracadabra@magic.co.uk:1234/',
                         'socks':'socks://Me:abracadabra@magic.co.uk:1234/'}
        self.test_Constructor()
        tdict = self.pd.GetDict()
        self.assertEqual(proxyTestDict, tdict)

if __name__ == "__main__":
    unittest.main()
