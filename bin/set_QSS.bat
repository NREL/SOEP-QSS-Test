@echo off
rem Set environment for using these scripts with QSS
rem Customize for your system
set SOEP_QSS_Test_bin=%~dp0
set SOEP_QSS_Test_bin=%SOEP_QSS_Test_bin:~0,-1%
set PATH=%PATH%;%SOEP_QSS_Test_bin%;
set SOEP_QSS_Test_bin=
