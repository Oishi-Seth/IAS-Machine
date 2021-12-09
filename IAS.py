# Made by Oishi Seth IMT2020525
# Made by V L Sahithi IMT2020047

# Function to convert binary to decimal number
def binaryToDecimal(n):
    return int(n,2)

# Function to convert decimal number to binary with leading zeroes
def decimalToBinary(n,h):
    return format(n, 'b').zfill(h)

# Function to convert sign-magnitude binary to decimal number
def signMagBinaryToDecimal(n):
    if (n[0]=='0'):
        return int(n[1:],2)
    elif (n[0]=='1'):
        return -1 * int(n[1:],2)

# Function to convert decimal number to sign-magnitude binary
def decimalToSignMagBinary(n):
    if n>=0:
        n_1 = '0'
        n_2 = decimalToBinary(n, 39)
    else:
        n_1 = '1'
        n_2 = decimalToBinary(-n, 39)
    return n_1 + n_2

# Function to fetch left instruction
def leftInstruction(Instruction):
    left_inst = []
    left_inst.append(Instruction[0:8])
    left_inst.append(Instruction[8:20])
    return left_inst

# Function to fetch right instruction
def rightInstruction(Instruction):
    right_inst = []
    right_inst.append(Instruction[20:28])
    right_inst.append(Instruction[28:40])
    return right_inst



# Initialising memory which holds instructions and data
instruction_mem=[]
for i in range(500):
    instruction_mem.append(decimalToBinary(0,40))

data_mem=[]
for i in range(500):
    data_mem.append(decimalToBinary(0,40))



# Taking input from user
print("Enter 2 numbers to add (a+b):")
a=int(input())
b=int(input())
print("Enter 2 number to subtract and then left shift (LSH(c-d)):")
c=int(input())
d=int(input())



# Opcode of instructions
INSTRUCTION_DICT = {
        '00100001' : 'STOR M(X)',
        '00000001' : 'LOAD M(X)',
        '00000101' : 'ADD M(X)',
        '00000110' : 'SUB M(X)',
        '00010100' : 'LSH',
        '11111111' : 'STOP'
}


# Writing assembly language instruction
instruction_mem[0] = '00000001' + decimalToBinary(200,12) + '00000101' + decimalToBinary(201,12)
instruction_mem[1] = '00100001' + decimalToBinary(400,12) + '00000001' + decimalToBinary(202,12)
instruction_mem[2] = '00000110' + decimalToBinary(203,12) + '00010100' + decimalToBinary(1000,12)
instruction_mem[3] = '00100001' + decimalToBinary(401,12) + '11111111' + decimalToBinary(1000,12)


# Storing user inputs into data memory in binary form
data_mem[200] = decimalToSignMagBinary(a)
data_mem[201] = decimalToSignMagBinary(b)
data_mem[202] = decimalToSignMagBinary(c)
data_mem[203] = decimalToSignMagBinary(d)



# Initialising the registers
PC = decimalToBinary(0,12)         # Program Counter
MAR = decimalToBinary(0,12)         # Memory AAddress Register
IR = decimalToBinary(0,8)           # Instruction Register
IBR = decimalToBinary(0,20)         # Instruction Buffer Register
AC = decimalToBinary(0,40)          # Accumulator
MBR = decimalToBinary(0,40)         # Memory Buffer Register
MQ = decimalToBinary(0,40)          # Multiply/Quotient



def decode(opcode):
    if opcode == 'LOAD M(X)':
        global MBR
        MBR = data_mem[binaryToDecimal(MAR)]
        global AC
        AC = MBR
        print('Value loaded in AC = ' + str(signMagBinaryToDecimal(AC)))

    if opcode == 'ADD M(X)':
        MBR = data_mem[binaryToDecimal(MAR)]
        print('Value loaded in MBR = ' + str(signMagBinaryToDecimal(MBR)))
        total = signMagBinaryToDecimal(AC) + signMagBinaryToDecimal(MBR)
        AC = decimalToSignMagBinary(total)

    if opcode == 'SUB M(X)':
        MBR = data_mem[binaryToDecimal(MAR)]
        print('Value loaded in MBR = ' + str(signMagBinaryToDecimal(MBR)))
        diff = signMagBinaryToDecimal(AC) - signMagBinaryToDecimal(MBR)
        AC = decimalToSignMagBinary(diff)

    if opcode == 'LSH':
        n = signMagBinaryToDecimal(AC)
        n = n*2
        AC = decimalToSignMagBinary(n)
        print('Value loaded in AC = ' + str(signMagBinaryToDecimal(AC)))

    if opcode == 'STOR M(X)':
        MBR = AC
        data_mem[binaryToDecimal(MAR)] = MBR
        print('Result = '+str(signMagBinaryToDecimal(MBR)))

    if opcode == 'STOP':
        global IR
        IR = '11111111'
        print('Execution complete.')



# Execution cycle
instruction = 'left'
while IR != '11111111':
    if instruction == 'left':
        MAR = PC                                                   # The next instruction address is stored in PC which is loaded to MAR
        MBR = instruction_mem[binaryToDecimal(MAR)]                # The 40 bit instruction from memory is loaded to MBR
        left = leftInstruction(MBR)                                # Left instruction is fetched from MBR
        right = rightInstruction(MBR)                              # Right instruction is fetched from MBR
        IBR = right[0]+right[1]                                    # Right instruction is stored in IBR
        IR = left[0]                                               # Opcode of Left instruction is loaded to IR
        MAR = left[1]                                              # Address of Left instruction is loaded to MAR
        decode(INSTRUCTION_DICT[IR])                               # Executing instruction based on opcode
        instruction = 'right'

    if instruction == 'right':
        IR = IBR[0:8]                                              # Opcode of right instruction is loaded to IR from IBR
        MAR = IBR[8:20]                                            # Address of right instruction is loaded to MAR from IBR
        decode(INSTRUCTION_DICT[IR])                               # Executing instruction based on opcode
        PC = decimalToBinary(binaryToDecimal(PC)+1,12)             # PC is incremented
        instruction = 'left'


