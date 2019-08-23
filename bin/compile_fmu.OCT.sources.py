#!/usr/bin/env python

# Compiles a Modelica file using the Buildings library with OCT
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (https://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017-2019 Objexx Engineering, Inc. All rights reserved.
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
#  Run from an environment with MODELICAPATH set up as in export MODELICAPATH=/opt/OCT/ThirdParty/MSL:/opt/modelica-buildings

# Imports
import os, sys
from pymodelica import compile_fmu

try:
    MODELICAPATH = os.getenv( 'MODELICAPATH' )
except:
    print( 'Error: MODELICAPATH environment variable is not set' )
    sys.exit( 1 )

try:
    model = sys.argv[ 1 ]
    if model.endswith( '.mo' ): model = model[ :-3 ]
    model_file = sys.argv[ 2 ] if len( sys.argv ) > 2 else model + '.mo'
    if os.name == 'nt':
        compiler_options = {
         'generate_html_diagnostics': False,
         'generate_ode_jacobian': True,
         'enable_lazy_evaluation': True,
         'event_indicator_structure': True,
         'event_output_vars': True,
         'time_events': True,
         'source_code_fmu': True,
        }
    else:
        compiler_options = {
         'generate_html_diagnostics': False,
         'generate_ode_jacobian': True,
#        'enable_lazy_evaluation': True, # Not currently supported by Linux OCT
         'event_indicator_structure': True,
         'event_output_vars': True,
         'time_events': True,
         'source_code_fmu': True,
        }
    fmu_file = compile_fmu(
     os.path.basename( model ),
     model_file,
     version = "2.0",
     compiler_log_level = 'error',
     compiler_options = compiler_options,
    )
except Exception as msg:
    print( 'Error: ' + str( msg ) )
    print( 'Usage options:' )
    print( ' ' + os.path.basename( sys.argv[ 0 ] ) + ' <model_name> [<mo_file_name>]' )
    print( ' ' + os.path.basename( sys.argv[ 0 ] ) + ' <mo_file_name>' )
