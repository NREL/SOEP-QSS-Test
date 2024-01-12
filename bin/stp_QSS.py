#!/usr/bin/env python

# Runs the model's OCT FMU with QSS and check/report step counts
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
#
# Run from an environment set up for QSS

# Imports
import os, shutil, subprocess, sys

# Set up pass-through arguments
qss_args = ''
qss = 'QSS3'
red = 'stp.log'
vars = []
for arg in sys.argv[1:]:
    if arg.startswith( '--red' ): # Redirect
        red = arg[6:].strip()
    elif arg.startswith( ( '--stp:', '--stp=', '--step:', '--step=', '--steps:', '--steps=' ) ): # Steps spec
        var = arg[6:].strip().split( '=', 1 )
        if var[0] == '':
            print( 'Error: Steps variable spec missing variable name:', arg )
            sys.exit( 1 )
        if len( var ) == 1: # No step count spec
            var.append( None )
        elif var[1]: # Step count spec
            try:
                var[1] = int( var[1] )
            except:
                print( 'Error: Steps variable step count is not an integer:', var )
                sys.exit( 1 )
            if var[1] < 0:
                print( 'Error: Steps variable step count is negative:', var )
                sys.exit( 1 )
        else: # Empty step count spec
            var[1] = None
        vars.append( var )
    elif arg.startswith( ( '--qss=', '--qss:' ) ): # QSS method
        qss = arg[6:].strip()
    else: # QSS arg
        qss_args += ' ' + arg
qss_args += ' --qss=' + qss + ' --steps'

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

# Run QSS
print( '', qss, model )
try:
    QSS_stp_dir = os.path.join( QSS_dir, 'stp' )
    if os.path.isdir( QSS_stp_dir ): shutil.rmtree( QSS_stp_dir )
    os.makedirs( QSS_stp_dir )
    os.chdir( QSS_stp_dir )
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

# Process steps file
print( ' Stp', model )
try:
    os.chdir( model_dir )
    QSS_model_stp = os.path.join( QSS_stp_dir, model + '.stp' )
    if vars: # Process specified variable(s)
        with open( 'stp.log', 'w', newline = '\n' ) as log: # Output to log file
            stp = open( QSS_model_stp, 'r' )
            nams = [ var[0] for var in vars ]
            line = stp.readline() # Total step count: Not used here
            while line:
                try:
                    line = stp.readline()
                    var_name, var_steps = line.rstrip( '\n' ).split()
                    if line:
                        try:
                            i_var = nams.index( var_name )
                            var_steps = int( var_steps )
                            c_var = vars[ i_var ][1]
                            if c_var is not None:
                                log.write( var_name + ' ' + str( var_steps ) + ' ' + ( '>' if var_steps > c_var else ( '<' if var_steps < c_var else '=' ) ) + ' step count spec = ' + str( c_var ) + '\n' )
                            else:
                                log.write( var_name + ' ' + str( var_steps ) + '\n' )
                        except:
                            log.write( var_name + ' ' + str( var_steps ) + '\n' )
                except:
                    pass
            stp.close()
    else: # Process all variables
        with open( 'stp.log', 'w', newline = '\n' ) as log: # Output to log file
            stp = open( QSS_model_stp, 'r' )
            line = stp.readline() # Total step count: Not used here
            while line:
                try:
                    line = stp.readline()
                    if line:
                        var_name, var_steps = line.rstrip( '\n' ).split()
                        var_steps = int( var_steps )
                        log.write( var_name + ' ' + str( var_steps ) + '\n' )
                except:
                    pass
            stp.close()
except Exception as err:
    print( 'Step count processing failed: ', err )
    sys.exit( 1 )
