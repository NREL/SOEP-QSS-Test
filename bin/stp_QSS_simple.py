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

# Run simple model step count checks
with open( 'stp_QSS_simple.log', 'w', newline = '\n' ) as log:
    print( 'Achilles' )
    subprocess.run( 'cd Achilles && stp_QSS.py --stp=x1=156 --stp=x2=160', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'BouncingBall' )
    subprocess.run( 'cd BouncingBall && stp_QSS.py --dtND=1e-5 --zTol=1e-6 --dtInf=0.1 --dtMax=0.1 --stp=h=32', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'CoupledSystem' )
    subprocess.run( 'cd CoupledSystem && stp_QSS.py --stp=x1=1 --stp=x2=1 --stp=x3=4', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'InputFunction' )
    subprocess.run( 'cd InputFunction && stp_QSS.py --fxn=u:step[1,1,1] --stp=u=0 --stp=x=9', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'IntegratorWithLimiter' )
    subprocess.run( 'cd IntegratorWithLimiter && stp_QSS.py --stp=x=0 --stp=y=0', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'Observers' )
    subprocess.run( 'cd Observers && stp_QSS.py --stp=x001=36', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'PID_Controller' )
    subprocess.run( 'cd PID_Controller && stp_QSS.py --dtND=7e-3 --stp=spring.w_rel=888 --stp=inertia1.phi=43 --stp=integrator.y=0', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'Quadratic' )
    subprocess.run( 'cd Quadratic && stp_QSS.py --stp=x=0', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'sinusoid' )
    subprocess.run( 'cd sinusoid && stp_QSS.py --stp=x1=10 --stp=x2=964', stdout = log, stderr = subprocess.STDOUT, shell = True )
