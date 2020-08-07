@echo off
rem Set environment for using these scripts with OCT
rem Customize for the directories on your system
set MODELICA_BUILDINGS_LIB=C:\Projects\EnergyPlus\SOEP\tst\modelica-buildings
set MODELICAPATH=C:\OCT\install\ThirdParty\MSL;%MODELICA_BUILDINGS_LIB%;.;..
set batPath=%~dp0
set batPath=%batPath:~0,-1%
set PATH=%PATH%;%batPath%;
set LIB=%LIB%;C:\OCT\install\Python\tests_jmodelica\files\Programs\Load_and_initialize
set batPath=
call C:\OCT\setenv.bat 64
