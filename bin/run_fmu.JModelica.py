# Run an FMU model with JModelica
# Run from an environment set up for JModelica such as jm_python.sh

import os, sys
import numpy
from pyfmi import load_fmu

# Load the FMU
try:
    model = sys.argv[ 1 ]
    if model.endswith( '.fmu' ): model = model[ :-4 ]
    fmu = load_fmu( model + '.fmu' )
    model = os.path.basename( model )
except:
    print( 'Usage: ' + sys.argv[ 0 ] + ' <model_name>' )

# Set simulation options
opt = fmu.simulate_options()
opt[ 'CVode_options' ][ 'atol' ] = 1e-6 # Match QSS default aTol
opt[ 'result_handling' ] = 'memory' # No file output
#opt[ 'result_handling' ] = 'csv'; opt[ 'result_file_name' ] = model + '.csv'
#opt[ 'result_handling' ] = 'file'; opt[ 'result_file_name' ] = model + '.txt'

# Simulate
res = fmu.simulate( options=opt )

# Clean up empty log file
try:
    log_file = model + '_log.txt'
    if os.path.getsize( log_file ) == 0:
        os.remove( log_file )
except:
    pass

# Generate output files
t = res[ 'time' ]
for key in res.keys():
    if not key[ 0 ] == '_': # Not internal variable
        if ( key[ 0:4 ] == 'der(' ) and ( key[ -1 ] == ')' ):
            pass # Skip derivatives
        elif key != 'time':
            numpy.savetxt( key + '.out', numpy.c_[ t, res[ key ] ], fmt = '%-20.16g', delimiter = '\t' )
