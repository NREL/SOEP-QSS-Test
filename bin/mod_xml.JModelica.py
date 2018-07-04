#!/usr/bin/env python

# JModelica modelDescription.xml Modification for QSS Solver Script
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (http://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017-2018 Objexx Engineerinc, Inc. All rights reserved.
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

# Imports
import sys

# Read input xml file
try:
    xmlname = sys.argv[ 1 ]
except:
    xmlname = 'modelDescription.xml'
try:
    with open( xmlname, 'rU' ) as f:
        lines = [ line for line in f ]
except:
    print( '\nInput open failed: ' + xmlname )
    sys.exit( 1 )

# Open output xml file: Will overwrite local file
try:
    xmlname = 'modelDescription.xml'
    if sys.version_info >= ( 3, 0 ):
        xmlfile = open( xmlname, 'w', newline = '\n' )
    else:
        xmlfile = open( xmlname, 'wb' )
except:
    print( '\nOutput open failed: ' + xmlname )
    sys.exit( 1 )

# Process and write xml lines
inModelVariables = False
iVars = 0
for line in lines:
    write_line = True
    if '<ModelVariables>' in line:
        inModelVariables = True
    elif '</ModelVariables>' in line:
        inModelVariables = False
    elif inModelVariables:
        if '<!-- Variable with index #' in line: # Remove pymodelica comment
            write_line = False
        elif '<ScalarVariable' in line: # Add index comment using Dymola's format
            pre = line[ : line.index( '<ScalarVariable' ) ]
            iVars += 1
            xmlfile.write( pre + '<!-- Index for next variable = ' + str( iVars ) + ' -->\n' )
    if write_line: xmlfile.write( line )

# Close output xml file
xmlfile.close()
