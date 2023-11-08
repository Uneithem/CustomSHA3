# CustomSHA3
This is my attempt to write SHA-256
It's not implemented well enough as my results and desired ones differ
for example this code: 

pt = ''
start = time.time()
hash_ = CustomSHA3(pt)
hash_ = hex(int(hash_, 2))[2:]
end = time.time()
print(hash_, '\n', end - start)
print(bin(int(hash_, 16))[2:])
start = time.time()
encoded_str = pt.encode()
hash_lib = hashlib.sha3_256(encoded_str).hexdigest()
end = time.time()
print(hash_lib, '\n', end - start)
print(bin(int(hashlib.sha3_256(encoded_str).hexdigest(), 16))[2:])

shows that hashvalue is wrong (mainly, there are more zeros in my output compared to the desired output) and time needed for calculations is bigger than in hashlib library
I'm sure that all of the functions are implemented correctly, the are only reasons why it's not working:
1. minor error in the implementation
2. There are mistakes in the source I've taken information from
