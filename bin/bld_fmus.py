#!/usr/bin/env python

# Builds all OCT FMUs in the repository
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.5+
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
#  Run from an environment with MODELICAPATH and MODELICA_BUILDINGS_LIB set up

# Imports
import argparse, os, subprocess, sys

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument( '--qss', help = 'QSS options (OCT)  [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-qss', help = 'No QSS options (OCT)', dest = 'qss', action = 'store_false' )
parser.add_argument( '--lazy', help = 'Enable lazy evaluation (OCT)  [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--no-lazy', help = 'Disable lazy evaluation (OCT)', dest = 'lazy', action = 'store_false' )
parser.add_argument( '--dd', help = 'Enable directional derivatives (OCT)  [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--no-dd', help = 'Disable directional derivatives (OCT)', dest = 'dd', action = 'store_false' )
parser.add_argument( '--source', help = 'Generate FMU source (JModelica)  [Off]', default = False, action = 'store_true' )
parser.add_argument( '--diag', help = 'Generate HTML diagnostics  [On if --qss]', default = None, action = 'store_true' )
parser.add_argument( '--xml', help = 'Extract modelDescription.xml from FMU  [On]', default = True, action = 'store_true' )
parser.add_argument( '--no-xml', help = 'Don\'t extract modelDescription.xml from FMU', dest = 'xml', action = 'store_false' )
args = parser.parse_args()
if args.qss: # Set up conditional defaults
    if args.lazy is None: args.lazy = True
    if args.dd is None: args.dd = True
    if args.diag is None: args.diag = True

# Set up pass-through arguments
args = ' '.join( sys.argv[1:] )

# Check Modelica environment is set up
if not os.getenv( 'MODELICAPATH' ):
    print( 'Error: MODELICAPATH environment variable is not set' )
    sys.exit( 1 )

# Check Modelica Buildings library environment is set up
if not os.getenv( 'MODELICA_BUILDINGS_LIB' ):
    print( 'Error: Modelica Buildings Library environment is not set up' )
    sys.exit( 1 )

# Find and change to local model directory
mdl = os.path.splitext( os.path.basename( os.getcwd() ) )[0]
if ( mdl != 'mdl' ) and ( 'mdl' in os.listdir() ): os.chdir( 'mdl' )
mdl_dir = os.getcwd()

# Walk the model directory and build the OCT FMUs
for dir in os.listdir():
    OCT_dir =  os.path.join( dir, 'OCT' )
    if os.path.isdir( OCT_dir ):
        os.chdir( OCT_dir )
        try:
            if sys.version_info >= ( 3, 0 ):
                ret = subprocess.check_call( 'bld_fmu.py' + args, shell = True )
                ret.check_returncode()
            else:
                ret = subprocess.check_call( 'bld_fmu.py' + args, shell = True )
        except Exception as err:
            print( 'FMU build failed for model: ', dir, ': ', err )
        else:
            print( 'FMU built for model: ', dir )
        os.chdir( mdl_dir )
