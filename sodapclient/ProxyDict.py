'''ProxyDict class definition'''


class ProxyDict:
    '''
    A class to provide proxy server details.
    Reads in the proxy details from a text file and returns a dictionary of
    proxy strings as required for class urllib.request.ProxyHandler
    '''

    def __init__(self, proxy_file_name):

        proxy_config = {}  # This is a convenience dictionary

        file = open(proxy_file_name, 'rt')
        for line in file:
            # Assumes newline at end of all lines
            srcdata = line[:-1].split(':')
            proxy_config[srcdata[0]] = srcdata[1]
        # Will read in string so convert to list
        proxy_config['methods'] = proxy_config['methods'].split(',')

        self.proxy_config = proxy_config

    def get_dict(self):
        '''Returns a dictionary containing the proxy data
        as required by urllib.request.ProxyHandler'''

        proxy_strs = {}

        for method in self.proxy_config['methods']:
            proxy_strs[method] = method + '://' + \
                self.proxy_config['user'] + ':' + \
                self.proxy_config['password'] + '@' + \
                self.proxy_config['server'] + ':' + \
                str(self.proxy_config['port']) + '/'

        return proxy_strs
