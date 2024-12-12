@echo off
echo Iniciando proceso de flasheo para ESP32...
echo.

REM Borrar la memoria flash
echo Borrando la memoria flash...
python -m esptool --chip esp32 --port COM8 erase_flash
if %errorlevel% neq 0 (
    echo Error al borrar la memoria flash. Verifica la conexión y vuelve a intentarlo.
    pause
    exit /b
)

REM Escribir el nuevo firmware
echo Escribiendo el firmware...
python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash 0x1000 espMicro.bin
if %errorlevel% neq 0 (
    echo Error al escribir el firmware. Verifica la conexión y vuelve a intentarlo.
    pause
    exit /b
)

echo.
echo Proceso de flasheo completado con éxito.
pause
