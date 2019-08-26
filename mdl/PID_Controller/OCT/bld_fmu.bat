@echo off
rem Build the local model FMU with OCT
rem jm script customized for your system must be on your PATH
rem compile_fmu.OCT.py and mod_xml.OCT.py must be on your PATH
rem Run from the OCT sub-directory of the model directory

rem Compile the FMU
compile_fmu.py
del PID_Controller.fmu >nul 2>nul
ren Modelica_Blocks_Examples_PID_Controller.fmu PID_Controller.fmu

