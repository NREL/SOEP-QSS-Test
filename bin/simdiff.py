#!/usr/bin/env python

# Simulation Signal Comparison Tool
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (https://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017-2022 Objexx Engineering, Inc. All rights reserved.
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
#  Inputs can be file names or a file and a directory, and can use wildcards
#   Only one file for each variable name is used in each input list
#   Variable spec lists can be supplied to filter the input lists
#   The logic attempts to match up files to compare in a non-surprising way
#   For more complex scenarios use a wrapper script to feed two files at a time to this script
#  Intended for comparison of simulation results containing a mix of text and numeric values
#  Tokens can be whitespace or comma separated
#  Numeric data columns quantities are assumed to be the same in both files
#  Interpolated and plotted results assume col 1 is the x-axis for the other columns

# Imports
import argparse, datetime, fastnumbers, fnmatch, glob, math, os, re, sys

# Globals
args = None
infinity = float( 'inf' )

def sim_diff():
    '''Compare simulation signal files'''

    # Save the current day+time
    now = datetime.datetime.utcnow()

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument( 'inp1', help = 'input 1' )
    parser.add_argument( 'inp2', help = 'input 2' )
    parser.add_argument( '--var', help = 'variable file' )
    parser.add_argument( '--rTol', help = 'relative tolerance  [1e-4]', type = float, default = 1.0e-3 )
    parser.add_argument( '--rtol', dest = 'rTol', help = argparse.SUPPRESS )
    parser.add_argument( '--rToly', dest = 'rTol', help = argparse.SUPPRESS )
    parser.add_argument( '--rTolY', dest = 'rTol', help = argparse.SUPPRESS )
    parser.add_argument( '--rtoly', dest = 'rTol', help = argparse.SUPPRESS )
    parser.add_argument( '--ltoly', dest = 'rTol', help = argparse.SUPPRESS )
    parser.add_argument( '--rTolx', help = 'x-axis relative tolerance  [0]', type = float, default = 0.0 )
    parser.add_argument( '--rTolX', dest = 'rTolx', help = argparse.SUPPRESS )
    parser.add_argument( '--rtolx', dest = 'rTolx', help = argparse.SUPPRESS )
    parser.add_argument( '--ltolx', dest = 'rTolx', help = argparse.SUPPRESS )
    parser.add_argument( '--aTol', help = 'absolute tolerance  [1e-6]', type = float, default = 1.0e-6 )
    parser.add_argument( '--atol', dest = 'aTol', help = argparse.SUPPRESS )
    parser.add_argument( '--aToly', dest = 'aTol', help = argparse.SUPPRESS )
    parser.add_argument( '--aTolY', dest = 'aTol', help = argparse.SUPPRESS )
    parser.add_argument( '--atoly', dest = 'aTol', help = argparse.SUPPRESS )
    parser.add_argument( '--aTolx', help = 'x-axis absolute tolerance  [0]', type = float, default = 0.0 )
    parser.add_argument( '--aTolX', dest = 'aTolx', help = argparse.SUPPRESS )
    parser.add_argument( '--atolx', dest = 'aTolx', help = argparse.SUPPRESS )
    parser.add_argument( '--sequential', help = "compare non-numeric lines  [F]", action = 'store_true' )
    parser.add_argument( '--no-sync', help = "don't sync numeric block  [F]", dest = 'sync', action = 'store_false' )
    parser.add_argument( '--no-interp', help = "don't interpolate (interp => sync)  [F]", dest = 'interp', action = 'store_false' )
    parser.add_argument( '--coarse', help = "compare at coarser signal's steps  [F]", action = 'store_true' )
    parser.add_argument( '--plot', help = 'plot signals  [F]', action = 'store_true' )
    parser.add_argument( '--plot-fail', help = 'plot signals if fail (=> interp)  [F]', action = 'store_true' )
    parser.add_argument( '--pyfunnel', help = 'pyfunnel signals  [F]', action = 'store_true' )
    parser.add_argument( '--pyfunnel-fail', help = 'pyfunnel failed signals  [F]', action = 'store_true' )
    parser.add_argument( '--dpi', help = 'screen dpi for plot', type = int, default = 0 )
    parser.add_argument( '--out', help = 'output to file(s)  [F]', action = 'store_true' )
    parser.add_argument( '-v', '--verbose', help = 'verbose report  [F]', action = 'store_true' )
    parser.set_defaults( sync = True, interp = True )
    global args
    args = parser.parse_args()
    if args.plot_fail or args.pyfunnel_fail: args.interp = True # Plot-on-fail => Interp
    if args.interp: args.sync = True # Interpolation => Sync

    # Generate input lists
    inp1 = args.inp1
    if ( '[' in inp1 ) or ( ']' in inp1 ): # Escape the brackets
        inp1 = re.sub( r'([\[\]])', '[\\1]', inp1 )
    if os.path.isdir( inp1 ):
        glob1 = glob.glob( os.path.join( inp1, '*.out' ) )
        if not glob1: glob1 = glob.glob( os.path.join( inp1, 'out', '*.out' ) )
    else:
        glob1 = glob.glob( inp1 )
        if not glob1: glob1 = glob.glob( inp1 + '.out' )
        if not glob1: glob1 = glob.glob( inp1 + '.*.out' )
    glob1 = [ fnam for fnam in glob1 if os.path.isfile( fnam ) ]
    inp2 = args.inp2
    if ( '[' in inp2 ) or ( ']' in inp2 ): # Escape the brackets
        inp2 = re.sub( r'([\[\]])', '[\\1]', inp2 )
    if os.path.isdir( inp2 ):
        glob2 = glob.glob( os.path.join( inp2, '*.out' ) )
        if not glob2: glob2 = glob.glob( os.path.join( inp2, 'out', '*.out' ) )
    else:
        glob2 = glob.glob( inp2 )
        if not glob2: glob2 = glob.glob( inp2 + '.out' )
        if not glob2: glob2 = glob.glob( inp2 + '.*.out' )
    glob2 = [ fnam for fnam in glob2 if os.path.isfile( fnam ) ]
    if not ( glob1 and glob2 ):
        if not glob1: print( '\nNo dirs|files found matching: ' + args.inp1 )
        if not glob2: print( '\nNo dirs|files found matching: ' + args.inp2 )
        sys.exit( 1 )
    for i in range( len( glob1 ) ): glob1[ i ] = os.path.abspath( glob1[ i ] )
    for i in range( len( glob2 ) ): glob2[ i ] = os.path.abspath( glob2[ i ] )

    # Generate input map by variable name: Only one (best) entry per variable
    typeB = ( '', '.x', '.f', '.q' ) # Signal types in decreasing match preference order
    eextB = ( '.x.out', '.f.out', '.q.out' ) # QSS extended extension types
    vars1 = {}
    for fnam in glob1:
        if 'QSS' in fnam.split( os.sep ) or os.path.basename( fnam ).endswith( eextB ): # Split QSS variable and type
            snam = vnam, tnam = qss_sig_name( fnam )
        else:
            snam = vnam, tnam = ( sig_name( fnam ), '' )
        if vnam in vars1:
            if tnam == '': # Preferred
                vars1[ vnam ] = fnam
            else: # Choose preferred signal types
                try:
                    if typeB.index( tnam ) < typeB.index( typ_name( vars1[ vnam ] ) ): # Better match
                        vars1[ vnam ] = fnam
                except: # Unexpected signal type
                    pass # Keep current best match
        else:
            vars1[ vnam ] = fnam
    vars2 = {}
    for fnam in glob2:
        if 'QSS' in fnam.split( os.sep ) or os.path.basename( fnam ).endswith( eextB ): # Split QSS variable and type
            snam = vnam, tnam = qss_sig_name( fnam )
        else:
            snam = vnam, tnam = ( sig_name( fnam ), '' )
        if vnam in vars2:
            if tnam == '': # Preferred
                vars2[ vnam ] = fnam
            else: # Choose preferred signal types
                try:
                    if typeB.index( tnam ) < typeB.index( typ_name( vars2[ vnam ] ) ): # Better match
                        vars2[ vnam ] = fnam
                except: # Unexpected signal type
                    pass # Keep current best match
        else:
            vars2[ vnam ] = fnam

    # Filter by variable spec list
    if args.var:

        # Read variable spec list
        vspcs = []
        with open( args.var, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' ) as var_file:
            for line in var_file:
                key = line.strip()
                if key and ( key[ 0 ] != '#' ):
                    vspcs.append( key )

        # Filter input 1
        for vnam in vars1.keys():
            if vnam not in vspcs: # See if it matches a wildcard|regexx
                m = False
                for vspc in vspcs:
                    m = fnmatch.filter( [ vnam ], vspc ) # File name wildcard pattern
                    if not m: # Try as regex
                        if not vspc.endswith( '$' ): vspc += '$' # Match whole string
                        if re.match( vspc, vnam ): m = True
                    if m: break
                if not m: del( vars1[ vnam ] )

        # Filter input 2
        for vnam in vars2.keys():
            if vnam not in vspcs: # See if it matches a wildcard|regexx
                m = False
                for vspc in vspcs:
                    m = fnmatch.filter( [ vnam ], vspc ) # File name wildcard pattern
                    if not m: # Try as regex
                        if not vspc.endswith( '$' ): vspc += '$' # Match whole string
                        if re.match( vspc, vnam ): m = True
                    if m: break
                if not m: del( vars2[ vnam ] )

        # Check if any variables
        if not ( vars1 and vars2 ):
            if not vars1: print( '\nNo variables matching --var list in: ' + args.inp1 )
            if not vars2: print( '\nNo variables matching --var list in: ' + args.inp2 )
            sys.exit( 1 )

    # Compare signals
    n_passed = 0
    n_failed = 0
    out_name = ''
    for vnam in sorted( vars1.keys() ):
        if vnam in vars2:
            path1 = vars1[ vnam ]
            path2 = vars2[ vnam ]
            if path2 != path1:
                passed, onam = sig_compare( path1, path2 )
                if passed:
                    n_passed += 1
                else:
                    n_failed += 1
                if not out_name:
                    out_name = onam
                else:
                    out_name = os.path.commonprefix( [ out_name, onam ] )
    out_name = out_name.rstrip( '.' )

    # Report summary
    if args.out:
        try: # Open summary output file
            if not out_name: out_name = 'Summary'
            if sys.version_info >= ( 3, 0 ):
                sys.stdout = open( out_name + '.sum', 'w', newline = '\n' )
            else:
                sys.stdout = open( out_name + '.sum', 'wb' )
        except:
            print( 'Summary file open failed' )
        try:
            for ext in ( '.pass', '.fail' ): # Clean any prior pass/fail files
                if os.path.isfile( out_name + ext ): os.remove( out_name + ext )
            if sys.version_info >= ( 3, 0 ):
                PF_file = open( out_name + ( '.pass' if n_failed == 0 else '.fail' ), 'w', newline = '\n' )
            else:
                PF_file = open( out_name + ( '.pass' if n_failed == 0 else '.fail' ), 'wb' )
            PF_file.close()
        except:
            print( 'Pass/Fail file write failed' )
    else:
        print( '' )
    print( 'Summary @ UTC ' + now.strftime( '%Y-%m-%d %H:%M:%S:' ) )
    print( ' Tolerances:  rTol: ' + str( args.rTol ) + '  aTol: ' + str( args.aTol ) )
    print( ' Pass: ' + str( n_passed ) )
    print( ' Fail: ' + str( n_failed ) )

    # Reset stdout
    if args.out:
        sys.stdout = sys.__stdout__
        print( 'Summary written to: ' + out_name + '.sum' )

def sig_name( fnam ):
    '''Signal name of a file name: /path/var.out -> var'''
    return os.path.splitext( os.path.basename( fnam ) )[ 0 ]

def qss_sig_name( fnam ):
    '''Signal name of a QSS file name: /path/var.sig.out -> (var,.sig)'''
    return os.path.splitext( os.path.splitext( os.path.basename( fnam ) )[ 0 ] )

def typ_name( fnam ):
    '''Signal type of a file name: /path/var.sig.out -> .sig'''
    return os.path.splitext( os.path.splitext( os.path.basename( fnam ) )[ 0 ] )[ 1 ]

def sig_compare( fnam1, fnam2 ):
    '''Compare two simulation signal files'''

    # Check/report files
    if ( os.path.getsize( fnam1 ) == 0 ) or ( os.path.getsize( fnam2 ) == 0 ):
        print( '\nSkipping empty file(s):\n' + fnam1 + '\n' + fnam2 )
        return

    # Open the files
    try:
        file1 = open( fnam1, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' )
    except:
        print( '\nOpen failed: ' + fnam1 )
        return
    try:
        file2 = open( fnam2, 'r' if sys.version_info >= ( 3, 0 ) else 'rU' )
    except:
        print( '\nOpen failed: ' + fnam2 )
        return

    # Plot conditional imports
    plotting = args.plot or args.plot_fail
    if args.interp or plotting:
        try:
            import numpy
        except:
            if args.interp:
                print( 'Error: Interpolation diffs unavailable: NumPy is not installed' )
                args.interp = False
            if plotting:
                print( 'Error: Plotting unavailable: NumPy is not installed' )
                plotting = args.plot = args.plot_fail = False
    if plotting:
        try:
            from matplotlib import pyplot
            pyplot.rcParams[ 'axes.formatter.offset_threshold' ] = 3
            if args.dpi > 0:
                pyplot.rcParams[ 'figure.dpi' ] = args.dpi
            elif sys.platform.startswith( 'linux' ): # Scale up to typically usable size
                pyplot.rcParams[ 'figure.dpi' ] = 150
        except:
            print( 'Error: Plotting unavailable: matplotlib is not installed' )
            plotting = args.plot = args.plot_fail = False

    # Pyfunnel conditional imports
    pyfunneling = args.pyfunnel or args.pyfunnel_fail
    if args.interp or pyfunneling:
        if 'numpy' not in sys.modules:
            try:
                import numpy
            except:
                if args.interp:
                    print( 'Error: Interpolation diffs unavailable: NumPy is not installed' )
                    args.interp = False
                if pyfunneling:
                    print( 'Error: Pyfunnel unavailable: NumPy is not installed' )
                    pyfunneling = args.pyfunnel = args.pyfunnel_fail = False
    if pyfunneling:
        try:
            import pyfunnel
        except:
            print( 'Error: Pyfunnel unavailable' )
            pyfunneling = args.pyfunnel = args.pyfunnel_fail = False

    # Argument aliases
    rTol = args.rTol
    aTol = args.aTol
    sequential = args.sequential
    sync = args.sync
    interp = args.interp
    coarse = args.coarse
    plot = args.plot
    plot_fail = args.plot_fail
    plotting = plot or plot_fail
    pyfunnel_it = args.pyfunnel
    pyfunnel_fail = args.pyfunnel_fail
    pyfunneling = pyfunnel_it or pyfunnel_fail
    interp_or_plot_or_pyfunnel = interp or plotting or pyfunneling
    out = args.out
    verbose = args.verbose

    if interp_or_plot_or_pyfunnel or out:
        # Extract model and tool name(s)
        parts1 = fnam1.split( os.sep )
        rdirs1 = reversed( parts1[ : -1 ] )
        tool1 = model1 = ''
        tools = ( 'ana', 'Dymola', 'JModelica', 'OCT', 'Ptolemy', 'PyFMI', 'QSS' )
        for dir in rdirs1:
            if not tool1:
                if ( dir in tools ) or ( 'QSS' in dir ):
                    tool1 = dir
            elif not any( tool in dir for tool in tools ): # Assume model name precedes tool name
                model1 = dir
                break
        try:
            mnam1 = os.path.join( *parts1[ parts1.index( model1 ) : ] )
        except:
            mnam1 = os.path.basename( fnam1 )
        parts2 = fnam2.split( os.sep )
        rdirs2 = reversed( parts2[ : -1 ] )
        tool2 = model2 = ''
        for dir in rdirs2:
            if not tool2:
                if ( dir in tools ) or ( 'QSS' in dir ):
                    tool2 = dir
            elif not any( tool in dir for tool in tools ): # Assume model name precedes tool name
                model2 = dir
                break
        try:
            mnam2 = os.path.join( *parts2[ parts2.index( model2 ) : ] )
        except:
            mnam2 = os.path.basename( fnam2 )

        # Extract variable name(s)
        vnam1 = os.path.splitext( os.path.basename( fnam1 ) )[ 0 ]
        vnam2 = os.path.splitext( os.path.basename( fnam2 ) )[ 0 ]
        if ( len( vnam1 ) > 2 ) and vnam1.endswith( ( '.f', '.q', '.x' ) ): vnam1 = os.path.splitext( vnam1 )[ 0 ]
        if ( len( vnam2 ) > 2 ) and vnam2.endswith( ( '.f', '.q', '.x' ) ): vnam2 = os.path.splitext( vnam2 )[ 0 ]

    # Compare the files
    lnum1 = lnum2 = 0 # Line numbers in files
    line1 = line2 = True # Not at end of files?
    nums1 = nums2 = False # Found numeric lines?
    in_nums1 = in_nums2 = False # In numeric blocks?
    wait1 = wait2 = False # File waiting for other file to reach numeric lines?
    tokens1 = tokens2 = []
    end1 = end2 = False # Reached end of files prev?
    row1_1 = row1_2 = row2_1 = row2_2 = None # 2 previous rows
    lin_diffs = 0
    seq_diffs = 0
    int_diffs = 0
    flt_diffs = 0
    str_diffs = 0
    f_min = f_max = None # min/max floating point differences in line scan
    passed = True
    if interp_or_plot_or_pyfunnel:
        row1_2 = []
        row2_2 = []
        row1_1 = []
        row2_1 = []
        row1 = []
        row2 = []
        cols1 = cols2 = None
        lbls = None
    if out:
        if model1 == model2:
            onam = model1
        else:
            onam = model1 + ( '-' if model1 and model2 else '' ) + model2
        if tool1 == tool2:
            onam += ( '.' if onam else '' ) + tool1
        else:
            onam += ( '.' if onam else '' ) + tool1 + ( '-' if tool1 and tool2 else '' ) + tool2
        if vnam1 == vnam2:
            onam += ( '.' if onam else '' ) + vnam1
        else:
            onam += ( '.' if onam else '' ) + vnam1 + ( '-' if vnam1 and vnam2 else '' ) + vnam2
        try:
            if sys.version_info >= ( 3, 0 ):
                sys.stdout = open( onam + '.rpt', 'w', newline = '\n' )
            else:
                sys.stdout = open( onam + '.rpt', 'wb' )
        except:
            print( 'Report file open failed' )
            sys.exit( 1 )
    else:
        onam = ''
    if not out: print( '' )
    print( 'Comparing:\n ' + mnam1 + '\n ' + mnam2 )
    if sequential: print( 'Sequential:' )
    while line1 or line2:
        if sync: # Read next lines unless waiting for other file to reach numeric lines
            wait1 = ( nums1 and ( not nums2 ) ) or ( interp and nums1 and ( not in_nums1 ) and in_nums2 )
            wait2 = ( nums2 and ( not nums1 ) ) or ( interp and nums2 and ( not in_nums2 ) and in_nums1 )
            if line1 and ( not wait1 ): line1 = file1.readline()
            if line2 and ( not wait2 ): line2 = file2.readline()
        else: # Read next lines unless end of file already reached
            if line1: line1 = file1.readline()
            if line2: line2 = file2.readline()
        old_diffs = seq_diffs
        if ( not line1 ) and ( not line2 ): # Simultaneously reached end of both files
            break
        elif not line1: # Reached end of file1 first
            if verbose and ( not end1 ) and ( not interp ): print( ' File 1: End hit first' )
            if ( not interp ) or ( not nums1 ): seq_diffs += 1
            end1 = True
            in_nums1 = False
        elif not line2: # Reached end of file2 first
            if verbose and ( not end2 ) and ( not interp ): print( ' File 2: End hit first' )
            if ( not interp ) or ( not nums2 ): seq_diffs += 1
            end2 = True
            in_nums2 = False
        if not wait1:
            lnum1 += 1
            sline1 = line1.strip()
            tokens1 = re.split( r'[\s,]+', sline1 ) if sline1 else []
            if tokens1 and tokens1[ 0 ] == '': del tokens1[ 0 ]
            while tokens1 and tokens1[ -1 ] == '': del tokens1[ -1 ]
        if not wait2:
            lnum2 += 1
            sline2 = line2.strip()
            tokens2 = re.split( r'[\s,]+', sline2 ) if sline2 else []
            if tokens2 and tokens2[ 0 ] == '': del tokens2[ 0 ]
            while tokens2 and tokens2[ -1 ] == '': del tokens2[ -1 ]
        if interp_or_plot_or_pyfunnel:
            row1_2 = row1_1
            row2_2 = row2_1
            row1_1 = row1 if not wait1 else []
            row2_1 = row2 if not wait2 else []
            row1 = []
            row2 = []
        l1 = len( tokens1 )
        l2 = len( tokens2 )
        if sequential and ( l1 != l2 ):
            if line1 and line2 and ( not ( sync and ( wait1 or wait2 ) ) ):
                if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ': Different number of tokens' )
                seq_diffs += 1
        num1 = l1 > 0 # Line 1 is all numeric tokens? (initialization)
        num2 = l2 > 0 # Line 2 is all numeric tokens? (initialization)
        for i in range( max( l1, l2 ) ):
            token1 = tokens1[ i ] if i < l1 else None
            token2 = tokens2[ i ] if i < l2 else None
            val1 = fastnumbers.fast_real( token1 ) if token1 else None
            val2 = fastnumbers.fast_real( token2 ) if token2 else None
            if ( val1 is None ) or isinstance( val1, str ): num1 = False
            if ( val2 is None ) or isinstance( val2, str ): num2 = False
            if sequential and ( not ( end1 or end2 ) ) and ( not ( interp and in_nums1 and in_nums2 ) ) and ( val1 != val2 ):
                if isinstance( val1, int ) and isinstance( val2, int ): # Compare as integers
                    if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + token1 + ' | ' + token2 )
                    seq_diffs += 1
                    int_diffs += 1
                elif ( val1 is not None ) and ( not isinstance( val1, str ) ) and ( val2 is not None ) and ( not isinstance( val2, str ) ): # Compare as floats
                    fdiff = abs( val1 - val2 )
                    if f_min is None:
                        f_min = f_max = fdiff
                    elif fdiff < f_min:
                        f_min = fdiff
                    elif fdiff > f_max:
                        f_max = fdiff
                    if fdiff > max( aTol, rTol * max( abs( val1 ), abs( val2 ) ) ): # Exceeds tolerance
                        if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + token1 + ' | ' + token2 )
                        seq_diffs += 1
                        flt_diffs += 1
                else: # Compare tokens as strings
                    if token1 != token2:
                        if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + str( token1 ) + ' | ' + str( token2 ) )
                        seq_diffs += 1
                        str_diffs += 1
            if interp_or_plot_or_pyfunnel:
                if val1 is not None: row1.append( val1 )
                if val2 is not None: row2.append( val2 )
        if interp_or_plot_or_pyfunnel:
            if in_nums1 or in_nums2: # See if past numeric block
                if not num1: in_nums1 = False
                if not num2: in_nums2 = False
            elif num1 and num2 and ( ( not nums1 ) or ( not nums2 ) ): # Numeric block initialization
                in_nums1 = in_nums2 = True
                n_cols = min( len( row1 ), len( row2 ) )
                cols1 = [ [] for i in range( n_cols ) ]
                cols2 = [ [] for i in range( n_cols ) ]
                lbls = [ '' for i in range( n_cols ) ]
                type_row = False
                if not row1_2: row1_2 = [ '' for i in range( n_cols ) ]
                if not row2_2: row2_2 = [ '' for i in range( n_cols ) ]
                if ( len( row1_2 ) == n_cols ) and ( len( row2_2 ) == n_cols ):
                    type_row = True
                    for i in range( n_cols ):
                        if row1_2[ i ] == row2_2[ i ]:
                            if str( row1_2[ i ] ): lbls[ i ] = str( row1_2[ i ] )
                        elif not row1_2[ i ]:
                            lbls[ i ] = str( row2_2[ i ] )
                        elif not row2_2[ i ]:
                            lbls[ i ] = str( row1_2[ i ] )
                        else:
                            lbls[ i ] = str( row1_2[ i ] ) + ' | ' + str( row2_2[ i ] )
                if not row1_1: row1_1 = [ '' for i in range( n_cols ) ]
                if not row2_1: row2_1 = [ '' for i in range( n_cols ) ]
                if ( len( row1_1 ) == n_cols ) and ( len( row2_1 ) == n_cols ):
                    if type_row: # Treat as units row
                        for i in range( n_cols ):
                            if row1_1[ i ] == row2_1[ i ]:
                                if str( row1_1[ i ] ): lbls[ i ] += ' (' + str( row1_1[ i ] ) + ')'
                            elif not row1_1[ i ]:
                                lbls[ i ] += ' (' + str( row2_1[ i ] ) + ')'
                            elif not row2_1[ i ]:
                                lbls[ i ] += ' (' + str( row1_1[ i ] ) + ')'
                            else:
                                lbls[ i ] += ' (' + str( row1_1[ i ] ) + '|' + str( row2_1[ i ] ) + ')'
                    else: # Treat as type row
                        for i in range( n_cols ):
                            if row1_1[ i ] == row2_1[ i ]:
                                if str( row1_1[ i ] ): lbls[ i ] = str( row1_1[ i ] )
                            elif not row1_1[ i ]:
                                lbls[ i ] = str( row2_1[ i ] )
                            elif not row2_1[ i ]:
                                lbls[ i ] = str( row1_1[ i ] )
                            else:
                                lbls[ i ] = str( row1_1[ i ] ) + ' | ' + str( row2_1[ i ] )
            if in_nums1:
                for i in range( n_cols ):
                    cols1[ i ].append( row1[ i ] )
            if in_nums2:
                for i in range( n_cols ):
                    cols2[ i ].append( row2[ i ] )
        if num1: nums1 = True
        if num2: nums2 = True
        if old_diffs < seq_diffs: lin_diffs += 1

    # Close the files
    file1.close()
    file2.close()

    # Sequential statistics
    if sequential:
        if ( not interp ) and ( f_min is not None ):
            print( ' Metrics:' )
            print( '  Min: ' + str( f_min ) )
            print( '  Max: ' + str( f_max ) )
            if abs( f_min ) > abs( f_max ):
                print( '  Mag: ' + str( f_min ) )
            else:
                print( '  Mag: ' + str( f_max ) )
        if seq_diffs == 0:
            print( ' Pass' )
            passed = True
        else:
            print( ' Fail:  Diffs:  Lines: ' + str( lin_diffs ) + '  Floats: ' + str( flt_diffs ) + '  Ints: ' + str( int_diffs ) + '  Strings: ' + str( str_diffs ) )
            passed = False

    # Check can interp and plot
    if interp_or_plot_or_pyfunnel and ( not ( cols1 and cols2 ) ):
        interp = False
        plotting = plot = plot_fail = False
        pyfunneling = pyfunnel = pyfunnel_fail = False
        interp_or_plot_or_pyfunnel = False

    # Interpolation and plotting and pyfunneling
    if interp_or_plot_or_pyfunnel:
        x1 = numpy.array( cols1[ 0 ] )
        x2 = numpy.array( cols2[ 0 ] )
        x = numpy.unique( numpy.concatenate( ( x1, x2 ) ) )
        row_diffs = 0
        for j in range( 1, n_cols ):
            y1 = numpy.array( cols1[ j ] )
            y2 = numpy.array( cols2[ j ] )
            Y1 = numpy.interp( x, x1, y1 )
            Y2 = numpy.interp( x, x2, y2 )
            Yd = Y1 - Y2

            # Interpolation
            if interp:
                failed = False
                print( ( 'YCol ' + str( j ) + ' ' if n_cols > 2 else '' ) + 'Interpolated:' )

                len_y1 = y1.size
                len_y2 = y2.size
                if coarse and ( len_y1 != len_y2 ): # Compare at steps of coarser signal
                    # Comparison signals
                    if y1.size < y2.size: # Use x1 steps
                        X = x1
                        z1 = y1
                        z2 = numpy.interp( x1, x2, y2 )
                    else: # Use x2 steps
                        X = x2
                        z1 = numpy.interp( x2, x1, y1 )
                        z2 = y2
                    zd = z1 - z2

                    # Tolerance
                    blk_diffs = 0
                    i_max = 0
                    fdiff = abs( zd[ 0 ] )
                    fitol = max( aTol, rTol * max( abs( z1[ 0 ] ), abs( z2[ 0 ] ) ) )
                    r_max = fdiff / fitol if fitol > 0.0 else infinity
                    for i in range( len( X ) ):
                        fdiff = abs( zd[ i ] )
                        fitol = max( aTol, rTol * max( abs( z1[ i ] ), abs( z2[ i ] ) ) )
                        r = fdiff / fitol if fitol > 0.0 else infinity
                        if r > r_max:
                            r_max = r
                            i_max = i
                        if fdiff > fitol: # Exceeds tolerance
                            if verbose: print( ' Row ' + str( i + 1 ) + ':  ' + str( z1[ i ] ) + ' | ' + str( z2[ i ] ) )
                            blk_diffs += 1
                    row_diffs += blk_diffs
                    print( ' Difference:' )
                    print( ' *Tol: ' + str( r_max ) + ' @ ' + str( X[ i_max ] ) )

                    # Statistics
                    i_min = zd.argmin()
                    i_max = zd.argmax()
                    m_min = isinstance( i_min, numpy.ndarray )
                    m_max = isinstance( i_max, numpy.ndarray )
                    if m_min: i_min = i_min[ 0 ]
                    if m_max: i_max = i_max[ 0 ]
                    yd_min = zd[ i_min ]
                    yd_max = zd[ i_max ]
                    print( '  Min: ' + str( yd_min ) + ' @ ' + str( X[ i_min ] ) + ( ' ...' if m_min else '' ) )
                    print( '  Max: ' + str( yd_max ) + ' @ ' + str( X[ i_max ] ) + ( ' ...' if m_max else '' ) )
                    yd_min = abs( yd_min )
                    yd_max = abs( yd_max )
                    if yd_min > yd_max:
                        print( '  Mag: ' + str( yd_min ) + ' @ ' + str( X[ i_min ] ) + ( ' ...' if m_min else '' ) )
                    elif yd_min < yd_max:
                        print( '  Mag: ' + str( yd_max ) + ' @ ' + str( X[ i_max ] ) + ( ' ...' if m_max else '' ) )
                    else:
                        print( '  Mag: ' + str( yd_min ) + ' @ ' + str( X[ min( i_min, i_max ) ] ) + ( ' ...' if m_min or m_max else '' ) )
                    x_range = X[ -1 ] - X[ 0 ]
                    if x_range != 0.0:
                        yda = numpy.abs( zd )
                        yda_avg = numpy.trapz( yda, X ) / x_range
                        yd2 = numpy.square( yda )
                        yd2_avg = math.sqrt( numpy.trapz( yd2, X ) / x_range )
                        print( ' |Avg| (L1): ' + str( yda_avg ) )
                        print( '  RMS  (L2): ' + str( yd2_avg ) )
                    if row_diffs == 0:
                        print( ' Pass' )
                        passed = True
                    else:
                        print( ' Fail:  Diffs:  Rows: ' + str( row_diffs ) )
                        passed = False
                        failed = True
                else: # Use full cross-interpolated signals
                    # Tolerance
                    blk_diffs = 0
                    i_max = 0
                    fdiff = abs( Yd[ 0 ] )
                    fitol = max( aTol, rTol * max( abs( Y1[ 0 ] ), abs( Y2[ 0 ] ) ) )
                    r_max = fdiff / fitol if fitol > 0.0 else infinity
                    for i in range( len( x ) ):
                        fdiff = abs( Yd[ i ] )
                        fitol = max( aTol, rTol * max( abs( Y1[ i ] ), abs( Y2[ i ] ) ) )
                        r = fdiff / fitol if fitol > 0.0 else infinity
                        if r > r_max:
                            r_max = r
                            i_max = i
                        if fdiff > fitol: # Exceeds tolerance
                            if verbose: print( ' Row ' + str( i + 1 ) + ':  ' + str( Y1[ i ] ) + ' | ' + str( Y2[ i ] ) )
                            blk_diffs += 1
                    row_diffs += blk_diffs
                    print( ' Difference:' )
                    print( ' *Tol: ' + str( r_max ) + ' @ ' + str( x[ i_max ] ) )

                    # Statistics
                    i_min = Yd.argmin()
                    i_max = Yd.argmax()
                    m_min = isinstance( i_min, numpy.ndarray )
                    m_max = isinstance( i_max, numpy.ndarray )
                    if m_min: i_min = i_min[ 0 ]
                    if m_max: i_max = i_max[ 0 ]
                    yd_min = Yd[ i_min ]
                    yd_max = Yd[ i_max ]
                    print( ' Metrics:' )
                    print( '  Min: ' + str( yd_min ) + ' @ ' + str( x[ i_min ] ) + ( ' ...' if m_min else '' ) )
                    print( '  Max: ' + str( yd_max ) + ' @ ' + str( x[ i_max ] ) + ( ' ...' if m_max else '' ) )
                    yd_min = abs( yd_min )
                    yd_max = abs( yd_max )
                    if yd_min > yd_max:
                        print( '  Mag: ' + str( yd_min ) + ' @ ' + str( x[ i_min ] ) + ( ' ...' if m_min else '' ) )
                    elif yd_min < yd_max:
                        print( '  Mag: ' + str( yd_max ) + ' @ ' + str( x[ i_max ] ) + ( ' ...' if m_max else '' ) )
                    else:
                        print( '  Mag: ' + str( yd_min ) + ' @ ' + str( x[ min( i_min, i_max ) ] ) + ( ' ...' if m_min or m_max else '' ) )
                    x_range = x[ -1 ] - x[ 0 ]
                    if x_range != 0.0:
                        yda = numpy.abs( Yd )
                        yda_avg = numpy.trapz( yda, x ) / x_range
                        yd2 = numpy.square( yda )
                        yd2_avg = math.sqrt( numpy.trapz( yd2, x ) / x_range )
                        print( ' |Avg| (L1): ' + str( yda_avg ) )
                        print( '  RMS  (L2): ' + str( yd2_avg ) )
                    if row_diffs == 0:
                        print( ' Pass' )
                        passed = True
                    else:
                        print( ' Fail:  Diffs:  Rows: ' + str( row_diffs ) )
                        passed = False
                        failed = True

            # Plotting
            if plot or ( plot_fail and failed ):
                # Plot title
                title = ''
                if model1 == model2: title = model1
                if vnam1 == vnam2: title += ( '  ' if title else '' ) + vnam1
                if n_cols > 2: title += ( '  ' if title else '' ) + 'YCol ' + str( j )
                len_title = len( title )
                if len_title <= 50:
                    title_font_size = 9
                elif len_title <= 70:
                    title_font_size = 8
                elif len_title <= 90:
                    title_font_size = 7
                else:
                    title_font_size = 6

                # Legend labels
                leg1 = leg2 = ''
                if model1 != model2:
                    leg1 = model1
                    leg2 = model2
                if tool1 != tool2:
                    leg1 += ( '  ' if leg1 else '' ) + tool1
                    leg2 += ( '  ' if leg2 else '' ) + tool2
                if vnam1 != vnam2:
                    leg1 += ( '  ' if leg1 else '' ) + vnam1
                    leg2 += ( '  ' if leg2 else '' ) + vnam2
                if not leg1: leg1 = 'File 1'
                if not leg2: leg2 = 'File 2'

                # Figure and axes
                fig, ( top, bot ) = pyplot.subplots( 2, sharex = True, gridspec_kw = { 'height_ratios': [3,1] }, figsize = ( 6, 6.5 ) )
                len_mnam = max( len( mnam1 ), len( mnam2 ) )
                if len_mnam <= 100:
                    mnam_font_size = 7
                elif len_mnam <= 140:
                    mnam_font_size = 6
                elif len_mnam <= 150:
                    mnam_font_size = 5
                else:
                    mnam_font_size = 4
                pyplot.suptitle( mnam1 + '\n' + mnam2, horizontalalignment = 'left', x = 0.01, y = 0.99, fontsize = mnam_font_size )

                # Overlay plot
                top.set_title( title + ( '  ' if title else '' ) + 'Overlay', fontsize = title_font_size )
                top.plot( x1, y1, label = leg1, linewidth = 0.6, color = 'darkgreen', zorder = 2.1 ) # zorder > 2 to put on top of File 2 curve
                top.plot( x2, y2, label = leg2, linewidth = 0.6, color = 'darkblue' )
                top.grid( linestyle = 'dotted', alpha = 0.25 )
                top.tick_params( axis = 'both', direction = 'in' )
                top.ticklabel_format( style = 'sci', scilimits = ( -4, 5 ), axis = 'both' )
                top.xaxis.get_offset_text().set_size( 6 )
                top.yaxis.get_offset_text().set_size( 6 )
                for tick in top.xaxis.get_major_ticks():
                    tick.label1.set_fontsize( 7 )
                for tick in top.yaxis.get_major_ticks():
                    tick.label1.set_fontsize( 7 )
                len_leg = max( len( leg1 ), len( leg2 ) )
                if len_leg <= 80:
                    leg_font_size = 7
                elif len_leg <= 120:
                    leg_font_size = 6
                elif len_leg <= 130:
                    leg_font_size = 5
                else:
                    leg_font_size = 4
                leg = top.legend( loc = 'best', fontsize = leg_font_size )
                #leg.get_frame().set_alpha( 1.0 ) # Make legend opaque (default is semi-transparent)

                # Diff plot
                bot.set_title( title + ( '  ' if title else '' ) + 'Diff', fontsize = title_font_size )
                bot.plot( x, Yd, linewidth = 0.8, color = 'darkred' )
                bot.grid( linestyle = 'dotted', alpha = 0.25 )
                bot.tick_params( axis = 'both', direction = 'in' )
                bot.ticklabel_format( style = 'sci', scilimits = ( -4, 5 ), axis = 'both' )
                bot.xaxis.get_offset_text().set_size( 6 )
                bot.yaxis.get_offset_text().set_size( 6 )
                for tick in bot.xaxis.get_major_ticks():
                    tick.label1.set_fontsize( 7 )
                for tick in bot.yaxis.get_major_ticks():
                    tick.label1.set_fontsize( 7 )

                # Labels
                if lbls:
                    if lbls[ 0 ]: bot.set_xlabel( lbls[ 0 ], fontsize = 8 * min( 35.0 / len( lbls[ 0 ] ), 1.0 ) )
                    if lbls[ j ]:
                        scl = min( 30.0 / len( lbls[ j ] ), 1.0 )
                        top.set_ylabel( lbls[ j ], fontsize = 8 * scl )
                        bot.set_ylabel( lbls[ j ], fontsize = 8 * scl )

                # Generate plot
                pyplot.tight_layout() # Prevents overlaps
                pyplot.subplots_adjust( top = 0.9 ) # Leave space for file names
                if out:
                    pnam = onam + ( '.YCol' + str( j ) if n_cols > 2 else '' ) + '.png' # '.pdf' '.png' '.jpg' #Do Make type an option
                    # pnam = os.path.abspath( pnam )
                    fig.set_size_inches( 8.5, 11 ) #Do Make this an option with default based on file type: 8.5x11 for pdf, ...
                    pyplot.savefig( pnam ) # pdf, png, jpg
                    if out:
                        sys.stderr.write( 'Plot saved to: ' + pnam + '\n' )
                    else:
                        print( 'Plot saved to: ' + pnam )
                    fig.set_size_inches( 6, 6.5 ) # Restore viewing size
                else:
                    pyplot.show()
                pyplot.close()

            # Pyfunneling
            if pyfunnel_it or ( pyfunnel_fail and failed ):
                pyfunnel.compareAndReport(
                 xReference = x,
                 yReference = Y1,
                 xTest = x,
                 yTest = Y2,
                 outputDirectory = 'pyfunnel_results',
                 atolx = args.aTolx,
                 atoly = ( args.aTol if args.aTol > 0.0 else 1e-10 ), # Prevent defaulting to 0.1 when 0 passed
                 ltolx = args.rTolx,
                 ltoly = args.rTol,
                )
                pyfunnel.plot_funnel( 'pyfunnel_results' )

    # Reset stdout
    if out:
        sys.stdout = sys.__stdout__
        print( 'Report written to: ' + onam + '.rpt' )

    # Return info
    return passed, onam

if __name__ == '__main__':
    sim_diff()
