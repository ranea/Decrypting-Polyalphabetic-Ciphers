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

The attack in automatic mode only works with big texts.
If you have a short text, you will have to use the option *--manual*

### Automatic attack

Suppose we encrypt the speech of Martin Luther King *I have a dream*
using Vigenère's cipher with the key *LUTHER*.
We have used [Sharky's Vigenere Cipher](http://sharkysoft.com/vigenere/)
but you can use whatever tool you want as long as it keeps
non-alphabet characters and it isn't case sensitive.

Let's try to decrypt:

    $ python3 decrypt_polycipher.py -i ihaveadream_encrypted.txt -o ihaveadream_decrypted.txt
    INFO: Getting encrypted text from ihaveadream_encrypted.txt
    INFO: Periods guessed using Kasiski's Method [2, 3, 6, 4, 12]
    INFO: Period with closest IC to English IC: 12
    INFO: Period with closest IC to ciphertext IC: 6
    INFO: Periods with confidence: [(6, '32.19%'), (12, '23.72%'), (2, '17.69%'), (3, '17.42%'), (4, '8.98%')]
    INFO: Key: LUTHER
    INFO: Saving decrypted text in ihaveadream_decrypted.txt.

We have obtained the correct key and the decrypted text is in the file *ihaveadream_decrypted.txt*.

### Manual attack

Suppose we encrypt the monologue *Tears in Rain* from *Blade Runner*:

    I've seen things you people wouldn't believe.
    Attack ships on fire off the shoulder of Orion.
    I watched C-beams glitter in the dark near the Tannhäuser Gate.
    All those moments will be lost in time, like tears...in...rain.
    Time to die.

We encrypt it using Vigenère's cipher with the key ROY and we obtain:

    A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd.
    Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc.
    H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwätktq Ypsw.
    Pkd igghd edlwcsk lhda aw anki hf ihet, kazd ltzjh...hf...gzac.
    Sabd ld cat.

If we try the automatic decryption:

    $ python3 decrypt_polycipher.py
    Introduce the ciphertext: A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd. Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc. H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwätktq Ypsw. Pkd igghd edlwcsk lhda aw anki hf ihet, kazd ltzjh...hf...gzac. Sabd ld cat.

    INFO: Periods guessed using Kasiski's Method [5, 2, 3, 4, 6]
    INFO: Period with closest IC to English IC: 3
    INFO: Period with closest IC to ciphertext IC: 2
    INFO: Periods with confidence: [(3, '30.77%'), (2, '26.15%'), (5, '21.54%'), (4, '10.77%'), (6, '10.77%')]
    INFO: Key: RRY
    INFO: Decrypted text: i'se sben qhikgs vou meomle touidn'q beiiese. aqtazk seipp on cirb ofc thb shlulaer lf ooiok. i wxtceed z-bexms dliqteo in qhe aarh nexr tee txnneÄbsuy gqae. qsl jooil metedas mplb ie bvsj pn jpmu, sial tuhri...pn...hhid. aicl te kiu.

It failed. However, we can guess that the beggining must be *I've*, so we have to change the second
monoalphabetic cipher (the second letter of the key).

If the letter *K* from the ciphertext correspond to the letter *V* in the plainletter,
the letter *E* must be encrypted to *T*.

We add the argument *--manual** to interact with the decryption:

    $ python3 decrypt_polycipher.py -m
    Introduce the ciphertext: A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd. Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc. H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwätktq Ypsw. Pkd igghd edlwcsk lhda aw anki hf ihet, kazd ltzjh...hf...gzac. Sabd ld cat.

    INFO: Periods guessed using Kasiski's Method [5, 2, 3, 4, 6]
    INFO: Period with closest IC to English IC: 3
    INFO: Period with closest IC to ciphertext IC: 2
    INFO: Periods with confidence: [(3, '30.77%'), (2, '26.15%'), (5, '21.54%'), (4, '10.77%'), (6, '10.77%')]

    Introduce period: 3

    INFO: Subsequence 0. Most common letters: [('W', 7), ('K', 6), ('S', 5), ('H', 5), ('F', 5)]

    Encryption of E: W

    INFO: Subsequence 0. Key: R <-> 18
    INFO: Subsequence 1. Most common letters: [('W', 7), ('A', 6), ('K', 5), ('I', 5), ('E', 4)]

    Encryption of E: T

    INFO: Subsequence 1. Key: O <-> 15
    INFO: Subsequence 2. Most common letters: [('D', 9), ('H', 8), ('T', 5), ('S', 4), ('N', 4)]

    Encryption of E: D

    INFO: Subsequence 2. Key: Y <-> 25
    INFO: Key: ROY
    INFO: Decrypted text: i've seen things you people wouldn't believe. attack ships on fire off the shoulder of orion. i watched c-beams glitter in the dark near the tannhÄbvuy jqah. qso joril pethdav mpob ih bvvj pq jppu, slal wuhui...pq...hhld. alcl we klu.

    Try another period [y/N]: N

We can see now why the automatic mode failed. The letter which *E* must be encrypted to
usually is the most common letter in the subsequence but in this case that doesn't applied.

## Support

Only English and Vigenère's cipher are supported.
Soon other languages and polyalphabetic ciphers will be added.
