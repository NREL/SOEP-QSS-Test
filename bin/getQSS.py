#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Get and Build latest SOEP-QSS:
# - Requires Python package GitPython (Ubuntu: python3-git)
# - SOEP-QSS build can fail if the scripts called by setQSS need to be adapted for the system

# Imports
import argparse
import os
import platform
import shutil
import subprocess
import sys

# Set/check platform
platform_name = platform.system()
if platform_name not in ( 'Linux', 'Windows' ):
    print( 'Error: Platform not supported:', platform_name )
    sys.exit( 1 )

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument( '--dir', help = 'Target directory  [SOEP-QSS]', default = 'SOEP-QSS' )
parser.add_argument( '--rev', help = 'Revision [latest]', default = None )
parser.add_argument( '--bld', help = 'Build specs  (Compiler[.Build])  [GCC|Clang|VC|IX[.r]]', default = 'GCC.r' )
parser.add_argument( '--no-bld', help = 'Don\'t build  [False]', default = False, action = 'store_true' )
parser.add_argument( '--git', help = 'Git executable directory (if not on PATH)', default = None )
args = parser.parse_args()

# Check git is on PATH then import GitPython
if args.git: # Git directory specified
    os.environ[ 'PATH' ] += os.pathsep + args.git
elif platform_name == 'Windows': # Windows
    if shutil.which( 'git.exe' ) is None: # Look in typical locations
        if os.path.isfile( r'C:\Program files\Git\cmd\git.exe' ):
            os.environ[ 'Path' ] += r';C:\Program files\Git\cmd'
        elif os.path.isfile( r'C:\Git\cmd\git.exe' ):
            os.environ[ 'Path' ] += r';C:\Git\cmd'
    if shutil.which( 'git.exe' ) is None:
        print( 'Error: git not found or on PATH' )
        sys.exit( 1 )
else: # Non-Windows platform
    if shutil.which( 'git' ) is None:
        print( 'Error: git not found on PATH' )
        sys.exit( 1 )
import git

# Get/update SOEP-QSS repo: Not using --force to avoid losing local modifications
if os.path.isdir( args.dir ): # Directory exists
    if os.path.isdir( os.path.join( args.dir, '.git' ) ): # Looks like a git repo
        repo = git.Repo( args.dir )
        git = repo.git
        git_remote = git.remote( '-v' )
        if git_remote.startswith( 'origin\tgit@github.com:NREL/SOEP-QSS.git (fetch)' ): # SOEP-QSS repo
            print( 'Pulling SOEP-QSS into', args.dir )
            git.checkout( 'master' )
            git.pull()
            if args.rev: git.checkout( args.rev ) # Checkout specified revision
        else: # Different repo
            print( 'Error: Target directory contains a different git repository:', git_remote[ 8:git_remote.index( ' (' ) ] )
            sys.exit( 1 )
    elif len( os.listdir( args.dir ) > 0 ): # Non-empty
            print( 'Error: Target directory is non-empty and is not a git repository' )
            sys.exit( 1 )
else: # Directory doesn't exist
    print( 'Cloning SOEP-QSS into', args.dir )
    try:
        repo = git.Repo.clone_from( 'git@github.com:NREL/SOEP-QSS.git', args.dir )
    except:
        repo = git.Repo.clone_from( 'https://github.com:NREL/SOEP-QSS.git', args.dir )
    git = repo.git
    if args.rev: git.checkout( args.rev ) # Checkout specified revision

# Done if build suppressed
if args.no_bld: sys.exit( 0 ) # Don't build

# Build SOEP-QSS
if '.' in args.bld:
    compiler, build = args.bld.split( '.' )
else:
    compiler = args.bld
    build = 'r'
compiler_lower = compiler.lower()
build = build.lower()
if compiler_lower in ( 'gcc', 'g++' ): # GCC
    compiler = 'GCC'
elif compiler_lower in ( 'clang', 'clang++' ): # Clang
    compiler = 'Clang'
elif compiler_lower in ( 'intel', 'icx', 'icpx', 'ix' ): # Intel C++ (LLVM)
    compiler = 'IX'
elif compiler_lower in ( 'msvc', 'msvs', 'vc', 'vc++' ): # Microsoft Visual C++
    if platform_name == 'Linux':
        print( 'Error: Visual C++ is not supported on Linux' )
        sys.exit( 1 )
    compiler = 'VC'
else:
    print( 'Error: Compiler not supported:', compiler )
    sys.exit( 1 )
if build not in ( 'r', 'd' ):
    print( 'Error: Build type not supported:', build )
    sys.exit( 1 )
print( 'Building SOEP-QSS in', args.dir )
try:
    if platform_name == 'Linux':
        print( subprocess.check_output( '. bin/Linux/' + compiler + '/' + build + '/setQSS && bin/Linux/bld', executable = '/bin/bash', shell = True, encoding = 'UTF-8', cwd = args.dir ) )
    elif platform_name == 'Windows':
        print( subprocess.check_output( [ 'bin\\Windows\\' + compiler + '\\' + build + '\\setQSS.bat', '&&', 'bin\\Windows\\bld.bat' ], shell = True, encoding = 'UTF-8', cwd = args.dir ) )
except subprocess.CalledProcessError as err:
        print( 'SOEP-QSS build error:', err.output )
