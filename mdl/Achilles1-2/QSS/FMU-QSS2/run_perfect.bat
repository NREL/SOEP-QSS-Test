@echo off
QSS --qss=QSS2 ..\..\..\Achilles1\QSS\FMU-QSS2\Achilles1_QSS.fmu ..\..\..\Achilles2\QSS\FMU-QSS2\Achilles2_QSS.fmu --con=Achilles2.x1:Achilles1.x1 --con=Achilles1.x2:Achilles2.x2 --perfect
