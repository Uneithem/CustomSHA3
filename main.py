def CustomSHA3(pt):
    pt = InputTransform(pt)
    padded = padding(pt)
    blocks = []
    rate = ''.zfill(1088)
    cap = ''.zfill(512)
    for i in range(0, len(padded), 1088):
        blocks.append(padded[i:i + 1088])
    for i in range(0, len(blocks)):
        word = XOR(blocks[i], rate) + cap
        for r in range(0, 24):
            word = func(word, r)
        rate = word[:1088]
        cap = word[1088:]
    return word[:256]

def func(text, round):
    A = []
    #firstly, I break the input and assign it to matrix of 5x5x64
    for i in range(0, 5):
        A.append([])
        for j in range(0, 5):
            A[i].append(text[i * 320 + j * 64:i * 320 + j * 64 + 64])
    Apr = A.copy()
    A.clear()
    #as elements in this marix are permutated in SHA-3
    for i in range(0, 5):
        A.append([])
        for j in range(0, 5):
            A[i].append(Apr[(i+3) % 5][(j + 3) % 5])
    Apr.clear()
    #implementation of theta function
    C = []
    for i in range(0, 5):
        C.append(XOR(A[i][4], XOR(A[i][3], XOR(A[i][2], XOR(A[i][1], A[i][0])))))
    D = []
    for i in range(0, 5):
        row = ''
        for k in range(0, 64):
            row += XOR(C[(i - 1) % 5][k], C[(i + 1) % 5][(k - 1) % 64])
        D.append(row)
    Aprime = []
    for i in range(0, 5):
        Aprime.append([])
        for j in range(0, 5):
            Aprime[i].append(XOR(A[i][j], D[i]))
    #ro function, I clear Aprime and copy Aprime into A in order to keep A as input and Aprime as an output
    A = Aprime.copy()
    Aprime.clear()
    ro_const = [[0, 36, 3, 105, 210], [1, 300, 10, 45, 66], [190, 6, 171, 15, 253], [28, 55, 153, 21, 120], [91, 276, 231, 136, 78]]
    for i in range(0, 5):
        Aprime.append([])
        for j in range(0, 5):
            string = A[i][j]
            Aprime[i].append(string[len(string) - ro_const[i][j] % 64:] + string[:len(string) - ro_const[i][j] % 64])
    #pi function
    A = Aprime.copy()
    Aprime.clear()
    for i in range(0, 5):
        Aprime.append([])
        for j in range(0, 5):
            Aprime[i].append(A[(i + 3*j) % 5][i])
    #chi function
    A = Aprime.copy()
    Aprime.clear()
    for i in range(0, 5):
        Aprime.append([])
        for j in range(0, 5):
            Aprime[i].append(XOR(A[i][j], AND(NOT(A[(i + 1) % 5][j]), A[(i + 2) % 5][j])))
    #iota function
    A = Aprime.copy()
    Aprime.clear()
    iota_const = [bin(int('0000000000000001', 16))[2:], bin(int('0000000000008082', 16))[2:],
                  bin(int('800000000000808A', 16))[2:], bin(int('8000000080008000', 16))[2:],
                  bin(int('000000000000808B', 16))[2:], bin(int('0000000080000001', 16))[2:],
                  bin(int('8000000080008081', 16))[2:], bin(int('8000000000008009', 16))[2:],
                  bin(int('000000000000008A', 16))[2:], bin(int('0000000000000088', 16))[2:],
                  bin(int('0000000080008009', 16))[2:], bin(int('000000008000000A', 16))[2:],
                  bin(int('000000008000808B', 16))[2:], bin(int('800000008000008B', 16))[2:],
                  bin(int('8000000000008089', 16))[2:], bin(int('8000000000008003', 16))[2:],
                  bin(int('8000000000008002', 16))[2:], bin(int('8000000000000080', 16))[2:],
                  bin(int('000000000000800A', 16))[2:], bin(int('800000008000000A', 16))[2:],
                  bin(int('8000000080008081', 16))[2:], bin(int('8000000000008080', 16))[2:],
                  bin(int('0000000080000001', 16))[2:], bin(int('8000000080008008', 16))[2:]]
    round_iota = iota_const[round]
    while len(round_iota) < 64:
        round_iota = '0' + round_iota
    for i in range(0, 5):
        Aprime.append([])
        for j in range(0, 5):
            string = ''
            for k in range(0, 64):
                if k == 1 or k == 3 or k == 7 or k == 15 or k == 63:
                    string += XOR(A[i][j][k], round_iota[k])
                else:
                    string += A[i][j][k]
            Aprime[i].append(string)
    result = ''
    for i in range(0, 5):
        for j in range(0, 5):
            result += Aprime[i][j]
    return result


def XOR(stra, strb):
    res = ''
    for i in range(0, len(stra)):
        if stra[i] == strb[i]:
            res += '0'
        else:
            res += '1'
    return res

def NOT(stra):
    res = ''
    for i in range(0, len(stra)):
        if stra[i] == '1':
            res += '0'
        else:
            res += '1'
    return res

def AND(stra, strb):
    res = ''
    for i in range(0, len(stra)):
        if stra[i] == strb[i]:
            res += '1'
        else:
            res += '0'
    return res
def InputTransform(text):
    bintext = ''
    for i in text:
        bintext += bin(ord(i))[2:].zfill(8)
    return bintext

def padding (text):
    text += '1'
    while (len(text) + 1) % 1088 != 0:
        text += '0'
    text += '1'
    return text
