@echo off
QSS ..\..\OCT\EventIndicator4.fmu --qss=QSS2 --dtND=1e-4 --dtInf=0.01 --out=trxo --statistics %* >run.log 2>&1
