@echo off
QSS ..\..\OCT\PID_Controller.fmu --qss=QSS2 --dtNum=1e-4 --out=trFxo --var=..\..\PID_Controller.var %* >run.log 2>&1
