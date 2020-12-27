@echo off
QSS ..\..\OCT\TwoFloor_TwoZone.fmu --qss=QSS2 --dtND=1e-4 --zFac=10 --dtOut=.001 --tEnd=.1 --out=RZDXO --var=..\..\TwoFloor_TwoZone.var >run.log 2>&1
