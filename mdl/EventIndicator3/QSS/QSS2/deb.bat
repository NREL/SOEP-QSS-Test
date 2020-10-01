@echo off
QSS ..\..\OCT\EventIndicator3.fmu --qss=QSS2 --dtND=1e-4 --zTol=1e-6 --out=trxod --statistics %* >deb.log 2>&1
