@echo off
rem Build the local model FMU with OCT
rem compile_fmu.OCT.PyFMI.py must be on your PATH
rem Run from the OCT sub-directory of the model directory

setlocal

rem Set tool name
set tool=OCT

rem Set model name and file
set mdl=Case600
set model=Buildings.ThermalZones.Detailed.Validation.BESTEST.Cases6xx.%mdl%
set model_file=%MODELICA_BUILDINGS_LIB%\%model:.=\%.mo

rem Compile the FMU
compile_fmu.%tool%.PyFMI.py %model% %model_file% %*

rem Rename the FMU
del %mdl%.fmu >nul 2>nul
ren %model:.=_%.fmu %mdl%.fmu

endlocal