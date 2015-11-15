# Decrypting-polyalphabetic-ciphers
Decrypting polyalphabetic ciphers using Kasiski's Method and Index of Coincidence

## Usage

    usage: decrypt_polycipher.py [-h] [-m] [-i INPUT_FILE] [-o OUTPUT_FILE] [-nc]
                                 [-v]

    decrypt a polyalphabetic substitution ciphered text

    optional arguments:
      -h, --help            show this help message and exit
      -m, --manual          interacts with the user
      -i INPUT_FILE, --input-file INPUT_FILE
                            the input file with the encrypted text
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            the output file with the decrypted text
      -nc, --no-colors      don't color the output
      -v, --verbosity       increase output verbosity

## Example

The attack in automatic mode only works with big texts. If you have a short text, you will have to use the option *--manual*

Suppose we encrypt the first chapter of 1984 using Vigenère's cipher with the key ORWELL.
We have used [CrypTool-Online](http://www.cryptool-online.org/index.php?option=com_cto&view=tool&Itemid=99&lang=en) with the options:
- Encrypt
- Keep non-alphabet characters
- Parse alphabet >>> Upper case

Let's try to decrypt:

    >>> python3 decrypt_polycipher.py -i 1984_chapter1_encrypted.txt -o output.txt
    INFO: Getting encrypted text from 1984_chapter1_encrypted.txt
    INFO: Periods guessed using Kasiski's Method [2, 3, 6, 4, 12]
    INFO: Period with closest IC to English IC: 12
    INFO: Period with closest IC to ciphertext IC: 5
    INFO: Periods with confidence: [(6, '32.43%'), (12, '23.10%'), (2, '18.19%'), (3, '17.79%'), (4, '8.49%')]
    INFO: Key: ORWELL
    INFO: Saving decrypted text in output.txt.

We have obtained the key and the decrypted text is in output.txt.


## Support

Only English and Vigenère's cipher are supported.
Soon other languages and polyalphabetic ciphers will be added.
