def makeroundkey (key1,key2,strings):
    a=1
    b=2
    RoundKeys = []
    #Default Values

    key1 = int(key1,2)
    key2 = int(key2,2)
    #Formats key values into hex with proper length

    for i in range(16):
        strings[i] = int(strings[i].encode("hex"),16)
    #Puts strings into hex

    for i in range (16):
        if i%2==0:
            RoundKeys.append(key2^strings[i])
        elif i%2==1:
            RoundKeys.append(key1^strings[i])
        else:
            RoundKeys.append(key2^strings[i])
    #Sorts RoundKeys in right order
    return RoundKeys

Pk = int(raw_input("Insert your private cipher key: ")) #Privatekey
while Pk <(10000000):
    Pk = Pk + Pk
Pk = str(Pk)
Pk = Pk.encode("hex")
Pk = bin(int(Pk,16))[2:]
Pk = int(Pk,2)
#Takes in private key


q = 1
while q == 1:
    messages = []
    keys = []
    inp = input("Message to decrypt: ")
    for i in range (len(inp)):
        if i%2 == 0:
            messages.append(inp[i])
        else:
            keys.append(inp[i])
    #Sorts out messages from keys

    for i in range (len(keys)):
        keys[i] = keys[i].decode("hex")
        keys[i] = int(keys[i],16)
        K = Pk^keys[i]        
        print K

        k1 = ""
        k2 = ""
        K = bin(K)
        K = K.lstrip("0b")
        while len(K)<64:
            K="0"+K
        #Corrects Lengths
        for i in range (32):
            k1 = k1 + K[i]
            k2 = k2 + K[32+i]
        #Splits K into k1 and k2
        
    
