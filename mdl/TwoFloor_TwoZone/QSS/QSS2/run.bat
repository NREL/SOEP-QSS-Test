@echo off
QSS ..\..\OCT\TwoFloor_TwoZone.fmu --qss=QSS2 --dtNum=1e-4 --zFac=10 --dtOut=100 --out=trFkxo --var=..\..\TwoFloor_TwoZone.var >run.log 2>&1
