@echo off
setlocal enabledelayedexpansion
:: Set up environment for OCT and runs passed Python script
for %%x in (%1) do (set script=%%~$PATH:x)
shift
if defined script (
  set MODELICA_BUILDINGS_LIB=C:\modelica-buildings
  call C:\OCT\setenv.bat 64
  "!PYTHONHOME!\python.exe" %script% %1 %2 %3 %4 %5 %6 %7 %8 %9
) else (
  echo %1 not found
)
endlocal
