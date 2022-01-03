#!/usr/bin/env python

# Builds an FMU from a Modelica file optionally using the Buildings library
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
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
#  Run from an environment set up for PyFMI such as jm_python.sh
#  Run from an environment with MODELICAPATH and MODELICA_BUILDINGS_LIB set up

# Imports
import argparse, os, shutil, subprocess, sys
import pymodelica

# Increase JVM memory
pymodelica.environ[ 'JVM_ARGS' ] = '-Xmx4096m'

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument( '--qss', help = 'QSS options (OCT)  [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-qss', help = 'No QSS options (OCT)', dest = 'qss', action = 'store_false' )
parser.add_argument( '--pyfmi', help = 'No QSS options (OCT)', dest = 'qss', action = 'store_false' )
parser.add_argument( '--lazy', help = 'Lazy evaluation (OCT)  [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--no-lazy', help = 'No lazy evaluation (OCT)', dest = 'lazy', action = 'store_false' )
parser.add_argument( '--dd', help = 'Directional derivatives (OCT)  [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--no-dd', help = 'No directional derivatives (OCT)', dest = 'dd', action = 'store_false' )
parser.add_argument( '--tearing', help = 'Automatic tearing [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-tearing', help = 'No automatic tearing', dest = 'tearing', action = 'store_false' )
parser.add_argument( '--deps', help = '<Dependencies> annotation [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--no-deps', help = 'No <Dependencies> annotation', dest = 'deps', action = 'store_false' )
parser.add_argument( '--source', help = 'Generate FMU source  [Off]', default = False, action = 'store_true' )
parser.add_argument( '--mof', help = 'Generate .mof flat files  [Off]', default = False, action = 'store_true' )
parser.add_argument( '--diag', help = 'Generate HTML diagnostics  [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-diag', help = 'Don\'t generate HTML diagnostics', dest = 'diag', action = 'store_false' )
parser.add_argument( '--xml', help = 'Extract modelDescription.xml from FMU  [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-xml', help = 'Don\'t extract modelDescription.xml from FMU', dest = 'xml', action = 'store_false' )
parser.add_argument( 'model', nargs = '?', help = 'Model file', default = '' )
args = parser.parse_args()
if args.qss: # Set up conditional defaults
    if args.lazy is None: args.lazy = True
    if args.dd is None: args.dd = True
    if args.deps is None: args.deps = True
else:
    if args.lazy is None: args.lazy = False
    if args.dd is None: args.dd = False
    if args.deps is None: args.deps = False

# Check Modelica environment is set up
if not os.getenv( 'MODELICAPATH' ):
    print( 'Error: MODELICAPATH environment variable is not set' )
    sys.exit( 1 )

# Check Modelica Buildings library environment is set up
if not os.getenv( 'MODELICA_BUILDINGS_LIB' ):
    print( 'Error: Modelica Buildings Library environment is not set up' )
    sys.exit( 1 )

# Find tool directory and name
tools = ( 'OCT', 'JModelica' )
tool_dir = os.getcwd()
tool = os.path.splitext( os.path.basename( tool_dir ) )[ 0 ]
while tool not in tools: # Move up one directory level
    tool_dir = os.path.dirname( tool_dir )
    tool = os.path.splitext( os.path.basename( tool_dir ) )[ 0 ]
    if os.path.splitdrive( tool_dir )[ 1 ] == os.sep: # At top of drive/mount
        tool_dir = tool = ''
        break
if not tool:
    print( 'Error: Not in/under a directory named for a supported FMU build tool: ', tools )
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
model = os.path.splitext( os.path.basename( model_dir ) )[ 0 ]
if os.path.splitdrive( model_dir )[ 1 ] == os.sep: # At top of drive/mount
    model_dir = model = ''
if not model:
    print( 'Error: Tool directory not in a model directory' )
    sys.exit( 1 )

# Set the .mo or .ref file to build
if args.model:
    if os.path.isfile( args.model ):
        model_inp = args.model
    else:
        print( 'Error: Specified model file not found: ' + args.model )
        sys.exit( 1 )
elif os.path.isfile( os.path.join( tool_dir, model + '.ref' ) ):
    model_inp = os.path.join( tool_dir, model + '.ref' )
elif os.path.isfile( os.path.join( tool_dir, model + '.mo' ) ):
    model_inp = os.path.join( tool_dir, model + '.mo' )
elif os.path.isfile( os.path.join( model_dir, model + '.ref' ) ):
    model_inp = os.path.join( model_dir, model + '.ref' )
elif os.path.isfile( os.path.join( model_dir, model + '.mo' ) ):
    model_inp = os.path.join( model_dir, model + '.mo' )
else:
    print( 'Error: No Modelica (' + model + '.mo) or ref (' + model + '.ref) file found in tool or model directories' )
    sys.exit( 1 )

# Set up Modelica file
nam = model
if model_inp.endswith( '.mo' ): # Direct Modelica input file
    mod = model_inp
    branch = commit = None
else: # Find Modelica input file from .ref file
    assert model_inp.endswith( '.ref' ), 'Input file should be a .mo or .ref'
    mod = None
    try:
        with open( model_inp, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as ref:
            line_1 = ref.readline().rstrip( '\n' )
            if line_1 == 'Buildings': # Uses Buildings Library but model is local .mo
                lib = 'Buildings'
                model_base = model_inp[:-3]
                if os.path.isfile( model_base + 'mo' ):
                    mod = model_base + 'mo'
                else:
                    print( 'Error: No Modelica (' + model_base + 'mo) file found in .ref file directory' )
                    sys.exit( 1 )
            elif line_1.startswith( 'Buildings.' ):
                nam = line_1
                lib = 'Buildings'
            elif line_1.startswith( 'Modelica.' ):
                nam = line_1
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
        print( '<Model name in Buildings or Modelica Library>|Buildings|<blank to use local .mo file>' )
        print( '[Buildings library branch name]' )
        print( '[Buildings library commit hash]' )
        print( '\nRef file example:' )
        print( 'Buildings.ThermalZones.Detailed.Validation.BESTEST.Cases6xx.Case600' )
        sys.exit( 1 )

# Set FMU compilation options
compiler_options = {}
compiler_options[ 'automatic_tearing' ] = args.tearing
compiler_options[ 'generate_mof_files' ] = args.mof
compiler_options[ 'generate_html_diagnostics' ] = args.diag
compiler_options[ 'disable_smooth_events' ] = False
if tool == 'OCT':
    compiler_options[ 'event_indicator_scaling' ] = args.qss
    compiler_options[ 'event_indicator_structure' ] = args.qss
    compiler_options[ 'event_output_vars' ] = args.qss
    compiler_options[ 'time_events' ] = args.qss
    compiler_options[ 'time_state_variable' ] = args.qss
    compiler_options[ 'include_protected_variables' ] = args.qss # Include protected variable info in XML
    compiler_options[ 'enable_lazy_evaluation' ] = args.lazy # Can cause FMU to give wrong derivatives # Can cause event indicator infinite loop with incomplete dependencies
    compiler_options[ 'generate_ode_jacobian' ] = args.dd # For directional derivatives # Doesn't support delay() # Causes some Buildings library models to abort in PyFMI
    compiler_options[ 'event_indicator_structure' ] = args.deps # For <Dependencies> annotation
    #compiler_options[ 'source_code_fmu' ] = args.source # Not supported by OCT yet: Not present in latest non-end-user OCT
    #compiler_options[ 'msvs_version' ] = '2017' # This seems to happen automatically when MSVS2017 is installed
    #compiler_options[ 'msvs_version' ] = '2019' # Not supported yet
else: # JModelica
    assert tool == 'JModelica', 'Tool should be OCT or JModelica'
    compiler_options[ 'copy_source_files_to_fmu' ] = args.source

# Set up to use model-specific Buildings Library if branch or commit specified
if branch or commit:

    # Model-specific Buildings Library setup
    try: # Create directory for model-specific Buildings Library
        buildings_dir = ( os.getenv( 'TEMP' ) + '\\' if os.name == 'nt' else '~/tmp/' ) + model + '_buildings'
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
        fmu_file = pymodelica.compile_fmu(
         nam,
         version = "2.0",
         compiler_log_level = 'warning',
         compiler_options = compiler_options
        )
        if nam != model: # Rename outputs to local model name
            nam = nam.replace( '.', '_' )
            nam_fmu = nam + '.fmu'
            if os.path.isfile( nam_fmu ): # Rename the FMU
                mdl_fmu = model + '.fmu'
                try:
                    if os.path.isfile( mdl_fmu ): os.remove( mdl_fmu )
                    os.rename( nam_fmu, mdl_fmu )
                except:
                    print( 'Warning: Renaming FMU failed:', nam_fmu, '->', mdl_fmu )
            nam_log = nam + '_log.txt'
            if os.path.isfile( nam_log ): # Rename the log
                mdl_log = model + '_log.txt'
                try:
                    if os.path.isfile( mdl_log ): os.remove( mdl_log )
                    os.rename( nam_log, mdl_log )
                except:
                    print( 'Warning: Renaming log failed:', nam_log, '->', mdl_log )
            nam_dia = nam + '_html_diagnostics'
            if os.path.isdir( nam_dia ): # Rename the HTML diagnostics folder
                mdl_dia = model + '_html_diagnostics'
                try:
                    if os.path.isdir( mdl_dia ): shutil.rmtree( mdl_dia )
                    os.rename( nam_dia, mdl_dia )
                except:
                    print( 'Warning: Renaming diagnostics failed:', nam_dia, '->', mdl_dia )
except Exception as err:
    print( '\nError: FMU compilation failed:', err )
    print( '\nUsage:', os.path.basename( sys.argv[ 0 ] ), '<path' + os.sep + 'model>.[mo|ref]' )
    sys.exit( 1 )

# Extract modelDescription.xml
if args.xml:
    try:
        if sys.version_info >= ( 3, 0 ):
            subprocess.call( 'unzip -o ' + model + '.fmu modelDescription.xml', stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
        else:
            DEVNULL = open( os.devnull, 'w' )
            subprocess.call( 'unzip -o ' + model + '.fmu modelDescription.xml', stdout = DEVNULL, stderr = DEVNULL, shell = True )
    except Exception as err:
        print( 'modelDescription.xml extraction failed for model: ', model, ': ', err )
