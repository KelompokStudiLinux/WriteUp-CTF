
passkey = '******' 
wut = {'10':'X', '01':'W', '00':'Y', '11':'Z'}

def encode(words,passkey, wut):
    cipher = ''
    passkey = passkey.lower()
    for word in words:
        char = bin(ord(word)^sum([ord(s) for s in passkey]))[2:]
        for c in range(0,len(char),2):
            for k,v in wut.items():
                if ''.join(char[c:c+2]) in k:
                    cipher+=v
    return cipher