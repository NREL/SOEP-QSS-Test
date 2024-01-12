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
# Copyright (c) 2017-2023 Objexx Engineering, Inc. All rights reserved.
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
#  Run from an environment with MODELICAPATH set up
#  Variable output list file entries can use glob or regex syntax
#  - PyFMI filter option only supports glob syntax

# Imports
import argparse, fnmatch, glob, math, os, re, sys
import numpy
from pyfmi import load_fmu

# Parse arguments
parser = argparse.ArgumentParser( formatter_class = argparse.RawTextHelpFormatter, add_help = False )
parser.add_argument( '-h', '--help', help = 'Show this message', action = 'help' )
parser.add_argument( '--solver', help = 'Solver  [CVode]', default = 'CVode', choices = [ 'CVode', 'Radau5ODE', 'RungeKutta34', 'Dopri5', 'RodasODE', 'LSODAR', 'ExplicitEuler', 'DASSL' ] ) # DASSL was removed from OCT
parser.add_argument( '--maxord', help = 'Max order', type = int )
parser.add_argument( '--discr', help = 'CVode discretization method  [BDF]', default = 'BDF', choices = [ 'BDF', 'Adams' ] )
parser.add_argument( '--iter', help = 'CVode iteration method  [Newton]', default = 'Newton', choices = [ 'Newton', 'FixedPoint' ] )
parser.add_argument( '--fxn', help = '''Input function in the form VARIABLE:FUNCTION
 VARIABLE  Input variable name
 FUNCTION  Function name/spec (only step function currently available):
  step[i,s,t]  Step function with initial value i and changing by s every t seconds
   step => step[0,1,1]
 Note: Currently only one variable can be given an input function
'''
)
parser.add_argument( '--rtol', help = 'Relative tolerance  [FMU]', type = float )
parser.add_argument( '--rTol', help = argparse.SUPPRESS, type = float, dest = 'rtol' )
parser.add_argument( '--atol', help = 'Absolute tolerance  [FMU]', type = float )
parser.add_argument( '--aTol', help = argparse.SUPPRESS, type = float, dest = 'atol' )
parser.add_argument( '--final_time', help = 'Simulation end time  [FMU]', type = float )
parser.add_argument( '--tEnd', help = argparse.SUPPRESS, type = float, dest = 'final_time' )
parser.add_argument( '--tend', help = argparse.SUPPRESS, type = float, dest = 'final_time' )
parser.add_argument( '--dtOut', help = 'Output time step (s)  [computed]', type = float )
parser.add_argument( '--dtout', help = argparse.SUPPRESS, type = float, dest = 'dtOut' )
parser.add_argument( '--maxh', help = 'Max time step (s) for CVode or Radau5ODE solvers (0 => ∞, <0 => compute from ncp)  [0]', type = float, default = '0' ) # Default to ∞ so output steps don't add integration steps
parser.add_argument( '--dtMax', help = argparse.SUPPRESS, type = float, dest = 'maxh' )
parser.add_argument( '--dtmax', help = argparse.SUPPRESS, type = float, dest = 'maxh' )
parser.add_argument( '--h', help = 'ExplicitEuler max time step (s)  [0.01]', type = float )
parser.add_argument( '--ncp', help = 'Number of communication (output) points (overrides dtOut) (0 => no sampled points)', type = int )
parser.add_argument( '--soo', help = 'Sampled output only (no event points)  [False]', default = False, action = 'store_true' )
parser.add_argument( '--res', help = 'Results format  [memory]', default = 'memory', choices = [ 'memory', 'binary', 'csv', 'text', 'none', '' ] )
parser.add_argument( '--var', help = 'Variable output filter list file' )
parser.add_argument( '--log', help = 'Logging level  [3]', type = int, default = 3, choices = [ 0, 1, 2, 3, 4, 5, 6, 7 ] )
args = parser.parse_args()
if args.maxh is not None and args.maxh < 0.0: args.maxh = None

# Check Modelica environment is set up
if not os.getenv( 'MODELICAPATH' ):
    print( 'Error: Modelica environment is not set up' )
    sys.exit( 1 )

# Find tool directory and name
tools = ( 'OCT', 'JModelica' )
tool_dir = os.getcwd()
tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
while tool not in tools: # Move up one directory level
    tool_dir = os.path.dirname( tool_dir )
    tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
    if os.path.splitdrive( tool_dir )[1] == os.sep: # At top of drive/mount
        tool_dir = tool = ''
        break
if not tool:
    print( 'Error: Not in/under a directory named for a supported FMU simulation tool: ', tools )
    sys.exit( 1 )

# Check tool environment is set up
if tool == 'OCT':
    if not os.getenv( 'OCT_HOME' ):
        print( 'Error: OCT environment is not set up' )
        sys.exit( 1 )
elif tool == 'JModelica':
    if not os.getenv( 'JMODELICA_HOME' ):
        print( 'Error: JModelica environment is not set up' )
        sys.exit( 1 )

# Find model directory and name: Should be one directory level above tool directory
model_dir = os.path.dirname( tool_dir )
model = os.path.splitext( os.path.basename( model_dir ) )[0]
if os.path.splitdrive( model_dir )[1] == os.sep: # At top of drive/mount
    model_dir = model = ''
if not model:
    print( 'Error: Tool directory not in a model directory' )
    sys.exit( 1 )

# Find the model FMU file
model_fmu = os.path.join( tool_dir, model + '.fmu' )
if not os.path.isfile( model_fmu ):
    print( 'Error: FMU not found:', model_fmu )
    sys.exit( 1 )

# Find the model variable output list file if present
if args.var is not None: # Use specified variable output list file
    model_var = os.path.abspath( args.var )
    if not os.path.isfile( model_var ):
        print( 'Error: Specified variable output list file not found:', model_var )
        sys.exit( 1 )
else: # Look for default variable output list file
    var = ''
    var_dir = os.getcwd()
    model_var = model + '.var'
    while True:
        var_look = os.path.join( var_dir, model_var )
        if os.path.isfile( var_look ): # Found var file
            var = var_look
            break
        elif var_dir == model_dir: # Reached model dir without finding var file
            break
        else: # Move up to parent directory
            var_dir = os.path.dirname( var_dir )
    if var: args.var = var_look

# Load the FMU
try:
    fmu = load_fmu( model_fmu, log_level = args.log )
except Exception as err:
    if err: print( 'Error: ' + str( err ) )
    print( 'FMU file: ' + model_fmu )
    sys.exit( 1 )
fmu.set_max_log_size( 2073741824 ) # = 2*1024^3 (about 2GB)

# Set simulation options
opt = fmu.simulate_options()
opt[ 'solver' ] = args.solver
if args.res in ( 'memory', 'none', '' ): # In-memory results: Signal files generated after simulation if memory
    opt[ 'result_handling' ] = 'memory'
elif args.res == 'binary': # Binary .mat results file
    opt[ 'result_handling' ] = 'binary'
    opt[ 'result_file_name' ] = model + '.mat'
elif args.res == 'csv': # CSV results file
    opt[ 'result_handling' ] = 'csv'
    opt[ 'result_file_name' ] = model + '.csv'
elif args.res == 'text': # Text results file
    opt[ 'result_handling' ] = 'file'
    opt[ 'result_file_name' ] = model + '.res'
if args.var: # Variable output filtering
    filter = []
    with open( args.var, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as var_file:
        for line in var_file:
            key = line.strip()
            if key and ( key[ 0 ] != '#' ):
                filter.append( key )
                if ( '[' in key ) or ( ']' in key ):
                    key = re.sub( r'([\[\]])', r'[\1]', key ) # filter needs glob syntax with recent OCT: Add variant assuming brackets aren't protected in .var files
                    filter.append( key )
    if filter: opt[ 'filter' ] = filter
if args.ncp is not None:
    opt[ 'ncp' ] = args.ncp
else: # Use dtOut to set ncp for PyFMI
    time_span = ( args.final_time if args.final_time is not None else fmu.get_default_experiment_stop_time() ) - fmu.get_default_experiment_start_time()
    if args.dtOut is None: # Set default dtOut
        args.dtOut = math.pow( 10.0, round( math.log10( time_span * 0.0002 ) ) )
    else: # Use specified dtOut
        if args.dtOut <= 0.0:
            print( 'Error: Non-positive dtOut time step specified:', args.dtOut )
            sys.exit( 1 )
    opt[ 'ncp' ] = int( round( time_span / args.dtOut ) )
if args.solver == 'CVode':
    opt_solver = opt[ args.solver + '_options' ]
    opt_solver[ 'discr' ] = args.discr
    opt_solver[ 'iter' ] = args.iter
    if args.maxord is not None: opt_solver[ 'maxord' ] = args.maxord
    if args.maxh is not None: opt_solver[ 'maxh' ] = args.maxh
# Additional arguments for testing
#   opt_solver[ 'external_event_detection' ] = False
#   opt_solver[ 'maxh' ] = ( fmu.get_default_experiment_stop_time() - fmu.get_default_experiment_stop_time() ) / float( opt[ 'ncp' ] )
#   opt_solver[ 'store_event_points' ] = True # True is default
elif args.solver == 'Radau5ODE':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination # May not be needed anymore since OCT 1.43.4 fix
    if args.maxh is not None: opt_solver[ 'maxh' ] = args.maxh
elif args.solver == 'RungeKutta34':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
elif args.solver == 'Dopri5':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
elif args.solver == 'RodasODE':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
elif args.solver == 'LSODAR':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    if args.maxord is not None:
        opt_solver[ 'maxordn' ] = args.maxord
        opt_solver[ 'maxords' ] = args.maxord
    opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination
elif args.solver == 'ExplicitEuler':
    try:
        opt_solver = opt[ args.solver + '_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    if args.h is not None: opt_solver[ 'h' ] = args.h
    #opt_solver[ 'maxsteps' ] = 100000000 # Avoid early termination # Not supported by ExplicitEuler
elif args.solver == 'DASSL':
    opt[ 'solver' ] = 'ODASSL'
    try:
        opt_solver = opt[ 'ODASSL_options' ]
    except:
        print( 'Error: Unsupported solver:', args.solver )
        sys.exit( 1 )
    if args.maxord is not None: opt_solver[ 'maxord' ] = args.maxord
else:
    print( 'Error: Unsupported solver:', args.solver )
    sys.exit( 1 )
if args.rtol is not None: opt_solver[ 'rtol' ] = args.rtol
if args.atol is not None: opt_solver[ 'atol' ] = args.atol
opt_solver[ 'store_event_points' ] = not args.soo

# Simulate
sim_args = { 'options': opt }
if args.final_time is not None:
    sim_args[ 'final_time' ] = args.final_time
if args.fxn:
    try:
        ( var, fxn ) = args.fxn.split( ':' )
    except:
        print( 'Error: Input option not in VAR:FXN format', args.fxn )
        sys.exit( 1 )
    if ( fxn == 'step' ) or ( fxn.startswith( 'step[' ) and fxn.endswith( ']' ) ):
        if fxn == 'step': # Default specs to [0,1,1]
            ( initial, step, delta_t ) = ( 0, 1, 1 )
        else:
            try:
                ( initial, step, delta_t ) = fxn[ 5 : -1 ].strip().split( ',' )
                ( initial, step, delta_t ) = ( float( initial ), float( step ), float( delta_t ) )
            except:
                print( 'Error: Unsupported step function specs:', fxn[ 4 : ].strip(), 'Should be in the form [initial,step,delta-t]' )
                sys.exit( 1 )
        def step_fxn( t ): # Step function matching QSS Function_Inp_step( 0.0, 1.0, 1.0 )
            h_0 = initial # Initial height
            h = step # Step height
            d = delta_t # Step time delta
            ftd = math.floor( t / d )
            step_num = ( ftd if d * ( ftd + 1.0 ) > t else ftd + 1.0 )
            return h_0 + ( h * step_num )
        sim_args[ 'input' ] = ( var, step_fxn )
    else:
        print( 'Error: Unsupported input function:', fxn, 'Only the step function is currently supported' )
        sys.exit( 1 )
try:
    res = fmu.simulate( **sim_args )
except Exception as err:
    print( 'Simulation failed: ', err )
    res = False

# Clean up empty log file
model_log = model + '_log.txt'
try:
    log_file = model_log
    if os.path.isfile( log_file ) and ( os.path.getsize( log_file ) == 0 ):
        os.remove( log_file )
except:
    pass
try:
    log_files = glob.glob( '*_log.txt' ) # Remove all 0-size log files (FMU internal name might not be model name)
    for log_file in log_files:
        if os.path.isfile( log_file ) and ( os.path.getsize( log_file ) == 0 ):
            os.remove( log_file )
        elif log_file.endswith( model_log ) and ( log_file != model_log ): # Rename log file to local model name
            if os.path.isfile( model_log ):
                os.remove( model_log )
            os.rename( log_file, model_log )
except:
    pass

# Terminate if simulation failed
if res is False: sys.exit( 1 )

# Generate signal output files if in-memory results
if args.res == 'memory':
    print( '\nGenerating output files...' )
    try:
        keys = res.keys()
    except: # Work-around for OCT-r23206_JM-r14295
        if sys.version_info >= ( 3, 0 ):
            keys = list( res._result_data.vars )
        else:
            keys = res._result_data.vars.keys()
    if sys.platform in ( 'win32', 'cygwin' ): # Case-insensitive file name handling
        keys.sort() # Assure the collision name decorating is deterministic
        keys_count = { key: 0 for key in keys } # Count number of variables
        KEYS_count = { key.upper(): 0 for key in keys } # Count of variables with same case-insensitive key
        for key in keys:
            KEYS_count[ key.upper() ] += 1
            keys_count[ key ] = KEYS_count[ key.upper() ]
        keys_out = {}
        for key in keys:
            if KEYS_count[ key.upper() ] == 1: # No case-insentive collision
                keys_out[ key ] = key
            else: # Add count to output key
                key_out = key + '.' + str( keys_count[ key ] )
                while key_out in keys: # In case the count-appended name conflicts
                    key_out += '_'
                keys_out[ key ] = key_out
    else:
        keys_out = { key: key for key in keys }
    t = res[ 'time' ]
    if args.var: # Variable output filtering
        with open( args.var, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as var_file:
            for line in var_file:
                key = line.strip()
                if key and ( key[ 0 ] != '#' ):
                    if key in keys:
                        key_out = keys_out[ key ] + '.out'
                        try:
                            t_v = numpy.c_[ t, res[ key ] ]
                            numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
                        except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                            print( 'Output failed to: ' + key_out )
                    else: # Try as file name glob pattern
                        m = fnmatch.filter( keys, key ) # File name glob pattern
                        if not m: # Try with protected brackets
                            key = re.sub( r'([\[\]])', r'[\1]', key ) # Assume brackets aren't protected in .var files
                            m = fnmatch.filter( keys, key ) # File name glob pattern
                        if m: # Matches found
                            for k in m:
                                key_out = keys_out[ k ] + '.out'
                                try:
                                    t_v = numpy.c_[ t, res[ k ] ]
                                    numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
                                except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                                    print( 'Output failed to: ' + key_out )
                        else: # No matches
                            print( 'No variables found matching: ' + key )
    else: # No variable output filtering
        temp_re = re.compile( r'temp_\d+' )
        for key in keys:
            if key == 'time': continue # Omit time
            if key.startswith( 'der(' ) and ( key[ -1 ] == ')' ): continue # Omit derivatives
            if key.startswith( '_' ) and ( not key.startswith( ( '_eventIndicator_' ) ) ): continue # Omit internals except for event indicators
            if temp_re.match( key ): continue # Omit temporaries
            key_out = keys_out[ key ] + '.out'
            try:
                t_v = numpy.c_[ t, res[ key ] ]
                numpy.savetxt( key_out, t_v, fmt = '%-.15g', delimiter = '\t' )
            except: # PyFMI sometimes raises KeyError on res[ key ] lookups (not sure why)
                print( 'Output failed to: ' + key_out )
