#!/usr/bin/env python

# Finds and runs the model's OCT FMU with PyFMI or QSS: reference solution
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.5+
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
#  Run from an environment set up for PyFMI and/or QSS

# Imports
import os, subprocess, sys

# Set up pass-through arguments
args = ' --rTol=1e-8'
red = 'run.log'
for arg in sys.argv[1:]:
    if arg.startswith( ( '--red=', '--red:' ) ): # Redirect
        red = arg[6:].strip()
    else: # Pass-through argument
        args += ' ' + arg

# Find tool directory and name
tools = ( 'QSS', 'OCT', 'JModelica' )
tool_dir = os.getcwd()
tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
while tool not in tools: # Move up one directory level
    tool_dir = os.path.dirname( tool_dir )
    tool = os.path.splitext( os.path.basename( tool_dir ) )[0]
    if os.path.splitdrive( tool_dir )[1] == os.sep: # At top of drive/mount
        tool_dir = tool = ''
        break
if not tool:
    print( 'Error: Not in/under a directory named for a supported simulation tool: ', tools )
    sys.exit( 1 )

# Run Simulation
try:
    if sys.version_info >= ( 3, 0 ):
        if tool == 'QSS':
            if red: # Redirect
                if red == 'nul': # Discard
                    subprocess.check_call( 'run_QSS.py' + args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
                else: # File
                    with open( red, 'w', newline = '\n' ) as log:
                        subprocess.check_call( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
            else: # Don't redirect
                subprocess.check_call( 'run_QSS.py' + args, shell = True )
        else: # PyFMI
            if red: # Redirect
                if red == 'nul': # Discard
                    subprocess.check_call( 'run_PyFMI.py' + args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
                else: # File
                    with open( red, 'w', newline = '\n' ) as log:
                        subprocess.check_call( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
            else: # Don't redirect
                subprocess.check_call( 'run_PyFMI.py' + args, shell = True )
    else:
        if tool == 'QSS':
            if red: # Redirect
                if red == 'nul': # Discard
                    DEVNULL = open( os.devnull, 'w' )
                    subprocess.check_call( 'run_QSS.py' + args, stdout = DEVNULL, stderr = DEVNULL, shell = True )
                else: # File
                    with open( red, 'wb' ) as log:
                        subprocess.check_call( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
            else: # Don't redirect
                subprocess.check_call( 'run_QSS.py' + args, shell = True )
        else: # PyFMI
            if red: # Redirect
                if red == 'nul': # Discard
                    DEVNULL = open( os.devnull, 'w' )
                    subprocess.check_call( 'run_PyFMI.py' + args, stdout = DEVNULL, stderr = DEVNULL, shell = True )
                else: # File
                    with open( red, 'wb' ) as log:
                        subprocess.check_call( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
            else: # Don't redirect
                subprocess.check_call( 'run_PyFMI.py' + args, shell = True )
except Exception as err:
    print( 'Simulation failed: ', err )
    sys.exit( 1 )
