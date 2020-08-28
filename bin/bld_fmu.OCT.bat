@echo off
rem Build the local model FMU with OCT
rem compile_fmu.OCT.py must be on your PATH
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
if exist "%tool_dir%%model%.ref" (
  compile_fmu.OCT.py %tool_dir%%model%.ref %*
) else (
if exist "%tool_dir%%model%.mo" (
  compile_fmu.OCT.py %tool_dir%%model%.mo %*
) else (
if exist "%model_dir%%model%.ref" (
  compile_fmu.OCT.py %model_dir%%model%.ref %*
) else (
if exist "%model_dir%%model%.mo" (
  compile_fmu.OCT.py %model_dir%%model%.mo %*
) else (
  echo "Neither Modelica (%model%.mo) nor ref (%model%.ref) files found in tool or model directories"
  exit /B 1
))))

endlocal
