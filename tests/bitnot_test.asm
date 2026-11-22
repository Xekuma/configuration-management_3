# Исходные данные по адресам 0..3
reg[0] = 0
mem[0] = reg[0]

reg[0] = 15
mem[1] = reg[0]

reg[0] = 0x0F0F0F0F
mem[2] = reg[0]

reg[0] = 0x0FFFFFFF
mem[3] = reg[0]

# Выполнение побитового "не" и запись результатов в адреса 10..13
reg[1] = ~mem[0]
mem[10] = reg[1]

reg[2] = ~mem[1]
mem[11] = reg[2]

reg[3] = ~mem[2]
mem[12] = reg[3]

reg[4] = ~mem[3]
mem[13] = reg[4]

# Проверка двойного отрицания: ~~mem[2] == mem[2] -> адрес 14
reg[5] = ~mem[12]
mem[14] = reg[5]