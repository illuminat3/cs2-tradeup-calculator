@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

if not exist "data\" mkdir data

echo Running maintaining scripts
echo.

set FAILED=0

for %%f in (maintaining\*.py) do (
    echo Running %%f...
    set PYTHONPATH=%CD%
    python "%%f"
    if !errorlevel! neq 0 (
        echo %%f failed.
        set FAILED=1
    ) else (
        echo %%f completed.
    )
    echo.
)

if %FAILED%==1 (
    echo One or more scripts failed.
    exit /b 1
) else (
    echo All scripts completed successfully.
)