def encrypt (private_key,message):
    import random

    def generaterandom (n):
        r = ""
        rnd = random.SystemRandom()
        for i in range(n):
            f = rnd.random()
            if f >= 0.5:
                r = r + "1"
            else:
                r = r + "0"
        r = int(r,2)
        return r
    # Generates random string of length n

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

    def messagedivide (mess):
        messages = []
        for i in range (1,(len(mess)/8)+ 2):
            messages.append(mess[(8*i-8):(8*i)])
        return messages
    #Divides messages into small pieces

    messages = messagedivide(messsage)
##    Splits message into 64 bit parts (8 ASCII)
##    characters, because algorithm uses only
##    64 bits
    private_key = int(private_key,10)
    while private_key < 10000000:
        private_key = 2*private_key
    private_key = str(private_key)
    private_key = private_key.encode("hex")
    private_key = private_key.lstrip("0x").rstrip("L")
    while len (private_key)< 16:
        private_key = "0"+private_key
    private_key = int(private_key,16)
    #Converts private key to 64 bit number in int

    for i in range (len(messages)):
        messages[i] = messages[i]encdoe("hex")
        messages[i] = messages[i].lstrip("0x").rstrip("L")
        while len(messages[i])<16:
            messages[i] = "0"+messages[i]
    for w in range(len(messages)):
        rndk = generaterandom(64) #Generates random key (64 bit)
        key = private_key^rndk
        if len(key) == 64:
            




        
