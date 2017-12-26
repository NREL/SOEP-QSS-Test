#!/usr/bin/env python

# Simulation Results Comparison Tool
#
# Project: QSS Solver
#
# Language: Python 2.7 and 3.x
#
# Developed by Objexx Engineering, Inc. (http://objexx.com) under contract to
# the National Renewable Energy Laboratory of the U.S. Department of Energy
#
# Copyright (c) 2017 Objexx Engineerinc, Inc. All rights reserved.
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
#   The logic attempts to match up files to compare in a non-surprising way
#   For more complex scenarios use a wrapper script to feed two files at a time to this script
#  Intended for comparison of simulation results containing a mix of text and numeric values
#  Tokens can be whitespace or comma separated
#  Numeric data columns quantities are assumed to be the same in both files
#  Interpolated and plotted results assume col 1 is the x-axis for the other columns

# Python imports
import argparse, fastnumbers, glob, math, os, re, sys
from types import NoneType

# Globals
args = None

def main():
    '''main'''

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument( 'inp1', help = 'input 1' )
    parser.add_argument( 'inp2', help = 'input 2' )
    parser.add_argument( '--rTol', help = 'relative tolerance  [0.001]', type = float, default = 0.001 )
    parser.add_argument( '--aTol', help = 'absolute tolerance  [0]', type = float, default = 0.0 )
    parser.add_argument( '--no-sync', help = "don't sync numeric block  [F]", dest = 'sync', action = 'store_false' )
    parser.add_argument( '--no-interp', help = "don't interpolate (interp=> sync)  [F]", dest = 'interp', action = 'store_false' )
    parser.add_argument( '--plot', help = 'plot curves/diff  [F]', action = 'store_true' )
    parser.add_argument( '--dpi', help = 'screen dpi', type = int, default = 0 )
    parser.add_argument( '--out', help = 'output to file(s)  [F]', action = 'store_true' )
    parser.add_argument( '-v', '--verbose', help = 'verbose report  [F]', action = 'store_true' )
    parser.set_defaults( sync = True, interp = True )
    global args
    args = parser.parse_args()
    if args.interp: args.sync = True # Interpolation => Sync

    # Generate input lists
    glob1 = glob.glob( args.inp1 )
    glob2 = glob.glob( args.inp2 )
    if not glob1:
        print( '\nNo paths found matching inp1: ' + args.inp1 )
        sys.exit( 1 )
    if not glob2:
        print( '\nNo paths found matching inp2: ' + args.inp2 )
        sys.exit( 1 )
    for i in range( len( glob1 ) ): glob1[ i ] = os.path.abspath( glob1[ i ] )
    for i in range( len( glob2 ) ): glob2[ i ] = os.path.abspath( glob2[ i ] )

    # Process single item inputs
    if ( len( glob1 ) == 1 ) and ( len( glob2 ) == 1 ): # Both single items: Handle specially to allow unrelated file names
        path1 = glob1[ 0 ]
        path2 = glob2[ 0 ]
        if os.path.isfile( path1 ) and os.path.isfile( path2 ):
            if path1 != path2:
                sim_compare( path1, path2 )
                glob1 = glob2 = [] # So don't keep checking

    # Process multiple item inputs
    next1 = []
    for path1 in glob1:
        if os.path.isfile( path1 ):
            done1 = False
            base1 = os.path.basename( path1 )
            root1 = os.path.splitext( base1 )[ 0 ]
            for path2 in glob2:
                if os.path.isfile( path2 ):
                    if path2 != path1:
                        base2 = os.path.basename( path2 )
                        root2 = os.path.splitext( base2 )[ 0 ]
                        if ( base2 == base1 ) or ( root2 == root1 ): # Base or root names match
                            sim_compare( path1, path2 )
                            done1 = True
                            break # Stop checking glob2
                elif os.path.isdir( path2 ):
                    file2 = os.path.join( path2, base1 )
                    if os.path.isfile( file2 ):
                        if file2 != path1:
                            sim_compare( path1, file2 )
                            done1 = True
                            break # Stop checking glob2
            if not done1: next1.append( path1 )

    for path2 in glob2:
        if os.path.isfile( path2 ):
            base2 = os.path.basename( path2 )
            root2 = os.path.splitext( base2 )[ 0 ]
            for path1 in next1:
                if os.path.isfile( path1 ):
                    if path1 != path2:
                        base1 = os.path.basename( path1 )
                        root1 = os.path.splitext( base1 )[ 0 ]
                        if ( base1 == base2 ) or ( root1 == root2 ): # Base or root names match
                            sim_compare( path2, path1 )
                            break # Stop checking next1
                elif os.path.isdir( path1 ):
                    file1 = os.path.join( path1, base2 )
                    if os.path.isfile( file1 ):
                        if file2 != path1:
                            sim_compare( path2, file1 )
                            break # Stop checking next1

def sim_compare( fnam1, fnam2 ):
    '''Compare simulation output files'''

    # Check/report files
    if ( os.path.getsize( fnam1 ) == 0 ) or ( os.path.getsize( fnam2 ) == 0 ):
        print( '\nSkipping empty file(s):\n' + fnam1 + '\n' + fnam2 )
        return

    # Open the files
    try:
        file1 = open( fnam1, 'rU' )
    except:
        print( '\nOpen failed: ' + fnam1 )
        return
    try:
        file2 = open( fnam2, 'rU' )
    except:
        print( '\nOpen failed: ' + fnam2 )
        return

    # Conditional imports
    if args.interp or args.plot:
        try:
            import numpy
        except:
            if args.interp:
                print( 'Interpolation diffs unavailable: NumPy is not installed' )
                args.interp = False
            if args.plot:
                print( 'Plotting unavailable: NumPy is not installed' )
                args.plot = False
    if args.plot:
        try:
            from matplotlib import pyplot
            pyplot.rcParams[ 'axes.formatter.offset_threshold' ] = 3
            if args.dpi > 0:
                pyplot.rcParams[ 'figure.dpi' ] = args.dpi
            elif sys.platform.startswith( 'linux' ): # Scale up to typically usable size
                pyplot.rcParams[ 'figure.dpi' ] = 150
        except:
            print( 'Plotting unavailable: matplotlib is not installed' )
            args.plot = False

    # Argument aliases
    rTol = args.rTol
    aTol = args.aTol
    sync = args.sync
    interp = args.interp
    plot = args.plot
    interp_or_plot = interp or plot
    out = args.out
    verbose = args.verbose

    # Compare the files
    lnum1 = lnum2 = 0 # Line numbers in files
    line1 = line2 = True # Not at end of files?
    nums1 = nums2 = False # Found numeric lines?
    in_nums1 = in_nums2 = False # In numeric blocks?
    wait1 = wait2 = False # File waiting for other file to reach numeric lines?
    end1 = end2 = False # Reached end of files prev?
    row1_1 = row1_2 = row2_1 = row2_2 = None # 2 previous rows
    lin_diffs = 0
    num_diffs = 0
    int_diffs = 0
    flt_diffs = 0
    str_diffs = 0
    f_min = f_max = None # min/max floating point differences in line scan
    if interp_or_plot:
        row1_2 = []
        row2_2 = []
        row1_1 = []
        row2_1 = []
        row1 = []
        row2 = []
        cols1 = cols2 = None
        lbls = None
    print( '' )
    if out:
        onam = os.path.splitext( os.path.basename( fnam1 ) )[ 0 ] + '-' + os.path.splitext( os.path.basename( fnam1 ) )[ 0 ]
        try:
            sys.stdout = open( onam + '.rpt', 'w' )
        except:
            print( 'Report open failed' )
            pass
    print( 'Comparing:\n' + fnam1 + '\n' + fnam2 )
    print( 'Sequential:' )
    while line1 or line2:
        if sync:
            wait1 = ( nums1 and ( not nums2 ) ) or ( interp and nums1 and ( not in_nums1 ) and in_nums2 )
            wait2 = ( nums2 and ( not nums1 ) ) or ( interp and nums2 and ( not in_nums2 ) and in_nums1 )
        if sync: # Read next lines unless waiting for other file to reach numeric lines
            if line1 and ( not wait1 ):
                line1 = file1.readline()
            elif wait1 and ( not end1 ):
                line1 = '\n'
            if line2 and ( not wait2 ):
                line2 = file2.readline()
            elif wait2 and ( not end2 ):
                line2 = '\n'
        else: # Read next lines unless end of file already reached
            if line1: line1 = file1.readline()
            if line2: line2 = file2.readline()
        old_diffs = num_diffs
        if ( not line1 ) and ( not line2 ): # Simultaneously reached end of both files
            break
        elif not line1: # Reached end of file1 first
            if verbose and ( not end1 ) and ( not interp ): print( ' File 1: End hit first' )
            num_diffs += 1
            end1 = True
        elif not line2: # Reached end of file2 first
            if verbose and ( not end2 ) and ( not interp ): print( ' File 2: End hit first' )
            num_diffs += 1
            end2 = True
            line2 = ''
        num1 = num2 = True # Lines are all numeric tokens?
        if not wait1: lnum1 += 1
        if not wait2: lnum2 += 1
        tokens1 = re.split( r'[\s,]+', line1 ) if line1 else []
        tokens2 = re.split( r'[\s,]+', line2 ) if line2 else []
        while tokens1 and tokens1[ -1 ] == '': del tokens1[ -1 ]
        while tokens2 and tokens2[ -1 ] == '': del tokens2[ -1 ]
        if len( tokens1 ) != len( tokens2 ):
            if line1 and line2 and ( not ( sync and ( wait1 or wait2 ) ) ):
                if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ': Different number of tokens' )
                num_diffs += 1
        if interp_or_plot:
            row1_2 = row1_1
            row2_2 = row2_1
            row1_1 = row1 if not wait1 else []
            row2_1 = row2 if not wait2 else []
            row1 = []
            row2 = []
        l1 = len( tokens1 )
        l2 = len( tokens2 )
        for i in range( max( l1, l2 ) ):
            token1 = tokens1[ i ] if i < l1 else None
            token2 = tokens2[ i ] if i < l2 else None
            val1 = fastnumbers.fast_real( token1 ) if token1 else None
            val2 = fastnumbers.fast_real( token2 ) if token2 else None
            if ( val1 is None ) or isinstance( val1, str ): num1 = False
            if ( val2 is None ) or isinstance( val2, str ): num2 = False
            if ( not ( interp and in_nums1 and in_nums2 ) ) and ( val1 != val2 ):
                if isinstance( val1, int ) and isinstance( val2, int ): # Compare as integers
                    if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + token1 + ' | ' + token2 )
                    num_diffs += 1
                    int_diffs += 1
                elif ( not isinstance( val1, ( str, NoneType ) ) ) and ( not isinstance( val2, ( str, NoneType ) ) ): # Compare as floats
                    fdiff = abs( val1 - val2 )
                    if f_min is None:
                        f_min = f_max = fdiff
                    elif fdiff < f_min:
                        f_min = fdiff
                    elif fdiff > f_max:
                        f_max = fdiff
                    if fdiff <= aTol: # Within abs tolerance
                        pass
                    elif fdiff <= rTol * max( abs( val1 ), abs( val2 ) ): # Within rel tolerance
                        pass
                    else:
                        if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + token1 + ' | ' + token2 )
                        num_diffs += 1
                        flt_diffs += 1
                else: # Compare tokens as strings
                    if token1 != token2:
                        if verbose: print( ' Line ' + str( lnum1 ) + '|' + str( lnum2 ) + ':  Token: ' + str( i + 1 ) + ':  ' + str( token1 ) + ' | ' + str( token2 ) )
                        num_diffs += 1
                        str_diffs += 1
            if interp_or_plot:
                if val1 is not None: row1.append( val1 )
                if val2 is not None: row2.append( val2 )
        if interp_or_plot:
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
                            lbls[ i ] = str( row1_2[ i ] )
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
                                lbls[ i ] += ' (' + str( row1_1[ i ] ) + ')'
                            elif not row1_1[ i ]:
                                lbls[ i ] += ' (' + str( row2_1[ i ] ) + ')'
                            elif not row2_1[ i ]:
                                lbls[ i ] += ' (' + str( row1_1[ i ] ) + ')'
                            else:
                                lbls[ i ] += ' (' + str( row1_1[ i ] ) + '|' + str( row2_1[ i ] ) + ')'
                    else: # Treat as type row
                        for i in range( n_cols ):
                            if row1_1[ i ] == row2_1[ i ]:
                                lbls[ i ] = str( row1_1[ i ] )
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
        if old_diffs < num_diffs: lin_diffs += 1

    # Close the files
    file1.close()
    file2.close()

    # Statistics
    print( ' Diffs:  Lines: ' + str( lin_diffs ) + '  Floats: ' + str( flt_diffs ) + '  Ints: ' + str( int_diffs ) + '  Strings: ' + str( str_diffs ) )
    if ( not interp ) and ( f_min is not None ):
        print( ' Metrics:' )
        print( '  Min: ' + str( f_min ) )
        print( '  Max: ' + str( f_max ) )
        if abs( f_min ) > abs( f_max ):
            print( '  Mag: ' + str( f_min ) )
        else:
            print( '  Mag: ' + str( f_max ) )

    # Check can interp and plot
    if interp_or_plot and ( not ( cols1 and cols2 ) ):
        interp = False
        plot = False

    # Reset stdout
    if out:
        sys.stdout = sys.__stdout__
        print( 'Report written to: ' + onam + '.rpt' )

    # Interpolation and plotting
    if interp or plot:
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
                print( ( 'YCol ' + str( j ) + ' ' if n_cols > 2 else '' ) + 'Interpolated:' )

                # Tolerance
                blk_diffs = 0
                for i in range( len( x ) ):
                    fdiff = abs( Yd[ i ] )
                    if fdiff <= aTol: # Within abs tolerance
                        pass
                    elif fdiff <= rTol * max( abs( Y1[ i ] ), abs( Y2[ i ] ) ): # Within rel tolerance
                        pass
                    else:
                        if verbose: print( ' Row ' + str( i + 1 ) + ':  ' + str( Y1[ i ] ) + ' | ' + str( Y2[ i ] ) )
                        blk_diffs += 1
                row_diffs += blk_diffs

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
                else:
                    print( ' Fail:  Diffs:  Rows: ' + str( row_diffs ) )

            # Plotting
            if plot:
                # Figure and axes
                fig, ( top, bot ) = pyplot.subplots( 2, sharex = True, gridspec_kw = { 'height_ratios': [3,2] }, figsize = ( 6, 6.5 ) )

                # Overlay plot
                top.set_title( ( 'YCol ' + str( j ) + ' ' if n_cols > 2 else '' ) + 'Overlay', fontsize = 9 )
                top.plot( x1, y1, label = 'File 1', linewidth = 0.5, color = 'darkgreen', zorder = 2.1 ) # zorder > 2 to put on top of File 2 curve
                top.plot( x2, y2, label = 'File 2', linewidth = 0.5, color = 'darkred' )
                top.grid( linestyle = 'dotted', alpha = 0.25 )
                top.tick_params( axis = 'both', direction = 'in' )
                top.ticklabel_format( style = 'sci', scilimits = ( -4, 5 ), axis = 'both' )
                top.xaxis.get_offset_text().set_size( 6 )
                top.yaxis.get_offset_text().set_size( 6 )
                for tick in top.xaxis.get_major_ticks():
                    tick.label.set_fontsize( 7 )
                for tick in top.yaxis.get_major_ticks():
                    tick.label.set_fontsize( 7 )
                leg = top.legend( loc = 'best', fontsize = 8 )
                leg.get_frame().set_alpha( 1.0 ) # Make legend opaque (default is semi-transparent)

                # Diff plot
                bot.set_title( ( 'YCol ' + str( j ) + ' ' if n_cols > 2 else '' ) + 'Diff', fontsize = 9 )
                bot.plot( x, Yd, linewidth = 0.8 )
                bot.grid( linestyle = 'dotted', alpha = 0.25 )
                bot.tick_params( axis = 'both', direction = 'in' )
                bot.ticklabel_format( style = 'sci', scilimits = ( -4, 5 ), axis = 'both' )
                bot.xaxis.get_offset_text().set_size( 6 )
                bot.yaxis.get_offset_text().set_size( 6 )
                for tick in bot.xaxis.get_major_ticks():
                    tick.label.set_fontsize( 7 )
                for tick in bot.yaxis.get_major_ticks():
                    tick.label.set_fontsize( 7 )

                # Labels
                if lbls:
                    if lbls[ 0 ]: bot.set_xlabel( lbls[ 0 ], fontsize = 8 * min( 35.0 / len( lbls[ 0 ] ), 1.0 ) )
                    if lbls[ j ]:
                        scl = min( 30.0 / len( lbls[ j ] ), 1.0 )
                        top.set_ylabel( lbls[ j ], fontsize = 8 * scl )
                        bot.set_ylabel( lbls[ j ], fontsize = 8 * scl )

                # Generate plot
                pyplot.tight_layout() # Prevents overlaps
                if out:
                    pnam = os.path.abspath( onam + ( '.YCol' + str( j ) if n_cols > 2 else '' ) + '.pdf' )
                    fig.set_size_inches( 8.5, 11 )
                    pyplot.savefig( pnam ) # pdf, png, jpg
                    print( 'Plot saved to: ' + pnam )
                    fig.set_size_inches( 6, 6.5 ) # Restore viewing size
                else:
                    pyplot.show()
                pyplot.close()

    # Report file summary
    print( 'Summary:' )
    if interp:
        if ( num_diffs == 0 ) and ( row_diffs == 0 ):
            print( ' Pass' )
        else:
            print( ' Fail:  Diffs:  Lines: ' + str( lin_diffs ) + '  Floats: ' + str( flt_diffs ) + '  Ints: ' + str( int_diffs ) + '  Strings: ' + str( str_diffs ) + '  Rows: ' + str( row_diffs ) )
    else:
        if num_diffs == 0:
            print( ' Pass' )
        else:
            print( ' Fail:  Diffs:  Lines: ' + str( lin_diffs ) + '  Floats: ' + str( flt_diffs ) + '  Ints: ' + str( int_diffs ) + '  Strings: ' + str( str_diffs ) )

if __name__ == '__main__':
    main()
