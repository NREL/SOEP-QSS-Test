@echo off
:: Set environment for using these scripts with OCT
:: Customize for your system
set SOEP_QSS_Test_bin=%~dp0
set SOEP_QSS_Test_bin=%SOEP_QSS_Test_bin:~0,-1%
set PATH=%PATH%;%SOEP_QSS_Test_bin%;
call %SOEP_QSS_Test_bin%\set_Modelica_400.bat
set SOEP_QSS_Test_bin=
call C:\OCT\setenv.bat 64
set "PATH=%PATH%;%PYTHONHOME%\Tools\scripts"
set "PYTHON_DIR=%PYTHONHOME%"
set "PYTHON_INC=%PYTHON_DIR%\include"
set "PYTHON_LIB_DIR=%PYTHON_DIR%\libs"
set "PYTHON_LIB=%PYTHON_LIB_DIR%\python37.lib"
set "MODELON_LICENSE_PATH=%AppData%\Modelon\Licenses\NodeLocked"
