[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "=== ТЕСТ: Этап 1 ===`n"

Write-Host "-------------------------------------------------------"
Write-Host "=== 1. Режим тестирования (тесты из спецификации) ==="
Write-Host "Параметры: tests/spec_test.asm out.bin --test`n"
python src/main.py tests/spec_test.asm out.bin --test

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 2. Обычный запуск (без режима тестирования) ==="
Write-Host "Параметры: tests/spec_test.asm out.bin`n"
python src/main.py tests/spec_test.asm out.bin

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 3. Ошибка: исходный файл не найден ==="
Write-Host "Параметры: tests/missing.asm out.bin --test`n"
python src/main.py tests/missing.asm out.bin --test