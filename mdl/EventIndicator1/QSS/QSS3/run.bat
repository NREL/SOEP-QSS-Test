@echo off
QSS ..\..\OCT\EventIndicator1.fmu --qss=QSS3 --dtND=1e-4 --out=trxo --statistics %* >run.log 2>&1
