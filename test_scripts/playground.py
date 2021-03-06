import time
import numpy as np

text = 'abcdefg'
text = text[:1] + 'Z' + text[2:]
print(text)

string = '039483247'
arr = np.array([0, 3, 9, 4, 8, 3, 2, 4, 7])
arr_candidate = 8
string_candidate = '8'

string_start = time.time()
for i in range(1000000):
    temp = string_candidate in string
    e = text[:1] + 'Z' + text[2:]
print("String: ")
print(time.time() - string_start)

numpy_start = time.time()
for i in range(1000000):
    temp = arr_candidate in arr
print("Numpy: ")
print(time.time() - numpy_start)

thing = 0b00101101
binary_start = time.time()
for i in range(1000000):
    temp = (thing & 0b00100000) > 0
    poi = bin(thing).count("1")
print("Binary: ")
print(time.time() - binary_start)
