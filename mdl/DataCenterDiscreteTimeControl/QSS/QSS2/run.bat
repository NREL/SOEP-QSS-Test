@echo off
QSS ..\..\OCT\DataCenterDiscreteTimeControl.fmu --qss=QSS2 --dtNum=1e-4 --zFac=10 --dtOut=100 --out=sFx --var=..\..\DataCenterDiscreteTimeControl.var >run.log 2>&1
