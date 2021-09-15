#!/usr/bin/env python

# Compare YAML files for two PyFMI vs QSS comparison runs
#
# Project: QSS Solver
#
# Language: Python 3.5+
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

# Imports
import sys, yaml

def indent_lines( s, indent = 1 ):
    o = s.split( '\n' )
    for i in range( len( o ) ):
        o[ i ] = indent * '  ' + o[ i ]
    o = '\n'.join( o )
    return o

def dump( d, indent = 1 ):
    if isinstance( d, dict ):
        return indent_lines( yaml.dump( d, sort_keys=False ).rstrip( '\n' ), indent )
    else:
        return indent_lines( str( d ), indent )

def rtol_ne( x, y, rtol ):
    if rtol > 0.0:
        return abs( x - y ) > rtol * max( abs( x ), abs( y ) )
    else:
        return x != y

# Get YAML file name arguments
try:
    yaml_1 = sys.argv[ 1 ]
    yaml_2 = sys.argv[ 2 ]
except:
    print( 'Error: YAML files to compare not specified on command line' )
    sys.exit( 1 )
print( '\nComparing:\n' + '[1] ' + yaml_1 + '\n' + '[2] ' + yaml_2 + '\n' )
try:
    yaml_file_1 = open( yaml_1, 'r' )
    yaml_file_2 = open( yaml_2, 'r' )
except:
    print( 'Error: YAML file open failed' )
    try:
        yaml_file_1.close()
        yaml_file_2.close()
    except:
        pass
    sys.exit( 1 )
try:
    yaml_dict_1 = yaml.safe_load( yaml_file_1 )
    yaml_dict_2 = yaml.safe_load( yaml_file_2 )
except:
    print( 'Error: YAML file load failed' )
    sys.exit( 1 )
finally:
    yaml_file_1.close()
    yaml_file_2.close()

# Report meta info differences ###

if 'cmp_PyFMI_QSS' not in yaml_dict_1:
    print( 'Error: YAML file 1 does not start with cmp_PyFMI_QSS' )
    sys.exit( 1 )
if 'cmp_PyFMI_QSS' not in yaml_dict_2:
    print( 'Error: YAML file 2 does not start with cmp_PyFMI_QSS' )
    sys.exit( 1 )
content_1 = yaml_dict_1[ 'cmp_PyFMI_QSS' ]
content_2 = yaml_dict_2[ 'cmp_PyFMI_QSS' ]

datetime_1 = content_1[ 'DateTime' ] # PyYAML interprets this as a datetime object
datetime_1 = datetime_1.isoformat( timespec = 'seconds' )
datetime_2 = content_2[ 'DateTime' ] # PyYAML interprets this as a datetime object
datetime_2 = datetime_2.isoformat( timespec = 'seconds' )
print( '[1] DateTime: ' + datetime_1 )
print( '[2] DateTime: ' + datetime_2 )

tools_1 = content_1[ 'Tools' ]
tools_2 = content_2[ 'Tools' ]
tools_first = True

oct_1 = tools_1[ 'OCT' ]
oct_2 = tools_2[ 'OCT' ]
if oct_1 != oct_2:
    if tools_first:
        print( '\nTools:' )
        tools_first = False
    print( '  [1] OCT:' )
    print( dump( oct_1, 2 ) )
    print( '  [2] OCT:' )
    print( dump( oct_2, 2 ) )

pyfmi_1 = tools_1[ 'PyFMI' ]
pyfmi_2 = tools_2[ 'PyFMI' ]
if pyfmi_1 != pyfmi_2:
    if tools_first:
        print( '\nTools:' )
        tools_first = False
    print( '  [1] PyFMI:' )
    print( dump( pyfmi_1, 2 ) )
    print( '  [2] PyFMI:' )
    print( dump( pyfmi_2, 2 ) )

qss_1 = tools_1[ 'QSS' ]
qss_2 = tools_2[ 'QSS' ]
if qss_1 != qss_2:
    if tools_first:
        print( '\nTools:' )
        tools_first = False
    print( '  [1] QSS:' )
    print( dump( qss_1, 2 ) )
    print( '  [2] QSS:' )
    print( dump( qss_2, 2 ) )
if tools_first:
    print( '\nTools: Match' )

# Report model variable differences
try:
    rtol = abs( float( sys.argv[ 3 ] ) )
except:
    rtol = 0.0
print( '\nModels:' )
mdls_1 = content_1[ 'Models' ]
mdls_2 = content_2[ 'Models' ]
for mdl_1 in mdls_1:
    mdl_name = mdl_1[ 'Name' ]
    for mdl_2 in mdls_2:
        if mdl_2[ 'Name' ] == mdl_name: break
    if mdl_2[ 'Name' ] != mdl_name: continue # No matching model found
    if mdl_1 == mdl_2:
        print( '  ' + mdl_name + ': Match' )
    else:
        match = True

        pyfmi_1 = mdl_1[ 'PyFMI' ]
        pyfmi_2 = mdl_2[ 'PyFMI' ]
        if pyfmi_1 != pyfmi_2:
            if match:
                print( '  ' + mdl_name + ':' )
                match = False
            print( '      [1] PyFMI:' )
            print( dump( pyfmi_1, 4 ) )
            print( '      [2] PyFMI:' )
            print( dump( pyfmi_2, 4 ) )

        qss_1 = mdl_1[ 'QSS' ]
        qss_2 = mdl_2[ 'QSS' ]
        if qss_1 != qss_2:
            if match:
                print( '  ' + mdl_name + ':' )
                match = False
            print( '      [1] QSS:' )
            print( dump( qss_1, 4 ) )
            print( '      [2] QSS:' )
            print( dump( qss_2, 4 ) )

        vars_1 = mdl_1[ 'Var' ]
        vars_2 = mdl_2[ 'Var' ]
        if vars_1 != vars_2:
            for var_1 in vars_1:
                var_nam = var_1[ 'Name' ]
                for var_2 in vars_2:
                    if var_2[ 'Name' ] == var_nam: break
                if var_2[ 'Name' ] != var_nam: continue # No matching variable found
                if var_1 != var_2:
                    rms_1 = var_1[ 'RMS' ]
                    rms_2 = var_2[ 'RMS' ]
                    val_1 = float( rms_1[ 'Val' ] )
                    val_2 = float( rms_2[ 'Val' ] )
                    lim_1 = float( rms_1[ 'Lim' ] )
                    lim_2 = float( rms_2[ 'Lim' ] )
                    sta_1 = val_1 <= lim_1
                    sta_2 = val_2 <= lim_2
                    if rtol_ne( val_1, val_2, rtol ) or ( sta_1 != sta_2 ):
                        if match:
                            print( '  ' + mdl_name + ':' )
                            match = False
                        print( '    ' + var_nam + ':' )
                        print( '      RMS:' )
                        print( '        [1] Val: ' + dump( val_1, 0 ) + ( ' (Pass)' if sta_1 else ' (Fail)' ) )
                        print( '        [2] Val: ' + dump( val_2, 0 ) + ( ' (Pass)' if sta_2 else ' (Fail)' ) )
                    elif lim_1 != lim_2:
                        if match:
                            print( '  ' + mdl_name + ':' )
                            match = False
                        print( '    ' + var_nam + ':' )
                        print( '      RMS:' )
                    if lim_1 != lim_2:
                        if match:
                            print( '  ' + mdl_name + ':' )
                            match = False
                        print( '        [1] Lim: ' + dump( lim_1, 0 ) )
                        print( '        [2] Lim: ' + dump( lim_2, 0 ) )

        if match:
            print( '  ' + mdl_name + ': Match' )
