@echo off
QSS --qss=QSS2 ..\..\..\Achilles1\OCT\Achilles1.fmu ..\..\..\Achilles2\OCT\Achilles2.fmu --con=Achilles2.x1:Achilles1.x1 --con=Achilles1.x2:Achilles2.x2 --dtInf=0.001 %* >run.log 2>&1
