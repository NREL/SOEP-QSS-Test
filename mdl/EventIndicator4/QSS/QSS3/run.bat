@echo off
QSS ..\..\OCT\EventIndicator4.fmu --qss=QSS3 --dtNum=1e-4 --dtMax=0.1 --out=trxo --statistics %* >run.log 2>&1
