@echo off
rem Build the local model FMU with JModelica
rem jm script customized for your system must be on your PATH
rem compile_fmu.JModelica.py and mod_xml.JModelica.py must be on your PATH
rem Run from the JModelica sub-directory of the model directory

rem Compile the FMU
compile_fmu.py
del PID_Controller.fmu >nul 2>nul
ren Modelica_Blocks_Examples_PID_Controller.fmu PID_Controller.fmu

rem Add index comment lines to XML
unzip -o PID_Controller.fmu modelDescription.xml >nul 2>nul
copy /Y modelDescription.xml modelDescription.orig.xml >nul 2>nul
mod_xml.JModelica.py
zip -f PID_Controller.fmu >nul 2>nul

