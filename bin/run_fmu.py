#!/usr/bin/env python

# Runs an FMU with PyFMI
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (https://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017-2020 Objexx Engineering, Inc. All rights reserved.
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
#  Variable list entries can use wildcard or regex syntax

# Imports
import argparse, fnmatch, glob, os, re, sys
import numpy
from pyfmi import load_fmu

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument( 'fmu', help = 'FMU file' )
parser.add_argument( '--var', help = 'variable file' )
parser.add_argument( '--solver', help = 'Solver  (CVode|DASSL|LSODAR|RungeKutta34)  [CVode]', default = 'CVode', choices = [ 'CVode', 'DASSL', 'LSODAR', 'RungeKutta34' ] )
parser.add_argument( '--discr', help = 'CVode discretization method  (BDF|Adams)  [BDF]', default = 'BDF', choices = [ 'BDF', 'Adams' ] )
parser.add_argument( '--rtol', help = 'Relative tolerance  [1e-4]', type = float )
parser.add_argument( '--atol', help = 'Absolute tolerance  [1e-6]', type = float )
parser.add_argument( '--final_time', help = 'Simulation end time', type = float )
parser.add_argument( '--maxord', help = 'Max order', type = int )
parser.add_argument( '--ncp', help = 'Number of communication (output) points  [internal]', type = int )
args = parser.parse_args()

# Check variable list file
if args.var and ( not os.path.isfile( args.var ) ):
    print( 'Error: Variable list file not found' )
    sys.exit( 1 )

# Load the FMU
model = args.fmu
if model.endswith( '.fmu' ): model = model[ :-4 ]

try:
    fmu = load_fmu( model + '.fmu' )
except Exception as err:
    if err: print( 'Error: ' + str( err ) )
    print( 'FMU file: ' + model + '.fmu' )
    sys.exit( 1 )
model = os.path.basename( model )

# Set simulation options
opt = fmu.simulate_options()
opt[ 'solver' ] = args.solver
opt[ 'result_handling' ] = 'memory' # No file output: We do that explicitly below to filter by var file
#opt[ 'result_handling' ] = 'csv'; opt[ 'result_file_name' ] = model + '.csv' # CSV output files
#opt[ 'result_handling' ] = 'file'; opt[ 'result_file_name' ] = model + '.txt' # ASCII output files
if args.ncp is not None: opt[ 'ncp' ] = args.ncp
if args.solver == 'CVode':
    opt_solver = opt[ args.solver + '_options' ]
    opt_solver[ 'discr' ] = args.discr
    if args.maxord is not None: opt_solver[ 'maxord' ] = args.maxord
elif args.solver == 'DASSL':
    opt[ 'solver' ] = 'ODASSL'
    opt_solver = opt[ 'ODASSL_options' ]
    if args.maxord is not None: opt_solver[ 'maxord' ] = args.maxord
elif args.solver == 'LSODAR':
    opt_solver = opt[ args.solver + '_options' ]
    if args.maxord is not None:
        opt_solver[ 'maxordn' ] = args.maxord
        opt_solver[ 'maxords' ] = args.maxord
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
elif args.solver == 'RungeKutta34':
    opt_solver = opt[ args.solver + '_options' ]
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
else:
    print( 'Error: Unsupported solver:', args.solver )
    sys.exit( 1 )
if args.rtol is not None: opt_solver[ 'rtol' ] = args.rtol
if args.atol is not None: opt_solver[ 'atol' ] = args.atol

# Simulate
if args.final_time is not None:
    res = fmu.simulate( final_time = args.final_time, options = opt )
else:
    res = fmu.simulate( options = opt )

# Clean up empty log file
try:
    log_file = model + '_log.txt'
    if os.path.getsize( log_file ) == 0:
        os.remove( log_file )
    log_files = glob.glob( '*_log.txt' ) # Remove all 0-size log files (FMU internal name might not be model name)
    for log_file in log_files:
        if os.path.getsize( log_file ) == 0:
            os.remove( log_file )
except:
    pass

# Generate output files
print( '\nGenerating output files...' )
keys = res.keys()
t = res[ 'time' ]
if args.var:
    with open( args.var, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as var_file:
        for line in var_file:
            key = line.strip()
            if key in keys:
                key_out = key + '.out'
                try:
                    t_v = numpy.c_[ t, res[ key ] ]
                    numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
                except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                    print( 'Output failed to: ' + key_out )
            else: # Try as file name wildcard pattern or regex
                bkey = '' # Key with literal brackets protected
                for c in key:
                    if c in ( '[', ']' ):
                        bkey += '[' + c + ']'
                    else:
                        bkey += c
                m = fnmatch.filter( keys, bkey ) # File name wildcard pattern
                if not m: # Try as regex
                    try:
                        re_key = re.compile( bkey + ( '' if key.endswith( '$' ) else '$' ) ) # Match whole string
                    except:
                        pass # Not a valid regex
                    else:
                        for k in keys:
                            if re_key.match( k ):
                                m.append( k )
                if m: # Matches found
                    for k in m:
                        key_out = k + '.out'
                        try:
                            t_v = numpy.c_[ t, res[ k ] ]
                            numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
                        except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                            print( 'Output failed to: ' + key_out )
                else: # No matches
                    print( 'No variables found matching: ' + key )
else:
    temp_re = re.compile( 'temp_\d+' )
    for key in keys:
        if ( key[ 0 ] != '_' ) or ( key[ 0:5 ] == '__zc_' ): # Not internal variable
            if ( key[ 0:4 ] == 'der(' ) and ( key[ -1 ] == ')' ):
                pass # Skip derivatives
            elif temp_re.match( key ):
                pass # Skip temporaries
            elif key != 'time':
                key_out = key + '.out'
                try:
                    t_v = numpy.c_[ t, res[ key ] ]
                    numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
                except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                    print( 'Output failed to: ' + key_out )
