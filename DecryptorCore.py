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
    #Returns list of RoundKeys(16 RoundKeys)

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
    nope = input("Message to decrypt: ")
    Inp = nope.split(',')
    print Inp
       
    for i in range (len(Inp)):
        if i%2 == 0:
            messages.append(Inp[i])
        else:
            keys.append(Inp[i])
    print messages
    print keys
    #Sorts out messages from keys
    
    
