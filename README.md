# argfuscator
Argfuscator is a tool used to randomize and obfuscate PowerShell command-line arguments.

Blog post - [04MAR2017 - argfuscator - Obfuscating and randomizing PowerShell arguments](http://ropgadget.com/posts/intro_argfuscator.html)

Below is an example of various argument strings from Magic Unicorn and PowerSploit being fed into the tool. 

```
$ python argfuscator.py "powershell.exe -noprofile -windowstyle hidden -noninteractive -EncodedCommand ZQBjAGgAbwAgACIAVwBpAHoAYQByAGQAIgA="

pOwErsheLL.EXe -e^nco^d^e^dc ZQ^BjAGg^A^bw^AgA^C^IA^V^w^B^pA^H^oAYQ^B^yAG^Q^AI^g^A^= -Wi^N^do hI^dDE^N -n^OnIN^t -n^O^P^R

$ python argfuscator.py "powershell.exe -nop -wind hidden -noni -enc ZQBjAGgAbwAgACIAVwBpAHoAYQByAGQAIgA="

pOwERSHElL.Exe -encodedcommand ZQBjAGgAbwAgACIAVwBpAHoAYQByAGQAIgA= -WI^N^doWS H^I^d^DEn -n^op^rO^f -nONInTeRAcTiVe

$ python argfuscator.py "powershell.exe -nop -win hidden -noni -enc ZQBjAGgAbwAgACIAVwBpAHoAYQByAGQAIgA="

powerShELl.exe -Wi hiDDEn -n^oPRoF -ec ZQ^B^jA^G^g^A^bwAg^ACIA^VwBp^AH^o^AYQ^B^y^AGQ^AI^g^A= -NONInTeRaCTiVe

$ python argfuscator.py "powershell.exe -NoP -NonI -W Hidden -E ZQBjAGgAbwAgACIAVwBpAHoAYQByAGQAIgA="

p^O^wE^R^s^hELl.^EXe -e ZQB^jA^GgAbwAg^A^C^I^A^VwB^pA^H^o^AYQ^By^AG^QAI^gA^= -w^iN^d^o^Ws^t h^i^dD^eN -NoninteRActIv -NOprofilE
```
