@echo off
cd /d "%~dp0"
setlocal

echo Gerando Latencia...

where py >nul 2>nul
if errorlevel 1 (
    echo Python nao foi encontrado.
    pause
    exit /b 1
)

if not exist .venv py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --disable-pip-version-check -q -r requirements-dev.txt

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release
mkdir release

pyinstaller Latencia.spec --noconfirm --clean
if errorlevel 1 goto fail

copy /y dist\Latencia.exe release\Latencia.exe >nul

where ISCC.exe >nul 2>nul
if errorlevel 1 (
    echo.
    echo Latencia.exe pronto em release\Latencia.exe
    echo O Inno Setup nao esta instalado, entao o instalador nao foi gerado.
    pause
    exit /b 0
)

ISCC.exe installer\Latencia.iss
if errorlevel 1 goto fail

echo.
echo Pronto.
echo release\Latencia.exe
echo release\Latencia-Setup.exe
pause
exit /b 0

:fail
echo.
echo A build falhou.
pause
exit /b 1
