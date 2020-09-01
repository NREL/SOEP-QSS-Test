@echo off
QSS ..\..\OCT\EventIndicator5.fmu --qss=QSS3 --dtNum=2e-3 --out=trxo --statistics %* >run.log 2>&1
