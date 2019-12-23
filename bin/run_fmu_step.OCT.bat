@echo off
rem Run the local model FMU with PyFMI
rem jm script customized for your system must be on your PATH
rem run_fmu.py must be on your PATH
rem Run from the modeling tool directory such as MyModel\OCT

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

rem Run the simulation with PyFMI
if exist "%model_dir%%model%.var" (
  call jm.OCT.bat run_fmu_step.py %tool_dir%%model%.fmu --var %model_dir%%model%.var %*
) else (
if exist "%tool_dir%%model%.fmu" (
  call jm.OCT.bat run_fmu_step.py %tool_dir%%model%.fmu %*
) else (
  call jm.OCT.bat run_fmu_step.py %*
))