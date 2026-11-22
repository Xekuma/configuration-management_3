[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "=== ТЕСТ: Этап 4 ===`n"

Write-Host "-------------------------------------------------------"
Write-Host "=== 1. Ассемблирование теста АЛУ (побитовое НЕ) ==="
Write-Host "Параметры: tests/bitnot_test.asm out/bitnot_test.bin`n"
python src/main.py tests/bitnot_test.asm out/bitnot_test.bin

Write-Host "`n-------------------------------------------------------"
Write-Host "=== 2. Запуск интерпретатора и XML-дамп памяти 0:14 ==="
Write-Host "Параметры: out/bitnot_test.bin out/bitnot_dump.xml 0:14`n"
python src/interpreter.py out/bitnot_test.bin out/bitnot_dump.xml 0:14

Write-Host "`nСодержимое out/bitnot_dump.xml:"
Get-Content out/bitnot_dump.xml