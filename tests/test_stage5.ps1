[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "=== ТЕСТ: Этап 5 (Вектор длины 7, побитовое НЕ) ===`n"

Write-Host "-------------------------------------------------------"
Write-Host "=== Пример 1: малые числа и степени двойки (0:6) ==="
python src/main.py tests/vector_not_1.asm out/vector_not_1.bin
python src/interpreter.py out/vector_not_1.bin out/vector_1.xml 0:6
Get-Content out/vector_1.xml

Write-Host "`n-------------------------------------------------------"
Write-Host "=== Пример 2: битовые маски hex (100:106) ==="
python src/main.py tests/vector_not_2.asm out/vector_not_2.bin
python src/interpreter.py out/vector_not_2.bin out/vector_2.xml 100:106
Get-Content out/vector_2.xml

Write-Host "`n-------------------------------------------------------"
Write-Host "=== Пример 3: произвольные десятичные числа (500:506) ==="
python src/main.py tests/vector_not_3.asm out/vector_not_3.bin
python src/interpreter.py out/vector_not_3.bin out/vector_3.xml 500:506
Get-Content out/vector_3.xml