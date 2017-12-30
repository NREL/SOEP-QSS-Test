#!/usr/bin/env python

# Runs an FMU with PyFMI Using a Step Input Function
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (http://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017 Objexx Engineerinc, Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# (1) Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
# (2) Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# (3) Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER, THE UNITED STATES
# GOVERNMENT, OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Notes
#  Run from an environment set up for PyFMI such as jm_python.sh

# Imports
import math, os, re, sys
import numpy
from pyfmi import load_fmu

# Load the FMU
try:
    model = sys.argv[ 1 ]
    if model.endswith( '.fmu' ): model = model[ :-4 ]
except:
    print( 'Usage: ' + sys.argv[ 0 ] + ' <model_name>' )
    sys.exit( 1 )
try:
    fmu = load_fmu( model + '.fmu' )
except Exception as err:
    if err: print( err )
    print( 'Error: ' + str( err ) )
    sys.exit( 1 )
model = os.path.basename( model )

# Set up input function
def step_fxn( t ): # Step function matching QSS Function_Inp_step( 1.0, 1.0, 0.1 )
    h_0 = 1.0 # Initial height
    h = 1.0 # Step height
    d = 0.1 # Step time delta
    ftd = math.floor( t / d )
    step_num = ( ftd if d * ( ftd + 1.0 ) > t else ftd + 1.0 )
    return h_0 + ( h * step_num )
u_fxn = ( 'u', step_fxn )

# Set simulation options
opt = fmu.simulate_options()
opt[ 'CVode_options' ][ 'atol' ] = 1e-6 # Match QSS default aTol
opt[ 'result_handling' ] = 'memory' # No file output
#opt[ 'result_handling' ] = 'csv'; opt[ 'result_file_name' ] = model + '.csv'
#opt[ 'result_handling' ] = 'file'; opt[ 'result_file_name' ] = model + '.txt'

# Simulate
res = fmu.simulate( input=u_fxn, options=opt )

# Clean up empty log file
try:
    log_file = model + '_log.txt'
    if os.path.getsize( log_file ) == 0:
        os.remove( log_file )
except:
    pass

# Generate output files
temp_re = re.compile( 'temp_\d+' )
t = res[ 'time' ]
for key in res.keys():
    if ( key[ 0 ] != '_' ) or ( key[ 0:5 ] == '__zc_' ): # Not internal variable
        if ( key[ 0:4 ] == 'der(' ) and ( key[ -1 ] == ')' ):
            pass # Skip derivatives
        elif temp_re.match( key ):
            pass # Skip temporaries
        elif key != 'time':
            numpy.savetxt( key + '.out', numpy.c_[ t, res[ key ] ], fmt = '%-20.16g', delimiter = '\t' )
