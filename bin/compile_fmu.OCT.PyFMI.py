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
#  Run from an environment set up for OCT such as jm_python.OCT.sh
#  Run from an environment with MODELICAPATH set up such as:
#   export MODELICAPATH=/opt/OCT/ThirdParty/MSL:/opt/modelica-buildings

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
mdl = os.path.splitext( os.path.basename( arg ) )[ 0 ]
if arg.endswith( '.mo' ):
    mof = arg
    if not os.path.isfile( mof ):
        print( '\nError: Modelica file not found:', mof )
        sys.exit( 1 )
    nam = mdl
elif arg.endswith( '.ref' ):
    mof = None
    try:
        with open( arg, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as ref:
            nam = ref.readline().rstrip( '\n' )
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
compiler_options[ 'disable_smooth_events' ] = True
compiler_options[ 'event_indicator_scaling' ] = False
compiler_options[ 'event_indicator_structure' ] = False
compiler_options[ 'event_output_vars' ] = False
compiler_options[ 'time_events' ] = True
compiler_options[ 'time_state_variable' ] = True
compiler_options[ 'generate_ode_jacobian' ] = False # For directional derivatives # Doesn't support delay()
#if os.name == 'nt': # Windows
#    compiler_options[ 'enable_lazy_evaluation' ] = True # Lazy evaluation not supported in Linux OCT yet # Can cause FMU to give wrong derivative # Can cause event indicator infinite loop with incomplete dependencies

# Compile FMU
try:
    # Compile the FMU
    if mof: # Pass Modelica file
        fmu_file = pymodelica.compile_fmu(
         nam,
         mof,
         version = "2.0",
         compiler_log_level = 'warning',
         compiler_options = compiler_options
        )
    else: # Modelica file found by searching MODELICAPATH
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
    print( '\nUsage:', os.path.basename( sys.argv[ 0 ] ), '<path\model>.[mo|ref]' )
    sys.exit( 1 )
