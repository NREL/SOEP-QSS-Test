@echo off
rem Set environment for using these scripts with JModelica + QSS
rem Customize for your system
set MODELICA_BUILDINGS_LIB=C:\Projects\EnergyPlus\SOEP\tst\modelica-buildings
set MODELICAPATH=C:\JModelica\install\ThirdParty\MSL;%MODELICA_BUILDINGS_LIB%;.;..
set batPath=%~dp0
set batPath=%batPath:~0,-1%
set PATH=%PATH%;%batPath%;
set batPath=
call C:\JModelica\setenv.bat 64
call setIC.bat
set PATH=%PATH%;C:\Projects\EnergyPlus\SOEP\dev\QSS_x\bin\Windows\IC\64\r
