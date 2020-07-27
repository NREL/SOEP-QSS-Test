#!/usr/bin/env python

# Compiles a Modelica file optionally using the Buildings library
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
#  Run from an environment set up for JModelica such as jm_python.JModelica.sh
#  Run from an environment with MODELICAPATH set up such as:
#   export MODELICAPATH=/opt/JModelica/ThirdParty/MSL:/opt/modelica-buildings

# Python imports
import os, shutil, sys

# Modelica imports
import pymodelica

# Increase JVM memory
pymodelica.environ[ 'JVM_ARGS' ] = '-Xmx4096m'

# Process argument
if len( sys.argv ) != 2:
    print( '\nError: One argument with the .mo or .ref file name expected' )
    sys.exit( 1 )
arg = sys.argv[ 1 ]
if not os.path.isfile( arg ):
    print( '\nError: Argument is not an existing file' )
    sys.exit( 1 )
nam = mdl = os.path.splitext( os.path.basename( arg ) )[ 0 ]
if arg.endswith( '.mo' ):
    mod = arg
    if not os.path.isfile( mod ):
        print( '\nError: Modelica file not found:', mod )
        sys.exit( 1 )
elif arg.endswith( '.ref' ):
    mod = None
    try:
        with open( arg, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as ref:
            ref = ref.readline().rstrip( '\n' )
            if ref == 'Buildings': # Uses Buildings Library but model is local .mo
                lib = 'Buildings'
            elif ref.startswith( 'Buildings.' ):
                nam = ref
                lib = 'Buildings'
            elif ref.startswith( 'Modelica.' ):
                nam = ref
                lib = 'Modelica'
            else:
                lib = ''
            if lib == 'Buildings':
                try:
                    branch = ref.readline().rstrip( '\n' )
                except:
                    branch = ''
                try:
                    commit = ref.readline().rstrip( '\n' )
                except:
                    commit = ''
            else:
                branch = commit = ''
    except Exception as msg:
        print( '\nError: Ref file read failed:', msg )
        print( '\nRef file format is:' )
        print( 'Model name in library' )
        print( '\nRef file example:' )
        print( 'Buildings.ThermalZones.Detailed.Validation.BESTEST.Cases6xx.Case600' )
        sys.exit( 1 )
else:
    print( '\nError: Argument not a .mo or .ref file' )
    sys.exit( 1 )

# Set FMU compilation options
compiler_options = {}
compiler_options[ 'generate_html_diagnostics' ] = False

# Compile FMU
try:
    # Compile the FMU
    if mod: # Pass Modelica file
        fmu_file = pymodelica.compile_fmu(
         nam,
         mod,
         version = "2.0",
         compiler_log_level = 'warning',
         compiler_options = compiler_options
        )
    else: # Modelica file found by searching MODELICAPATH
        if branch or commit: # Create temporary model-specific Buildings Library

            # Model-specific Buildings Library setup
            try: # Create directory for model-specific Buildings Library
                buildings_dir = ( os.getenv( 'TEMP' ) + '\\' if os.name == 'nt' else '~/tmp/' ) + mdl + '_buildings'
                if not os.path.isdir( buildings_dir ): # Assume existing model-specific Buildings Library is correctly set up to save time
                    if branch: # Clone the specified Buildings Library branch
                        os.system( 'git clone -b ' + branch + ' git@github.com:lbl-srg/modelica-buildings.git ' + buildings_dir )
                    else: # Clone the Buildings Library master branch
                        os.system( 'git clone git@github.com:lbl-srg/modelica-buildings.git ' + buildings_dir )
                    if commit: # Check out a specified commit
                        os.system( 'git -C ' + buildings_dir + ' checkout ' + commit )
            except Exception as msg:
                print( 'Buildings Library clone/checkout from .ref file specs failed: ' + msg )
                sys.exit( 1 )

            # Set up environment to use model-specific Buildings Library
            os.environ[ 'MODELICA_BUILDINGS_LIB' ] = buildings_dir
            MODELICAPATH = os.getenv( 'MODELICAPATH' )
            if MODELICAPATH:
                os.environ[ 'MODELICAPATH' ] = buildings_dir + ( ';' if os.name == 'nt' else ':' ) + MODELICAPATH
            else:
                os.environ[ 'MODELICAPATH' ] = buildings_dir
            pymodelica.environ[ 'MODELICAPATH' ] = os.getenv( 'MODELICAPATH' )

        if not os.getenv( 'MODELICAPATH' ):
            print( 'Error: MODELICAPATH environment variable is not set: Required for reference to library models' )
            sys.exit( 1 )
        fmu_file = pymodelica.compile_fmu(
         nam,
         version = "2.0",
         compiler_log_level = 'warning',
         compiler_options = compiler_options
        )
        if nam != mdl: # Rename outputs to local model name
            nam = nam.replace( '.', '_' )
            nam_fmu = nam + '.fmu'
            if os.path.isfile( nam_fmu ): # Rename the FMU
                mdl_fmu = mdl + '.fmu'
                try:
                    if os.path.isfile( mdl_fmu ): os.remove( mdl_fmu )
                    os.rename( nam_fmu, mdl_fmu )
                except:
                    print( 'Warning: Renaming FMU failed:', nam_fmu, '->', mdl_fmu )
            nam_log = nam + '_log.txt'
            if os.path.isfile( nam_log ): # Rename the log
                mdl_log = mdl + '_log.txt'
                try:
                    if os.path.isfile( mdl_log ): os.remove( mdl_log )
                    os.rename( nam_log, mdl_log )
                except:
                    print( 'Warning: Renaming log failed:', nam_log, '->', mdl_log )
            nam_dia = nam + '_html_diagnostics'
            if os.path.isdir( nam_dia ): # Rename the HTML diagnostics folder
                mdl_dia = mdl + '_html_diagnostics'
                try:
                    if os.path.isdir( mdl_dia ): shutil.rmtree( mdl_dia )
                    os.rename( nam_dia, mdl_dia )
                except:
                    print( 'Warning: Renaming diagnostics failed:', nam_dia, '->', mdl_dia )
except Exception as msg:
    print( '\nError: FMU compilation failed:', msg )
    print( '\nUsage:', os.path.basename( sys.argv[ 0 ] ), '<path' + os.sep + 'model>.[mo|ref]' )
    sys.exit( 1 )
