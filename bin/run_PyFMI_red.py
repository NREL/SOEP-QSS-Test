#!/usr/bin/env python
import subprocess, sys

# Set up pass-through QSS arguments
args = ''
red = ''
for arg in sys.argv[1:]:
    if arg.startswith( ( '--red=', '--red:' ) ): # Redirect
        red = arg[6:].strip()
    else: # Pass-through argument
        args += ' ' + arg

# Run PyFMI
try:
    if red: # Redirect
        if red == 'nul': # Discard
            subprocess.run( 'run_PyFMI.py' + args, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, shell = True )
        else: # File
            with open( red, 'w', newline = '\n' ) as log:
                subprocess.run( 'run_PyFMI.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
    else: # Don't redirect
        subprocess.run( 'run_PyFMI.py' + args, shell = True )
except Exception as err:
    print( 'Simulation failed: ', err )
    sys.exit( 1 )
