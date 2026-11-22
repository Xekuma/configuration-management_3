# Инициализация вектора длины 7 по адресам 0..6
reg[0] = 0
mem[0] = reg[0]
reg[0] = 1
mem[1] = reg[0]
reg[0] = 2
mem[2] = reg[0]
reg[0] = 4
mem[3] = reg[0]
reg[0] = 8
mem[4] = reg[0]
reg[0] = 15
mem[5] = reg[0]
reg[0] = 255
mem[6] = reg[0]

# Поэлементное побитовое "не" с записью в исходный вектор (0..6)
reg[1] = ~mem[0]
mem[0] = reg[1]
reg[1] = ~mem[1]
mem[1] = reg[1]
reg[1] = ~mem[2]
mem[2] = reg[1]
reg[1] = ~mem[3]
mem[3] = reg[1]
reg[1] = ~mem[4]
mem[4] = reg[1]
reg[1] = ~mem[5]
mem[5] = reg[1]
reg[1] = ~mem[6]
mem[6] = reg[1]