import sys
import argparse
from crack_vigenere import CrackVigenere
from period_polialphabetic_cipher import PolialphabeticCipher

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="crack a Vigenère's cipher")
    parser.add_argument("-m", "--manual", action="store_true",
                                        help="interacts with the user")
    parser.add_argument("-spa", "--spanish", action="store_true",
                                            help="suppose the ciphertext is in Spanish")
    parser.add_argument("-i", "--input-file", type=str,
                                            help="the input file with the encrypted text")
    parser.add_argument("-o","--output-file", type=str,
                                            help="the output file with the decrypted text")
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        print("If you want to:\n"
                "\t- Read/write from/to a file.\n"
                "\t- Interact with the decryption process.\n"
                "\t- Decrypt texts that are in Spanish (English by default).\n"
                "use command-line arguments. For more information, type:\n"
                "\tpython3 " + sys.argv[0] + " --help\n")

    if args.input_file:
        print('Getting encrypted text from: ' + args.input_file)
        with open(args.input_file) as filehandler:
            ciphertext = filehandler.read()
    else:
        ciphertext = input("Introduce the ciphertext: ")

    if args.spanish:
        language = "Spanish"
    else:
        language = "English"

    if not args.manual:
        periods = PolialphabeticCipher(ciphertext,language).guess_period()
        period = periods[0][0]
        key, plaintext = CrackVigenere(ciphertext,language).decrypt_text(period)
    else:
        periods = PolialphabeticCipher(ciphertext,language).guess_period()
        while True:
            print("Possible periods: {0}".format(periods))
            try:
                period = int(input("Introduce period: "))
            except ValueError:
                log.warning("Bad character found. Type a number")
                continue
            print()

            key, plaintext = CrackVigenere(ciphertext,language).decrypt_text(period,
                                                                                                manual=args.manual)
            print("Key: {0}\n{1}...".format(key,plaintext[:1000]))

            option = input("\nTry again [y/N]: ")
            if not option.upper() == 'Y':
                break

    if args.output_file:
        print('Saving key and decrypted text in: ' + args.output_file)
        with open(args.output_file,'w') as filehandler:
            filehandler.write('Key: ' + key + '\n')
            filehandler.write(plaintext)
    else:
        print("Key: " + key)
        print(plaintext)
