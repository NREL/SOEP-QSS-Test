@echo off
rem Build the local model FMU with JModelica
rem compile_fmu.JModelica.py and mod_xml.JModelica.py must be on your PATH
rem Run from the JModelica sub-directory of the model directory

setlocal

rem Set tool name
set tool=JModelica

rem Set model name and file
set mdl=Case600
set model=Buildings.ThermalZones.Detailed.Validation.BESTEST.Cases6xx.%mdl%
set model_file=%MODELICA_BUILDINGS_LIB%\%model:.=\%.mo

rem Compile the FMU
compile_fmu.%tool%.py %model% %model_file% %*

rem Rename the FMU
del %mdl%.fmu >nul 2>nul
ren %model:.=_%.fmu %mdl%.fmu
set model=%mdl%

rem Add index comment lines to XML
if exist "%model%.fmu" (
  unzip -o %model%.fmu modelDescription.xml >nul 2>nul
  copy /Y modelDescription.xml modelDescription.orig.xml >nul 2>nul
  mod_xml.JModelica.py
  zip -f %model%.fmu >nul 2>nul
)

endlocal