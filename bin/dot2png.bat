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
set PNG_FILE_NAME=%DOT_FILE_NAME:~0,-2%png
C:\Graphviz\bin\dot.exe -Tpng -Gdpi=300 %DOT_FILE_NAME% -o %PNG_FILE_NAME%
start %PNG_FILE_NAME%
:Exit
endlocal
