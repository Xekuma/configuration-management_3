# Инициализация исходного массива по адресам 10..14
reg[0] = 100
mem[10] = reg[0]
reg[0] = 200
mem[11] = reg[0]
reg[0] = 300
mem[12] = reg[0]
reg[0] = 400
mem[13] = reg[0]
reg[0] = 500
mem[14] = reg[0]

# Копирование массива из адресов 10..14 в адреса 20..24
reg[1] = 10
reg[2] = mem[reg[1]]
mem[20] = reg[2]

reg[1] = 11
reg[2] = mem[reg[1]]
mem[21] = reg[2]

reg[1] = 12
reg[2] = mem[reg[1]]
mem[22] = reg[2]

reg[1] = 13
reg[2] = mem[reg[1]]
mem[23] = reg[2]

reg[1] = 14
reg[2] = mem[reg[1]]
mem[24] = reg[2]