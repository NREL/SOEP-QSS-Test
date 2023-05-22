#!/usr/bin/env python

# Generate YAML file with header info for PyFMI QSS comparison runs
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
# Run from an environment set up for PyFMI and QSS

# Imports
import datetime, os, shutil, subprocess, sys

def cmp_PyFMI_QSS_hdr( ofile, date_time = None ):
    with open( ofile, 'w', newline = '\n' ) as log:
        log.write( '---\n' )
        log.write( 'cmp_PyFMI_QSS:\n' )
        log.write( '  DateTime: ' + ( date_time if date_time else datetime.datetime.now().isoformat( timespec = 'seconds' ) ) + '\n' )
#       log.write( '  DateTime: ' + ( date_time if date_time else datetime.datetime.now( tz = datetime.datetime.now( datetime.timezone.utc ).astimezone().tzinfo ).isoformat( timespec = 'seconds' ) ) + '\n' ) # UTC offset variant
        log.write( '  Tools:\n' )
        log.write( '    OCT:\n' )
        if ( os.getenv( 'OCT_BIN_HOME' ) is None ) or ( os.getenv( 'OCT_HOME' ) is None ): print( 'OCT environment is not set up' )
        try:
            oct_version_file = os.path.join( os.environ[ 'OCT_BIN_HOME' ], 'version.txt' )
            with open( oct_version_file, 'r' ) as ver:
                oct_version = ver.readline().strip()
                prefix = 'OCT version '
                if oct_version.startswith( prefix ): oct_version = oct_version[ len( prefix ) : ]
        except:
            oct_version = '?'
        log.write( '      Version: ' + oct_version + '\n' )
        try:
            oct_install_file = os.path.join( os.environ[ 'OCT_HOME' ], 'version.txt' )
            with open( oct_install_file, 'r' ) as ver:
                oct_install = ver.readline().strip()
        except:
            oct_install = '?'
        log.write( '      Install: ' + oct_install + '\n' )
        try:
            oct_pyfmi_file = os.path.join( os.environ[ 'OCT_HOME' ], 'Python', 'pyfmi', 'version.txt' )
            with open( oct_pyfmi_file, 'r' ) as ver:
                oct_pyfmi = ver.readline().strip()
        except:
            oct_pyfmi = '?'
        log.write( '    PyFMI:\n' )
        log.write( '      Version: ' + oct_pyfmi + '\n' )
        log.write( '    QSS:\n' )
        if shutil.which( 'QSS' ) is None: print( 'QSS is not on PATH' )
        try:
            qss_version = subprocess.run( [ 'QSS', '--version' ], check = True, capture_output = True ).stdout.decode().strip().split( '\n' )[ 0 ]
            iVersion = qss_version.index( 'Version: ' )
            qss_version = qss_version[ iVersion + 9 : ]
        except:
            qss_version = '?'
        log.write( '      Version: ' + qss_version + '\n' )
        log.write( '  Models:\n' )

if __name__ == '__main__':
    yaml_file_name = sys.argv[ 1 ] if len( sys.argv ) > 1 else 'cmp.yaml'
    date_time = sys.argv[ 2 ] if len( sys.argv ) > 2 else None
    cmp_PyFMI_QSS_hdr( yaml_file_name, date_time )
