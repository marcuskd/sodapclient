class ProxyDict:

    '''
    A class to provide proxy server details.
    Reads in the proxy details from a text file and returns a dictionary of proxy strings as required for
    class urllib.request.ProxyHandler
    '''

    def __init__(self, proxyFileName):

        proxyConfig = {} # This is a convenience dictionary

        fi = open(proxyFileName,'rt')
        for line in fi:
            srcdata = line[:-1].split(':') # Assumes newline at end of all lines
            proxyConfig[srcdata[0]] = srcdata[1]
        proxyConfig['methods'] = proxyConfig['methods'].split(',') # Will read in string so convert to list

        self.proxyConfig = proxyConfig

    def GetDict(self):

        proxyStrs = {} # This is the dictionary required by class urllib.request.ProxyHandler

        for method in self.proxyConfig['methods']:
            proxyStrs[method] = method + '://' + self.proxyConfig['user'] + ':' + \
            self.proxyConfig['password'] + '@' + self.proxyConfig['server'] + ':' + \
            str(self.proxyConfig['port']) + '/'

        return proxyStrs
