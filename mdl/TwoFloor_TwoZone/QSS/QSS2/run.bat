@echo off
QSS ..\..\OCT\TwoFloor_TwoZone.fmu --qss=QSS2 --dtND=1e-2 --dtOut=100 --out=trFkxo --var=..\..\TwoFloor_TwoZone.var %* >run.log 2>&1
