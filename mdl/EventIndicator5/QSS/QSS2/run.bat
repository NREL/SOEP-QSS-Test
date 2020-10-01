@echo off
QSS ..\..\OCT\EventIndicator5.fmu --qss=QSS2 --dtND=1e-4 --out=trxo --statistics %* >run.log 2>&1
