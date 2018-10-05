@echo off
rem Set environment for using these scripts with OCT
rem Customize for the directory of the Buildings library
set MODELICAPATH=C:\OCT\install\ThirdParty\MSL;C:\Projects\EnergyPlus\SOEP\tst\modelica-buildings
set MODELICA_BUILDINGS_LIB=C:\Projects\EnergyPlus\SOEP\tst\modelica-buildings
set batPath=%~dp0
set batPath=%batPath:~0,-1%
set PATH=%PATH%%batPath%;
set batPath=
call C:\OCT\setenv.bat 64
