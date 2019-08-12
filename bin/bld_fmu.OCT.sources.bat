@echo off
rem Build the local model FMU with OCT
rem compile_fmu.OCT.py and mod_xml.OCT.py must be on your PATH
rem Run from the OCT sub-directory of the model directory

setlocal

rem Find tool directory and name
for /D %%d in (%cd%\) do set tool_dir=%%~dpd
for /D %%t in (%tool_dir:~0,-1%) do set tool=%%~nt
:UpLoop
if "%tool%" NEQ "Dymola" if "%tool%" NEQ "JModelica" if "%tool%" NEQ "OCT" if "%tool%" NEQ "Ptolemy" if "%tool%" NEQ "QSS" (
  for /D %%d in (%tool_dir:~0,-1%) do set tool_dir=%%~dpd
  for /D %%t in (%tool_dir:~0,-1%) do set tool=%%~nt
  goto UpLoop
)

rem Find model directory and name
for /D %%t in (%tool_dir:~0,-1%) do set model_dir=%%~dpt
for /D %%t in (%model_dir:~0,-1%) do set model=%%~nt

rem Compile the FMU
compile_fmu.OCT.sources.py %model_dir%\%model%.mo %*

rem Add index comment lines to XML
if exist "%model%.fmu" (
  unzip -o %model%.fmu modelDescription.xml >nul 2>nul
  copy /Y modelDescription.xml modelDescription.orig.xml >nul 2>nul
  mod_xml.OCT.py
  zip -f %model%.fmu >nul 2>nul
)

endlocal