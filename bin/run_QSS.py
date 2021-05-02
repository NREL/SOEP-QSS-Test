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
# Copyright (c) 2017-2021 Objexx Engineering, Inc. All rights reserved.
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

# Set up pass-through QSS arguments
args = var = qss = red = ''
gen = 'OCT' # Default FMU generator
for arg in sys.argv[1:]:
    if arg.startswith( ( '--red=', '--red:' ) ): # Redirect
        red = arg[6:].strip()
    elif arg.lower() == '--oct': # Use OCT FMU
        gen = 'OCT'
    elif arg.lower() == '--jmodelica': # Use JModelica FMU
        gen = 'JModelica'
    elif arg.lower() == '--dymola': # Use Dymola FMU
        gen = 'Dymola'
    else: # Pass-through argument
        if arg.startswith( ( '--var=', '--var:' ) ): # Variable file
            var = arg[6:].strip()
        elif arg.startswith( ( '--qss=', '--qss:' ) ): # QSS method
            qss = arg[6:].strip()
        else: # Clean up options
            arg.replace( '--final_time', '--tEnd', 1 )
        args += ' ' + arg

# Try to deduce QSS solver if not specified
if not qss: # QSS solver not specified
    solver = ''
    solvers = ( 'xLIQSS1', 'xLIQSS2', 'xLIQSS3', 'LIQSS1', 'LIQSS2', 'LIQSS3', 'xQSS1', 'xQSS2', 'xQSS3', 'QSS1', 'QSS2', 'QSS3' )
    solver_dir = os.getcwd()
    solver_dir = os.path.splitext( os.path.basename( os.getcwd() ) )[0]
    if solver_dir in solvers:
        solver = solver_dir
    else:
        for slv in solvers:
            if slv in solver_dir:
                solver = slv
                break
    if solver: args += ' --qss=' + solver

# Find tool directory and name
tools = ( 'QSS', )
tool_dir = os.getcwd()
tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
while tool not in tools: # Move up one directory level
    tool_dir = os.path.dirname( tool_dir )
    tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
    if os.path.splitdrive( tool_dir )[1] == os.sep: # At top of drive/mount
        tool_dir = tool = ''
        break
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

# Find the model FMU file
model_fmu = os.path.join( model_dir, gen, model + '.fmu' )
if not os.path.isfile( model_fmu ):
    print( 'Error: FMU not found:', model_fmu )
    sys.exit( 1 )

# Find the model variable output list file if present
if var: # Use specified variable output list file
    if not os.path.isfile( os.path.abspath( var ) ):
        print( 'Error: Specified variable output list file not found:', var )
        sys.exit( 1 )
else: # Look for default variable output list file
    var = os.path.join( model_dir, model + '.var' )
    if os.path.isfile( var ): args += ' --var=' + var

# Run QSS
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
