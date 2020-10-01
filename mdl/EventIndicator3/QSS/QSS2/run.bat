@echo off
QSS ..\..\OCT\EventIndicator3.fmu --qss=QSS2 --dtND=1e-3 --out=trxo --statistics %* >run.log 2>&1
