# String Transformer

![string transformer the transformation tool](https://s32.postimg.org/se5y3sl39/cyberbots_revised_autobots_faction_symbol_by_t.png)

## The transformtion tool

Sometimes when you are playing CTFs you get an string and you need a fast way to generate its equivalents (hexa,octal,md5,etc) and analyze them. String transformer is a python script that takes an input (or list of inputs) and transforms them into several representations; please note that this tool is currently on development so expect a lot of changes and improvements.

## Usage

```
stringTransformer v0.1 (https://github.com/alevsk/stringTransformer/)

Usage: stringTransformer.py -i INPUT_STRING | --input INPUT_STRING | --load FILE

Options:
  -h/--help             show this help message and exit
  -i/--input=INPUT      set the input string to test with
  -l/--load=LOAD_FILE   load list of input strings (one per line)
  -x/--exclude=EXCLUDE  exclude this representations
  -o/--only=ONLY        transform input only to this representations
  -O/--output=OUTPUT    generate an output file
  --list                list available input representations
  --update              update from the official git repository

Examples:
./stringTransformer.py -i [STRING]
./stringTransformer.py -i [STRING] --exclude "hexa, octal"
./stringTransformer.py -i [STRING] --only "hexa, octal"
./stringTransformer.py -i [STRING] --params "rot.cipher=13,rot.encoding=utf-8"
./stringTransformer.py --load list.txt
./stringTransformer.py --list
```
## Extending the application

Transformation modules are located in `representations` folder.
You can help extends the functionality of this tool by creating your own modules in a very simple way, first you need to create a new python class. 

NOTE: you can use the following code as an example:

```
#!/usr/bin/env python -B
class module:
    def transform(self,input, parameters = {}):
        '''your transformation algorithm'''
        return  input
```
You must respect the following conventions:

* `Class name` is the same as the `file name`
* Class must have a function called `transform` that receive at least two parameters (self & input) and an optional third parameter (an object that serves as a parameter holder for customization)
* `transform` function must return an string

ie: `hexa` module:

```
#!/usr/bin/env python -B
class hexa:
    def transform(self,input):
        return  "0x".join("{:02x} ".format(ord(c)) for c in input)
```
## Reporting Issues

You can use the `Issues` section, I will be happy to improve the tool in every possible way

## Contributing

Just submit a pull request. We can review and talk through it there. Feel free to ask any questions in issues or you can contact me on [@Alevsk](https://twitter.com/Alevsk)

# License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.