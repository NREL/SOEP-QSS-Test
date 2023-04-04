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
set PDF_FILE_NAME=%DOT_FILE_NAME:~0,-2%pdf
C:\Graphviz\bin\dot.exe -Tpdf %DOT_FILE_NAME% -o %PDF_FILE_NAME%
start %PDF_FILE_NAME%
:Exit
endlocal
