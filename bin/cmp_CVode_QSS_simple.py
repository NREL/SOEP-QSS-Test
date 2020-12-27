#!/usr/bin/env python
import os, subprocess, sys

# Find and change to mdl directory
mdl_dir = os.getcwd()
while os.path.basename( mdl_dir ) != 'mdl': # Move up one directory level
    mdl_dir = os.path.dirname( mdl_dir )
    if os.path.splitdrive( mdl_dir )[1] == os.sep: # At top of drive/mount
        print( 'Error: Not under a "mdl" directory' )
        sys.exit( 1 )
os.chdir( mdl_dir )

# Run simple model comparisons
with open( 'cmp_CVode_QSS_simple.log', 'w', newline = '\n' ) as log:
    print( 'Achilles' ); subprocess.run( 'cd Achilles && cmp_PyFMI_QSS.py --qss:rTol=2e-6 --cmp=x1=1e-6 --cmp=x2=1e-6', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'BouncingBall' ); subprocess.run( 'cd BouncingBall && cmp_PyFMI_QSS.py --dtND=1e-5 --zTol=1e-6 --dtInf=0.1 --dtMax=0.1 --cmp=h=3e-6', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'CoupledSystem' ); subprocess.run( 'cd CoupledSystem && cmp_PyFMI_QSS.py --qss:rTol=1e-7 --cmp=x1=1e-7', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'InputFunction' ); subprocess.run( 'cd InputFunction && cmp_PyFMI_QSS.py --inp=step --fxn=u:step[1,1,1] --cmp=x=2e-3', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'IntegratorWithLimiter' ); subprocess.run( 'cd IntegratorWithLimiter && cmp_PyFMI_QSS.py --cmp=x=1e-6', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'Observers' ); subprocess.run( 'cd Observers && cmp_PyFMI_QSS.py --qss:rTol=1e-5 --cmp=x001=1e-3', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'PID_Controller' ); subprocess.run( 'cd PID_Controller && cmp_PyFMI_QSS.py --qss:rTol=2e-6 --dtND=7e-3 --cmp=torque.tau=2e-4', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'Quadratic' ); subprocess.run( 'cd Quadratic && cmp_PyFMI_QSS.py --cmp=x=1e-6', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'sinusoid' ); subprocess.run( 'cd sinusoid && cmp_PyFMI_QSS.py --cmp=x1=1e-7 --cmp=x2=1e-4', stdout = log, stderr = subprocess.STDOUT, shell = True )
