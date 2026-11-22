[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "=== ТЕСТ: Этап 3 ===`n"

Write-Host "-------------------------------------------------------"
Write-Host "=== 1. Ассемблирование программы копирования массива ==="
Write-Host "Параметры: tests/copy_array.asm out/copy_array.bin`n"
python src/main.py tests/copy_array.asm out/copy_array.bin

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 2. Запуск интерпретатора и XML-дамп памяти 10:24 ==="
Write-Host "Параметры: out/copy_array.bin out/copy_dump.xml 10:24`n"
python src/interpreter.py out/copy_array.bin out/copy_dump.xml 10:24

Write-Host "`nСодержимое out/copy_dump.xml:"
Get-Content out/copy_dump.xml

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 3. Ошибка: некорректный диапазон адресов ==="
Write-Host "Параметры: out/copy_array.bin out/err.xml 25:10`n"
python src/interpreter.py out/copy_array.bin out/err.xml 25:10