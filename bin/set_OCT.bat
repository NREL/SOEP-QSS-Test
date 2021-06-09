@echo off
rem Set environment for using these scripts with OCT
rem Customize for your system
set SOEP_QSS_Test_bin=%~dp0
set SOEP_QSS_Test_bin=%SOEP_QSS_Test_bin:~0,-1%
set PATH=%PATH%;%SOEP_QSS_Test_bin%;
call %SOEP_QSS_Test_bin%\set_MODELICA.bat
set LIB=%LIB%;C:\OCT\install\Python\tests_jmodelica\files\Programs\Load_and_initialize
set SOEP_QSS_Test_bin=
call C:\OCT\setenv.bat 64
