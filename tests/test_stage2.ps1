[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "=== ТЕСТ: Этап 2 ===`n"

Write-Host "-------------------------------------------------------"
Write-Host "=== 1. Режим тестирования (байты из спецификации) ==="
Write-Host "Параметры: tests/spec_test.asm out/spec_test.bin --test`n"
python src/main.py tests/spec_test.asm out/spec_test.bin --test

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 2. Обычный запуск и проверка размера бинарника ==="
Write-Host "Параметры: tests/spec_test.asm out/spec_test.bin`n"
python src/main.py tests/spec_test.asm out/spec_test.bin
$Size = (Get-Item out/spec_test.bin).Length
Write-Host "Размер out/spec_test.bin: $Size байт (ожидается 17)"

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 3. Ошибка: исходный файл не найден ==="
Write-Host "Параметры: tests/missing.asm out/spec_test.bin --test`n"
python src/main.py tests/missing.asm out/spec_test.bin --test