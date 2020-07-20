@echo off
QSS ..\..\OCT\HeatingCoolingHotWater3Clusters.fmu --qss=QSS2 --dtNum=1e-4 --zFac=10 --dtOut=100 --out=sFx --var=..\..\HeatingCoolingHotWater3Clusters.var >run.log 2>&1
