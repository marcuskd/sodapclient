# Example use of sodapclient
# To run this example at the command line enter: python3 Example.py

import numpy

from sodapclient import Handler

# Define the URL (one of the datasets available at the official OpenDAP test server):
url = 'http://test.opendap.org/opendap/hyrax/data/nc/sst.mnmean.nc.gz.html'

h = Handler(url) # Initialise the handler, which will also get the DDS and DAS

# We'll access the SST data over the last 2 times, the last 3 lats and the last 4 longs available...

# Set up the arrays for the required dimensions, shape 1x3 for map variables and nx3 for data variables with n dimensions
timeDims = numpy.array([[1800,10,1810]]) # Time indices 1800 and 1810
latDims = numpy.array([[70,2,74]]) # Latitude indices 70, 72 and 74
lonDims = numpy.array([[80,1,83]]) # Longitude indices 80 to 83
sstDims = numpy.array([timeDims[0],latDims[0],lonDims[0]])

byteOrder = '>' # Big Endian

# Get the data and the dimension variables

h.GetVariable('time',timeDims,byteOrder)
h.GetVariable('lat',latDims,byteOrder)
h.GetVariable('lon',lonDims,byteOrder)
h.GetVariable('sst',sstDims,byteOrder)

h.Print() # Print the DDS, DAS and data to screen

# Then get access to any variable from the handler's variables dictionary, e.g.

sst = h.variables['sst']
print('\nSST...\n',sst)
