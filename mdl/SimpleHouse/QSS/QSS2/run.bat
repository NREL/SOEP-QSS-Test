@echo off
QSS ..\..\OCT\SimpleHouse.fmu --qss=QSS2 --dtND=5e-4 --zFac=2 --dtOut=3600 --out=sFx --var=..\..\SimpleHouse.var --statistics >run.log 2>&1
