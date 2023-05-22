#!/usr/bin/env python

# Convert a CSV Data File to ASCII
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
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

# Imports
import getopt, os, re, string, sys

def main():

    # Open input file
    if len( sys.argv ) != 2: raise IOError( 'One CSV file argument required' )
    iname = sys.argv[ 1 ]
    if iname == '': raise IOError( 'No input file specified' )
    ifile = open( iname, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' )

    # Open output file
    base = os.path.splitext( os.path.basename( iname ) )[ 0 ]
    oname = base + '.out'
    if sys.version_info >= ( 3, 0 ):
        ofile = open( oname, 'w', newline = '\n' )
    else:
        ofile = open( oname, 'wb' )

    # Process the input file
    line = ifile.readline().rstrip( '\n' )
    if line.startswith( 'time,' ): line = ifile.readline().rstrip( '\n' ) # Skip heading
    while line:
        line = line.split( ',' )
        if len( line ) < 2: raise IOError( 'CSV line without 2 entries' )
        ofile.write( line[ 0 ] + '\t' + line[ 1 ] + '\n' )
        line = ifile.readline().rstrip( '\n' )

    # Close files
    ifile.close()
    ofile.close()
    print( 'ASCII file written to ' + oname )

# Runner
if __name__ == '__main__':
    main()
