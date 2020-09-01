@echo off
QSS ..\..\OCT\EventIndicator2.fmu --qss=QSS2 --zFac=4 --out=trxo --statistics %* >run.log 2>&1
