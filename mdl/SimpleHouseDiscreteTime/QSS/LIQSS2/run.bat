@echo off
QSS ..\..\OCT\SimpleHouseDiscreteTime.fmu --qss=LIQSS2 --dtOut=120 --out=sFx --var=..\..\SimpleHouseDiscreteTime.var --statistics --dtND=1e-3 %* >run.log 2>&1
