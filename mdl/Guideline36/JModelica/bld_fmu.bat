@echo off
rem Build the local model FMU with OCT
rem compile_fmu.OCT.py and mod_xml.OCT.py must be on your PATH
rem Run from the OCT sub-directory of the model directory

setlocal

rem Set tool name
set tool=JModelica

rem Set model name and file
set mdl=Guideline36
set model=BBuildings.Examples.VAVReheat.%mdl%
set model_file=%MODELICA_BUILDINGS_LIB%\%model:.=\%.mo

rem Compile the FMU
compile_fmu.%tool%.py %model% %model_file% %*

rem Rename the FMU
if exist "%mdl%.fmu" del "%mdl%.fmu"
ren %model:.=_%.fmu %mdl%.fmu

endlocal