import unicodedata

spaces = [
0x0020,
0x00A0,
0x1680,
0x2000,
0x2001,
0x2002,
0x2003,
0x2004,
0x2005,
0x2006,
0x2007,
0x2008,
0x2009,
0x200A,
0x200B,
0x202F,
0x205F,
0x3000,
0xFEFF
]

def analyze(inp):
    ans = 0
    read_number = False
    end_of_read = False
    for current_char in inp:
        if current_char == '\n': break
        if current_char.isdigit():
            if end_of_read: return "N/A"
            read_number = True
            ans *= 10
            ans += int(unicodedata.normalize('NFKD', current_char))
        elif ord(current_char) in spaces:
            end_of_read |= read_number
        else:
            return "N/A"
    return hex(ans)

input_file = 'submitInput.txt'
lines = open(input_file, 'r', errors='strict', encoding='utf-16-le').readlines()
T = int(analyze(lines[0]), 16)

for tc in range(1, T+1):
    ans = analyze(lines[tc])
    print("Case #%d: %s"%(tc, ans.replace('0x', '')))
