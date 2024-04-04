#!/usr/bin/env python

# Finds and runs the model's FMU with QSS
#
# Project: QSS Solver
#
# Language: Python 3.5+
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
#  Run from an environment set up for QSS
#  Variable output list file entries can use wildcard or regex syntax

# Imports
import os, subprocess, sys

# Solvers in subset-safe search order
solvers = (
 'nifLIQSS2',
 'nifLIQSS3',
 'nrfQSS2',
 'nrfQSS3',
 'ifLIQSS1',
 'ifLIQSS2',
 'ifLIQSS3',
 'nfQSS2',
 'nfQSS3',
 'nfLIQSS2',
 'nfLIQSS3',
 'niLIQSS2',
 'niLIQSS3',
 'nrQSS2',
 'nrQSS3',
 'rfQSS2',
 'rfQSS3',
 'nQSS2',
 'nQSS3',
 'nLIQSS2',
 'nLIQSS3',
 'rQSS2',
 'rQSS3',
 'fQSS1',
 'fQSS2',
 'fQSS3',
 'fLIQSS1',
 'fLIQSS2',
 'fLIQSS3',
 'iLIQSS1',
 'iLIQSS2',
 'iLIQSS3',
 'LIQSS1',
 'LIQSS2',
 'LIQSS3',
 'QSS1',
 'QSS2',
 'QSS3',
)

# Set up pass-through QSS arguments
args = var = qss = red = ''
fmus = []
gen = 'OCT' # Default FMU generator
for arg in sys.argv[1:]:
    if arg in ( '--help', '-h' ):
        print( 'usage:', os.path.basename( sys.argv[0] ), '[options] [<model>.fmu]' )
        print( '  --help, -h  Show this help information' )
        print( '  --red=REDIRECT  Redirect output to REDIRECT' )
        print( '  --oct  Run the OCT FMU (the default)' )
        print( '  --jmodelica  Run the JModelica FMU' )
        print( '  --dymola  Run the Dymola FMU' )
        print( '  <model>.fmu  FMU(s) to run (can specify more than 1)' )
        print( '  Other QSS options (run QSS --help)' )
        sys.exit( 0 )
    elif arg.startswith( ( '--red=', '--red:' ) ): # Redirect
        red = arg[6:].strip()
    elif arg.lower() == '--oct': # Use OCT FMU
        gen = 'OCT'
    elif arg.lower() == '--jmodelica': # Use JModelica FMU
        gen = 'JModelica'
    elif arg.lower() == '--dymola': # Use Dymola FMU
        gen = 'Dymola'
    elif ( arg[0:2] != '--' ) and arg.endswith( ".fmu" ):
        if os.name == 'nt': # Windows
            arg = arg.replace( '/', '\\' )
        else:
            arg = os.path.splitdrive( arg )[ 1 ] # Discard drive letter
            arg = arg.replace( '\\', '/' )
        fmus.append( arg )
    else: # Pass-through argument
        if arg.startswith( ( '--var=', '--var:' ) ): # Variable file
            var = arg[6:].strip()
        elif arg.startswith( ( '--qss=', '--qss:', '--QSS=', '--QSS:' ) ): # Solver
            qss = arg[6:].strip()
        else: # Clean up options
            arg.replace( '--start_time', '--tStart', 1 )
            arg.replace( '--start-time', '--tStart', 1 )
            arg.replace( '--tBeg', '--tStart', 1 )
            arg.replace( '--tbeg', '--tStart', 1 )
            arg.replace( '--final_time', '--tStop', 1 )
            arg.replace( '--final-time', '--tStop', 1 )
            arg.replace( '--tEnd', '--tStop', 1 )
            arg.replace( '--tend', '--tStop', 1 )
            arg.replace( '--res=csv', '--csv', 1 )
        args += ' ' + arg

# Set QSS solver
if not qss: # QSS solver not specified
    solver_dir = os.getcwd()
    solver = os.path.splitext( os.path.basename( solver_dir ) )[0]
    looking = True
    while looking:
        if solver in solvers:
            looking = False
            break
        else:
            for slv in solvers:
                if slv in solver:
                    solver = slv
                    looking = False
                    break
        if looking:
            solver_dir = os.path.dirname( solver_dir )
            if os.path.splitdrive( solver_dir )[1] == os.sep: # At top of drive/mount
                solver_dir = solver = ''
                break
            solver = os.path.splitext( os.path.basename( solver_dir ) )[0]
    if solver:
        args += ' --qss=' + solver

# Find tool directory and name
tools = ( 'QSS', )
tool_dir = os.getcwd()
tool_sub = [] # Tool subdirectories
tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
while tool not in tools: # Look up one directory level
    tool_dir = os.path.dirname( tool_dir )
    if os.path.splitdrive( tool_dir )[1] == os.sep: # At top of drive/mount
        tool = None
        break
    tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
    if tool not in tools: tool_sub.append( tool )
if not tool:
    print( 'Error: Not in/under a directory named for a supported QSS simulation tool:', tools )
    sys.exit( 1 )

# Find model directory and name: Should be one directory level above tool directory
model_dir = os.path.dirname( tool_dir )
model = os.path.splitext( os.path.basename( model_dir ) )[0]
if os.path.splitdrive( model_dir )[1] == os.sep: # At top of drive/mount
    model_dir = model = ''
if not model:
    print( 'Error: QSS directory not in a model directory' )
    sys.exit( 1 )

# Find the model FMU(s)
if fmus: # Use specified FMU(s)
    for fmu in fmus:
        if not os.path.isfile( fmu ):
            print( 'Error: FMU not found:', fmu )
            sys.exit( 1 )
    model_fmu = ' '.join( fmus )
else: # Search for the model's FMU
    found = False
    if tool_sub:
        model_fmu = os.path.join( model_dir, gen, *tool_sub, model + '.fmu' )
        if os.path.isfile( model_fmu ): # Found FMU in tool subdirectory
            found = True
    if not found: # Look in tool directory
        model_fmu = os.path.join( model_dir, gen, model + '.fmu' )
        if not os.path.isfile( model_fmu ):
            print( 'Error: FMU not found:', model_fmu )
            sys.exit( 1 )

# Find the model variable output list file if present
if var: # Use specified variable output list file
    if not os.path.isfile( os.path.abspath( var ) ):
        print( 'Error: Specified variable output list file not found:', var )
        sys.exit( 1 )
else: # Look up the directory tree for a default variable output list file
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
    if var: args += ' --var=' + var

# Run QSS
sys.stdout.flush() # Flush any diagnostic output
try:
    if sys.version_info >= ( 3, 0 ):
        if red: # Redirect
            if red == 'nul': # Discard
                subprocess.check_call( 'QSS ' + model_fmu + args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
            else: # File
                with open( red, 'w', newline = '\n' ) as log:
                    subprocess.check_call( 'QSS ' + model_fmu + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
        else: # Don't redirect
            subprocess.check_call( 'QSS ' + model_fmu + args, shell = True )
    else:
        if red: # Redirect
            if red == 'nul': # Discard
                DEVNULL = open( os.devnull, 'w' )
                subprocess.check_call( 'QSS ' + model_fmu + args, stdout = DEVNULL, stderr = DEVNULL, shell = True )
            else: # File
                with open( red, 'wb' ) as log:
                    subprocess.check_call( 'QSS ' + model_fmu + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
        else: # Don't redirect
            subprocess.check_call( 'QSS ' + model_fmu + args, shell = True )
except Exception as err:
    print( 'Simulation failed: ', err )
    sys.exit( 1 )
