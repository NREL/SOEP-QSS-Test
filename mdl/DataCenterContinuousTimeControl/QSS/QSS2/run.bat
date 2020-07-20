@echo off
QSS ..\..\OCT\DataCenterContinuousTimeControl.fmu --qss=QSS2 --dtNum=1e-4 --zFac=10 --dtOut=100 --out=sFx --var=..\..\DataCenterContinuousTimeControl.var >run.log 2>&1
