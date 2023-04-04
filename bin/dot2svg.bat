@echo off
setlocal
if exist %1.gv (
  set DOT_FILE_NAME=%1.gv
) else (
  if exist %1 (
    set DOT_FILE_NAME=%1
  ) else (
    echo Dot file not found!
    goto Exit
  )
)
set SVG_FILE_NAME=%DOT_FILE_NAME:~0,-2%svg
C:\Graphviz\bin\dot.exe -Tsvg %DOT_FILE_NAME% -o %SVG_FILE_NAME%
start %SVG_FILE_NAME%
:Exit
endlocal
