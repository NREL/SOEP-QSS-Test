@echo off
QSS ..\..\OCT\sinusoid.fmu --qss=QSS3 --dtND=1e-4 --aFac=0.01 --out=RZDXQ %* >run.log 2>&1
