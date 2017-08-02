# Decrypting Polyalphabetic Ciphers

Decrypting polyalphabetic ciphers using Kasiski's Method and Index of Coincidence.

The report [informe.pdf](../blob/master/informe.pdf) (in spanish) explains in details the implementation and contains several examples showing all the funcionalities of the program.

## Usage

    $ python3 main.py --help
    usage: main.py [-h] [-m] [-spa] [-i INPUT_FILE] [-o OUTPUT_FILE]

    crack a Vigenère's cipher

    optional arguments:
        -h, --help          show this help message and exit
        -m, --manual        interacts with the user
        -spa, --spanish     suppose the ciphertext is in Spanish
        -i INPUT_FILE, --input-file INPUT_FILE
                            the input file with the encrypted text
        -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            the output file with the decrypted text


## Example

The automatic decryption of small texts may not work. In this case, the text can be decrypted using the *manual mode* which requieres some interaction with the user.


### Automatic mode

Suppose we encrypt the monologue *Tears in Rain*

    I've seen things you people wouldn't believe.
    Attack ships on fire off the shoulder of Orion.
    I watched C-beams glitter in the dark near the Tannhauser Gate.
    All those moments will be lost in time, like tears...in...rain.
    Time to die.


using Vigenère's cipher with the key *ROY* (using *vigenere_cipher.py*).

    A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd.
    Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc.
    H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwzmhdj Vzlt.
    Zda szdrw bnetmlh vaak tt kghs ac sabd, dxjw idsgr...ac...qsxm.
    Lxlw in vxd.


Let's try to decrypt:

    [adrian@archPC trabajo]\$ python3 main.py
    If you want to:
        - Read/write from/to a file.
        - Interact with the decryption process.
        - Decrypt texts that are in Spanish (English by default).
    use command-line arguments. For more information, type:
        python3 main.py --help

    Introduce the ciphertext: A'kd ktdf igacfk nnm edgekw lnmacf'i
    awahwkd. Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc. H opsuwdv
    R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwzmhdj Vzlt. Zda szdrw
    bnetmlh vaak tt kghs ac sabd, dxjw idsgr...ac...qsxm. Lxlw in vxd.


The program decrypts the ciphertext successfully:

    Key: ROY

    i've seen things you people wouldn't believe. attack ships on
    fire off the shoulder of orion. i watched c-beams glitter in the
    dark near the tannhauser gate. all those moments will be lost
    in time, like tears...in...rain. time to die.


### Manual mode

Please see the report [informe.pdf](../blob/master/informe.pdf).
