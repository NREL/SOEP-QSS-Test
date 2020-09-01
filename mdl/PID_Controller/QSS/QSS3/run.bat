@echo off
QSS ..\..\OCT\PID_Controller.fmu --qss=QSS3 --dtNum=5e-3 --out=trFxo --statistics --var=..\..\PID_Controller.var %* >run.log 2>&1
