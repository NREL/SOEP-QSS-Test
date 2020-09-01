@echo off
QSS ..\..\OCT\Case600.fmu --qss=QSS2 --dtOut=100 --out=sFx %* >run.log 2>&1
