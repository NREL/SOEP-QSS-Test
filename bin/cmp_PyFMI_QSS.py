#!/usr/bin/env python

# Runs the model's OCT FMU with PyFMI and QSS and compares results
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
#
# Run from an environment set up for PyFMI and QSS
#
# We use check_call on the runs to avoid simultaneous use of the same FMU
# which is not supported currently
#
# PyFMI and QSS need different tolerances to get the same solution accuracy
# so the --qss:rTol flag is provided to override the QSS tolerance with a
# value that gives QSS a similar accuracy to PyFMI relative to a reference
# solution
#
# PyFMI output time steps (set here via --ncp or --dtOut) cause internal
# simulation steps so they can effectively override the specified tolerance
# and make the QSS and PyFMI tolerances for the same accuracy appear to be
# more different than they are

# Imports
import os, shutil, subprocess, sys

# Set up pass-through arguments
args = ''
pyfmi_args = ''
qss_args = ''
qss = 'QSS3'
red = 'cmp.log'
vars = []
for arg in sys.argv[1:]:
    if arg.startswith( '--red' ): # Redirect
        red = arg[6:].strip()
    elif arg.startswith( ( '--cmp:', '--cmp=' ) ): # Comparison variable
        var = arg[6:].strip().split( '=', 1 )
        if var[0] == '':
            print( 'Error: Comparison variable spec missing variable name:', arg )
            sys.exit( 1 )
        if len( var ) == 1: # No RMS spec
            var.append( None )
        elif var[1]: # RMS spec
            try:
                var[1] = float( var[1] )
            except:
                print( 'Error: Comparison variable RMS spec is not a number:', var )
                sys.exit( 1 )
            if var[1] < 0.0:
                print( 'Error: Comparison variable RMS spec is negative:', var )
                sys.exit( 1 )
        else: # Empty RMS spec
            var[1] = None
        vars.append( var )
    elif arg.startswith( ( '--solver', '--maxord', '--discr', '--inp', '--ncp' ) ): # PyFMI arg
        pyfmi_args += ' ' + arg
    elif arg.startswith( '--soo' ): # PyFMI arg automatically added
        pass
    elif arg.startswith( '--qss:rTol' ): # QSS rTol
        qss_args += ' --rTol=' + arg[11:].strip()
    elif arg.startswith( ( '--qss=', '--qss:' ) ): # QSS method
        qss = arg[6:].strip()
    elif arg.lower().startswith( (
     '--afac',
     '--ztol',
     '--zfac',
     '--dtmin',
     '--dtmax',
     '--dtinf',
     '--dtzc',
     '--dtnd',
     '--dtcon',
     '--pass',
     '--cycles',
     '--inflection',
     '--refine',
     '--prune',
     '--perfect',
     '--fxn',
     '--con',
     '--dep',
     '--bin',
     '--out',
     '--tloc',
    ) ): # QSS arg
        qss_args += ' ' + arg
    else: # Common argument
        args += ' ' + arg
pyfmi_args = args + pyfmi_args + ' --soo'
qss_args = args + qss_args + ' --qss=' + qss + ' --out=sSXL'

# Find model directory and name
model_dir = os.getcwd()
while os.path.basename( os.path.dirname( model_dir ) ) != 'mdl': # Move up one directory level
    model_dir = os.path.dirname( model_dir )
    if os.path.splitdrive( model_dir )[1] == os.sep: # At top of drive/mount
        print( 'Error: Not under a "mdl" directory' )
        sys.exit( 1 )
model = os.path.splitext( os.path.basename( model_dir ) )[0]

# Set up tool directory names
OCT_dir = os.path.join( model_dir, 'OCT' )
QSS_dir = os.path.join( model_dir, 'QSS' )

# Find the model FMU file
model_fmu = os.path.join( OCT_dir, model + '.fmu' )
if not os.path.isfile( model_fmu ):
    print( 'Error: FMU not found:', model_fmu )
    sys.exit( 1 )
print( '\nRunning', model )

# Run PyFMI
print( ' PyFMI', model )
try:
    OCT_cmp_dir = os.path.join( OCT_dir, 'cmp' )
    if os.path.isdir( OCT_cmp_dir ): shutil.rmtree( OCT_cmp_dir )
    os.mkdir( OCT_cmp_dir )
    os.chdir( OCT_cmp_dir )
    if red: # Redirect
        if red == 'nul': # Discard
            subprocess.check_call( 'run_PyFMI.py' + pyfmi_args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
        else: # File
            with open( red, 'w', newline = '\n' ) as log:
                subprocess.check_call( 'run_PyFMI.py' + pyfmi_args, stdout = log, stderr = subprocess.STDOUT, shell = True )
    else: # Don't redirect
        subprocess.check_call( 'run_PyFMI.py' + pyfmi_args, shell = True )
except Exception as err:
    print( 'PyFMI simulation failed: ', err )
    sys.exit( 1 )

# Run QSS
print( '', qss, model )
try:
    QSS_cmp_dir = os.path.join( QSS_dir, 'cmp' )
    if os.path.isdir( QSS_cmp_dir ): shutil.rmtree( QSS_cmp_dir )
    os.makedirs( QSS_cmp_dir )
    os.chdir( QSS_cmp_dir )
    if red: # Redirect
        if red == 'nul': # Discard
            subprocess.check_call( 'run_QSS.py' + qss_args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
        else: # File
            with open( red, 'w', newline = '\n' ) as log:
                subprocess.check_call( 'run_QSS.py' + qss_args, stdout = log, stderr = subprocess.STDOUT, shell = True )
    else: # Don't redirect
        subprocess.check_call( 'run_QSS.py' + qss_args, shell = True )
except Exception as err:
    print( 'QSS simulation failed: ', err )
    sys.exit( 1 )

# Run comparison
print( ' Cmp', model )
try:
    os.chdir( model_dir )
    if vars: # Compare specified variable(s)
        with open( 'cmp.log', 'w', newline = '\n' ) as log: # Output to log file
            for var in vars:
                subprocess.check_call( 'simdiff.py --coarse ' + os.path.join( OCT_cmp_dir, var[0] ) + ' ' + os.path.join( QSS_cmp_dir, var[0] ), stdout = log, stderr = subprocess.STDOUT, shell = True )
    else: # Compare all variables
        with open( 'cmp.log', 'w', newline = '\n' ) as log: # Output to log file
            subprocess.check_call( 'simdiff.py --coarse ' + OCT_cmp_dir + ' ' + QSS_cmp_dir, stdout = log, stderr = subprocess.STDOUT, shell = True )
except Exception as err:
    print( 'Comparison failed: ', err )
    sys.exit( 1 )

# Extract RMS for each variable
print( ' RMS', model )
try:
    i_var = 0
    with open( 'cmp.log', 'r' ) as log: # Scan log file
        line = log.readline()
        while line:
            while line and ( line != 'Comparing:\n' ): line = log.readline()
            var1 = os.path.splitext( os.path.basename( log.readline() ) )[0]
            var2 = os.path.splitext( os.path.splitext( os.path.basename( log.readline() ) )[0] )[0]
            assert var1 == var2, 'Variable names must match: ' + var1 + ' ' + var2
            var = var1
            while line and ( line != ' Difference:\n' ): line = log.readline()
            while line and ( not line.startswith( '  RMS  (L2): ' ) ): line = log.readline()
            if line:
                RMS = line[13:-1]
                if vars:
                    var_ = vars[ i_var ]
                    assert var_[0] == var, 'Comparison variable sequence must match: ' + var_[0] + ' ' + var
                    if ( var_[1] is not None ):
                        RMS_f = float( RMS )
                        RMS_s = var_[1]
                        print( '  ' + var + ' ' + RMS + ' ' + ( '>' if RMS_f > RMS_s else ( '<' if RMS_f < RMS_s else '=' ) ) + ' RMS limit =', RMS_s )
                        i_var += 1
                    else:
                        print( '  ' + var + ' ' + RMS )
                else:
                    print( '  ' + var + ' ' + RMS )
except Exception as err:
    print( 'Comparison scan failed: ', err )
    sys.exit( 1 )
