# CryptoToolbox

The program has different modules implemented.

## Getting Started

### Vernam Algorithm
Implementation of Vernam algorithm. Basically, it applies bit-wise xor to files. The key
file will be repeated if necessary.
To decode apply xor to encoded file with the same key once again.

```
echo "KEY" > key.txt
echo "Encode me" | python main.py vernam -o encoded.txt -k key.txt
python main.py vernam -i encoded.txt -o decoded.txt -k key.txt
```

### Cesar Algorithm
Cesar algorithm operates on english alphabetical characters and ignores other symbols.
The implementation allows hacking cesar algorithm using statistical methods.
#### Encrypt
```
echo "ENCODE ME" > original.txt
python cesar encrypt -i original.txt -o encoded.txt --shift 13
cat encoded.txt
```

#### Decrypt
```
python cesar decrypt -i encoded.txt --shift 13
```

### Hack
To use hack you need big train file to calculate distribution of characters.
You can use following command to get one. 
```
curl https://norvig.com/big.txt --output train.txt
```
Also hack only works on big input files since we can extract more reliable information from them.
You can get big file to encode with the following command (although the file contains 
html tags they will not interfere with the algorithm's work):
```
curl https://norvig.com/ibol.html --output original.txt
```
Usage of hack:

```
python main.py cesar encrypt -i original.txt -o encoded.txt -s 9
python main.py cesar hack -i encoded.txt -o decoded.txt --train train.txt
```

### Vigenere Algorithm
Vigenere is a generalisation of Cesar Algorithm for several shifts.
#### Encrypt
```
echo "ENCODE ME" > original.txt
python main.py vigenere encrypt -i original.txt -o encoded.txt -k IAmKey
```

#### Decrypt
```
python main.py vigenere decrypt -i encoded.txt -k IAmKey
```
