@echo off
setlocal enabledelayedexpansion
rem Set up environment for OCT and runs passed Python script
for %%x in (%1) do (set script=%%~$PATH:x)
if defined script (
  set MODELICA_BUILDINGS_LIB=C:\Projects\EnergyPlus\SOEP\tst\modelica-buildings
  call C:\OCT\setenv.bat 64
  "!PYTHONHOME!\python.exe" %script% %2 %3 %4 %5
) else (
  echo %1 not found
)
endlocal