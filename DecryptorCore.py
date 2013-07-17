def makeroundkey (key1,key2,strings):
    a=1
    b=2
    RoundKeys = []
    #Default Values

    key1 = int(key1,2)
    key2 = int(key2,2)
    #Formats key values into int with proper length

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
while q == 1: #Infinite loop
    messages = []
    keys = []
    nope = input("Message to decrypt: ")
    if nope == "*Kubinova*":
        print "Satan"
    #EasterEgg1
    Inp = nope.split(',')
    #Converts string to array
       
    for i in range (len(Inp)):
        if i%2 == 0:
            messages.append(Inp[i])
        else:
            keys.append(Inp[i])
    #Sorts out messages from keys

    for w in range (len(keys)):
        keys[w] = keys[w].encode("hex")
        keys[w] = int(keys[w],16)
        K = Pk^keys[w]        
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

        RoundStrings = ["aeiouywg","chjmnbtr","loqd4850","zukhq4mn","uqwrifs2",
        "ctelmrdz","afjajc23","is2xafw8","svgw8e2r","hv2j39fs","jkdsg3e/","svls;wa4",
        "asfh29ce", "ajv29fsa", "ajf983fc", "xiw20dfs"]
        #Resets default value of RS

        RoundKeys = makeroundkey(k1,k2,RoundStrings)
        #messages[w] = messages[w].encode("hex")
        #Converts every message back to hex value

        for i in range (16):
            RoundKeys[i] = int(bin(RoundKeys[i]),2)
        #Right format for RoundKeys
        while len(messages[w]) != 32:
            messages[w] = "0"+messages[w]
        #Corrects lengths in hex
            
        Output = []
        Right = []
        Left = []
        # Sets lists for Feistel

        for x in range (16):
            if x == 0:
                Kubinova = int(messages[w][:16],16)
                Right.append(Kubinova)
                Satan = int(messages[w][16:],16)
                Left.append(Satan)
            else:
                Right.append(Left[x-1])
                Left.append(Right[x-1]^(Left[x-1]^RoundKeys[x-1]))
        #16 Round Feistel Network (16RFN)

        Right[15] = hex(Right[15])
        Left[15] = hex(Left[15])
        Right[15] = Right[15].lstrip("0x").rstrip("L")
        Left[15] = Left[15].lstrip("0x").rstrip("L")

        print Right[15]
        print Left[15]
        
                
                
                
            
        
        
                
            
        

        
    
