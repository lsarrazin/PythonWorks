import operator
 
def getXor(msg, key):
    
    om = ''
    kl = len(key)
    for mi in range(len(msg)):
        
        cm = msg[mi]
        ck = key[mi % kl]   # Le modulo, c'est pour chiffrer un texte plus long que la clé
 
        cx = ord(cm) ^ ord(ck)  # Le XOR tout bête entre un caractère du message et de la clé
        om += chr(cx)
 
    return om
 
def txt2bin(msg):
 
    mbin = ''
    for c in msg:
        cbin = bin(ord(c))[2:]     # 2: pour enlever le 0b retourné par bin
        lbin = len(cbin)
        mbin += '0' * (8-lbin) + cbin + ' '  # Ajout de 0 pour avoir 8 bits à chaque fois
 
    return mbin
 
def txt2oct(msg):
 
    mo = ''
    for c in msg:
        mo += str(ord(c)) + ' '
 
    return mo
 
cle = 'cryptographie005'
message_initial = 'message urgent plus long que la clé'
 
msg_code = getXor(message_initial, cle)
msg_decode = getXor(msg_code, cle)
 
print('En binaire : ' + txt2bin(msg_code))
print('En octets : ' + txt2oct(msg_code))
print(msg_decode)
