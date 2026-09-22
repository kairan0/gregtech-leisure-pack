@echo off
cd /d "%~dp0"
if not defined GTL_JAVA set "GTL_JAVA=java"
if defined GTL_PYTHON (
  "%GTL_PYTHON%" "%~dp0gtl-update.py" --java "%GTL_JAVA%" %*
) else (
  py -3 "%~dp0gtl-update.py" --java "%GTL_JAVA%" %*
)
exit /b %errorlevel%
