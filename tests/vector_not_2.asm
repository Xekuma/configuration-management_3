# Инициализация вектора длины 7 по адресам 100..106
reg[0] = 0x00000000
mem[100] = reg[0]
reg[0] = 0x0AAAAAAA
mem[101] = reg[0]
reg[0] = 0x05555555
mem[102] = reg[0]
reg[0] = 0x0F0F0F0F
mem[103] = reg[0]
reg[0] = 0x00FF00FF
mem[104] = reg[0]
reg[0] = 0x0000FFFF
mem[105] = reg[0]
reg[0] = 0x0FFFFFFF
mem[106] = reg[0]

# Поэлементное побитовое "не" с записью в исходный вектор (100..106)
reg[1] = ~mem[100]
mem[100] = reg[1]
reg[1] = ~mem[101]
mem[101] = reg[1]
reg[1] = ~mem[102]
mem[102] = reg[1]
reg[1] = ~mem[103]
mem[103] = reg[1]
reg[1] = ~mem[104]
mem[104] = reg[1]
reg[1] = ~mem[105]
mem[105] = reg[1]
reg[1] = ~mem[106]
mem[106] = reg[1]