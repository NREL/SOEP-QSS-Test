@echo off
QSS ..\..\OCT\ASHRAE2006.fmu --qss=QSS2 --dtNum=1e-4 --zFac=10 --dtOut=100 --out=sFx --var=..\..\ASHRAE2006.var >run.log 2>&1
