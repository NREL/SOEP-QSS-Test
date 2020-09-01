@echo off
QSS ..\..\OCT\sinusoid.fmu --qss=QSS3 --dtNum=1e-4 --aFac=0.01 --out=rxq %* >run.log 2>&1
