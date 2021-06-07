#!/usr/bin/env python
import subprocess, sys
args = '  ../../../Achilles1/QSS/FMU-QSS2/Achilles1_QSS.fmu ../../../Achilles2/QSS/FMU-QSS2/Achilles2_QSS.fmu --con=Achilles2.x1:Achilles1.x1 --con=Achilles1.x2:Achilles2.x2 --dtInf=0.001 --perfect --out=ROZDXK ' + ' '.join( sys.argv[1:] )
with open( 'run.log', 'w' ) as log:
    subprocess.run( 'run_QSS.py' + args, stdout = log, stderr = subprocess.STDOUT, shell = True )
