@echo off
QSS ..\..\OCT\EventIndicator3.fmu --qss=QSS3 --dtNum=1e-4 --zTol=1e-6 --out=trxo --statistics %* >run.log 2>&1
