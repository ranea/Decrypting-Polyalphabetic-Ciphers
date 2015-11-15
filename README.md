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

### Automatic attack

The attack in automatic mode only works with big texts.
If you have a short text, you will have to use the option *--manual*

Suppose we encrypt the speech of Marthin Luther King *I have a dream*
using Vigenère's cipher with the key *LUTHER*.
We have used [Sharky's Vigenere Cipher](http://sharkysoft.com/vigenere/)
but you can use whatever tool you want as long as it keeps
non-alphabet characters and it isn't case sensitive.

Let's try to decrypt:

    >>> python3 decrypt_polycipher.py -i ihaveadream_encrypted.txt -o ihaveadream_decrypted.txt
    INFO: Getting encrypted text from ihaveadream_encrypted.txt
    INFO: Periods guessed using Kasiski's Method [2, 3, 6, 4, 12]
    INFO: Period with closest IC to English IC: 12
    INFO: Period with closest IC to ciphertext IC: 6
    INFO: Periods with confidence: [(6, '32.19%'), (12, '23.72%'), (2, '17.69%'), (3, '17.42%'), (4, '8.98%')]
    INFO: Key: LUTHER
    INFO: Saving decrypted text in ihaveadream_decrypted.txt.

We have obtained the correct key and the decrypted text is in the file ihaveadream_decrypted.txt.

### Manual attack

...

## Support

Only English and Vigenère's cipher are supported.
Soon other languages and polyalphabetic ciphers will be added.
