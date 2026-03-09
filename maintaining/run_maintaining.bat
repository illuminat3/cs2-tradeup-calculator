@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

if not exist "data\" mkdir data

echo Running maintaining scripts
echo.

set "FAILED=0"

for %%f in (maintaining\*.py) do (
    echo Running %%f...
    set "PYTHONPATH=%CD%"
    python "%%f"
    if !errorlevel! neq 0 (
        echo.
        echo %%f failed.
        set "FAILED=1"
        echo Press any key to close...
        pause >nul
        exit /b 1
    ) else (
	echo.
        echo %%f completed.
	pause >nul
    )
    echo.
)

echo All scripts completed successfully.
exit /b 0