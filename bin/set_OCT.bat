@echo off
rem Set environment for using these scripts with OCT
rem Customize for your system
set batPath=%~dp0
set batPath=%batPath:~0,-1%
call %batPath%\set_MODELICA.bat
set PATH=%PATH%;%batPath%;
set LIB=%LIB%;C:\OCT\install\Python\tests_jmodelica\files\Programs\Load_and_initialize
set batPath=
call C:\OCT\setenv.bat 64
