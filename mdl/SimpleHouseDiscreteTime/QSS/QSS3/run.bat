@echo off
QSS ..\..\OCT\SimpleHouseDiscreteTime.fmu --qss=QSS3 --dtOut=120 --out=sFx --var=..\..\SimpleHouseDiscreteTime.var --statistics --dtNum=1e-3 %* >run.log 2>&1
