@echo off

REM KuGame Test Script
REM Run all tests and type checks with one click

echo ==========================================
echo [TEST] KuGame Test Suite
echo ==========================================
echo.

REM Run pytest tests
echo [1/2] Running pytest tests...
echo ------------------------------------------
python -m pytest
set PYTEST_RESULT=%ERRORLEVEL%
echo.

REM Run mypy type checking
echo [2/2] Running mypy type checking...
echo ------------------------------------------
python -m mypy kugame/
set MYPY_RESULT=%ERRORLEVEL%
echo.

REM Display final results
echo ==========================================
echo [SUMMARY] Test Results
echo ==========================================
if %PYTEST_RESULT% equ 0 (
    echo [PASS] pytest tests: Passed
) else (
    echo [FAIL] pytest tests: Failed
)

if %MYPY_RESULT% equ 0 (
    echo [PASS] mypy type checking: Passed
) else (
    echo [FAIL] mypy type checking: Failed
)
echo ==========================================

REM Pause to view results
echo Press any key to exit...
pause > nul