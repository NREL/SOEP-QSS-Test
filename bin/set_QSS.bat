@echo off
:: Set environment for running QSS
set PATH=%PATH%;%~dp0
set OMP_NUM_THREADS=6
set OMP_WAIT_POLICY=ACTIVE
