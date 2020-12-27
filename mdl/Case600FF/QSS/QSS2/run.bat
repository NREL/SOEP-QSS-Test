@echo off
QSS ..\..\OCT\Case600FF.fmu --qss=QSS2 --dtOut=100 --out=SXF --var=..\..\Case600FF.var %* >run.log 2>&1
