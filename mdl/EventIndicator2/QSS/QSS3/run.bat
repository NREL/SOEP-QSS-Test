@echo off
QSS ..\..\OCT\EventIndicator2.fmu --qss=QSS3 --zFac=2 --dtNum=1e-4 --out=trxo --statistics %* >run.log 2>&1
