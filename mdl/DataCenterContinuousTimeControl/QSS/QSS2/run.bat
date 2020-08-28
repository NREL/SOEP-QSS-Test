@echo off
QSS ..\..\OCT\DataCenterContinuousTimeControl.fmu --qss=QSS2 --dtNum=1e-4 --zFac=2 --dtOut=60 --out=sFx --statistics --var=..\..\DataCenterContinuousTimeControl.var %* >run.log 2>&1
