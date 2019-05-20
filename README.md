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
Also you can choose language with --lang. Available options are --lang ru and --lang en.
#### Encrypt
```
echo "ENCODE ME" > original.txt
python main.py cesar encrypt -i original.txt -o encoded.txt --shift 13
cat encoded.txt
```

#### Decrypt
```
echo "RAPBQR ZR" > encoded.txt
python main.py cesar decrypt -i encoded.txt --shift 13
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
Vigenere is a generalisation of Cesar Algorithm for several shifts. You can also choose language from english and russian.
#### Encrypt
```
echo "ENCODE ME" > original.txt
python main.py vigenere encrypt -i original.txt -o encoded.txt -k IAmKey
```

#### Decrypt
```
python main.py vigenere decrypt -i encoded.txt -k IAmKey
```

### Writing your own module
If you want to extend the program and add new modules then you should follow the following steps:
#### Config file
Create config JSON file in config folder. 
```
{arguments: [
	{"names": ["--fullname", "-f"],
	"type": "int",
	"help": "Some help text"},	
	{"names": ["--second_fullname", "-f"],
	"type": "str",
	"help": "Some second help text"},
],
"parents": ["SomeParentConfig.json", "SomeSecondConfig.json"]
}
```
Names specify full and sortened name of option. Other arguments will be simply passed to add_argument of subparser except for type argument. It's impossible to write python function name in json so we use TypeCaster singleton object. It stores mapping from strings to actual type functions. If you want to add new type you should call 
```
TypeCaster().register_argument(your_name, your_func)
```
In module \_\_init\_\_ before calling super().\_\_init\_\_ which will parse the config.
