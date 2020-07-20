@echo off
QSS ..\..\OCT\StateEvent6.fmu --qss=QSS2 --dtMax=0.01 --var=..\..\StateEvent6.var %* >run.log 2>&1
