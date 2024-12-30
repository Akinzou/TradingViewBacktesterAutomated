import sys
sl = int(sys.argv[1])*-1
file_name = sys.argv[2]
print("min: ", sl)
print("nazwa: ", file_name)

with open(sys.argv[2], 'a') as plik:
    plik.write(str(sl) + '\n')