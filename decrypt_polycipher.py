#!/usr/bin/env python3

import sys
from operator import itemgetter
from itertools import zip_longest
import string
import logging as log
import argparse
from collections import Counter
from math import gcd

## TODO
# sanitaze input

def cleanText(text):
    """ Removes the punctuation symbol, digits and whitespaces from text """
    cleantext = text
    chars_to_removed = [string.punctuation,string.whitespace,string.digits,'—']
    chars_to_removed = ''.join(chars_to_removed)
    for c in chars_to_removed:
        cleantext = cleantext.replace(c,'')
    return cleantext

def isValidCipherText(text):
    """ Returns if a text only contains ascii uppercase letters """
    text_upper = text.upper()
    for letter in text_upper:
        if not letter in string.ascii_uppercase:
            return False
    else:
        return True

def rebuildText(originaltext,newtext):
    """ Adds the punctuation symbol, whitespaces and digits from originaltext to newtext

    Example
        rebuildText('ifmmp1!','hello')
        hello!
    """
    rebuilt_text = list(newtext)
    for pos,letter in enumerate(originaltext):
        if letter in string.punctuation or letter in string.whitespace or letter in string.digits:
            rebuilt_text.insert(pos,letter)
    return ''.join(rebuilt_text)

def getNgrams(text):
    """ Gets the n-grams that are repeated in the text.
    The output is a list of list where each (sub)list
    contains all the grams of the same length
    that are repeated and its occurrences.
    The list and each (sub)list are sorted in reversed order
    with respect to the length and the number of occurrences.

    Example:
        >>> getNgrams("abcxabc)
        [[('abc', 2)], [('ab', 2), ('bc', 2)], [('a', 2), ('b', 2), ('c', 2)]]
    """
    ngrams = []
    for j in range(3,int(len(text)/2+1)):
        jgrams = {}
        for i in range(len(text)-j+1):
            currentgram = text[i:i+j]
            jgrams[currentgram] = jgrams.get(currentgram,0) + 1
        for k,v in list(jgrams.items()): # removes the jgrams that aren't repeated
            if v == 1:
                del jgrams[k]
        if jgrams:
            ngrams.append( sorted(jgrams.items(), key=itemgetter(1), reverse=True) )
        else:
            break

    return list(reversed(ngrams))

def KasiskiMethod(text, ngrams):
    """Calculates the possible periods of a polyalphabetic substitution ciphers
    using Kasiski's method.
    """
    distances = []
    possible_periods = []
    for ngram in ngrams:
        first_occcurrence = text.find(ngram)
        second_occcurrence = text.find(ngram,first_occcurrence+1)
        distance = second_occcurrence-first_occcurrence
        distances.append(distance)
        log.debug('Distance of %s: %s-%s=%s',ngram,second_occcurrence,first_occcurrence,distance)

        for possible_period in range(2,distance+1):
            if distance % possible_period == 0:
                possible_periods.append(possible_period)

    return possible_periods, distances

def indexOfCoincidence(text):
    """Calculates the index of coincidence of text normalized"""
    frequency_of_letters = Counter(text)
    ic = 0
    n = len(text)
    for f in frequency_of_letters.values():
        ic +=  (f*(f-1))/(n*(n-1))

    return float("{0:.6f}".format(ic))

def averageIndexOfCoincidece(text,period):
    """Calculates the indices of coincidence of subsequences of the text
    and computes the average. The i-subsequence is calculated
    joining the letters i+0*period,i+1*period,i+2*period,...

    For example, if period=2 and text="defendtheeastwallcastle":
        subsequence1 = dfnteatalate
        subsequence2 = eedheswlcsl
    """

    subsequences = [[] for i in range(period)]
    for pos,letter in enumerate(text):
        subsequences[pos%period].append(letter)

    subseq_ics = []
    for index,subseq in enumerate(subsequences):
        ic = indexOfCoincidence(subseq)
        subseq_ics.append(ic)
        log.debug('(period=%s) Subsequence %s: %s',period, index,''.join(subseq))
        log.debug('(period=%s) IC: %s',period, ic)

    avg_ic = sum(subseq_ics)/period

    return float("{0:.6f}".format(avg_ic))

def elementClosestToValue(elements, value, returns_position=True):
    """ Returns the element (or the position in the list) in elements that
    is closest to value. If more than one element are at the minimum distance
    to value, it returns the first one. If returns_position=False, it returns
    the element.

    Example:
        >>> elementClosestToValue([1,2,3], 1.8)
        2
        >>> elementClosestToValue([1,2,4,6], 3)
        2
    """
    distances_repect_value = ["{0:.6f}".format(abs(element-value)) for element in elements]
    min_value = min(distances_repect_value)
    min_index = distances_repect_value.index(min_value)

    #log.debug('Distances respect value: %s',distances_repect_value)
    #log.debug('Element closest to %s is elements[%s]=%s',value,min_index,elements[min_index])

    if returns_position:
        return min_index
    else:
        return elements[min_index]


def guessPeriod(periods_with_occurrences,period_closest_english_ic,period_closest_ciphertext_ic):
    """ Calculates the confidence/probability of each period of having been used for
    encrypt the text. It uses the periods obtained with the Kasiski method, the
    period closest to the English ic and the period closest to the ciphertext ic
    to compute the confidence.
    """

    periods = [period for period,_ in periods_with_occurrences]
    occurrences = [occurrences for _,occurrences in periods_with_occurrences]
    total_occurrences = sum(occurrences)
    log.debug('Total occurrences of all guessed periods: %s',total_occurrences)

    periods_with_confidence = []
    for period,occurrences in periods_with_occurrences:
        confidence = 70*occurrences/total_occurrences
        periods_with_confidence.append( [period,confidence] )
    log.debug('Periods with their confidence using Kasiski: %s', periods_with_confidence)

    pos_element_closest = elementClosestToValue(periods, period_closest_english_ic)
    periods_with_confidence[pos_element_closest][1] += 20
    log.debug('Periods with their confidence using Kasiski and language IC: %s', periods_with_confidence)

    pos_element_closest = elementClosestToValue(periods, period_closest_ciphertext_ic)
    periods_with_confidence[pos_element_closest][1] += 10
    periods_with_confidence.sort(key=itemgetter(1),reverse=True)
    log.debug('Periods with their confidence using Kasiski,language IC and period IC: %s', periods_with_confidence)

    periods_with_confidence = [(period,"{0:.2f}%".format(confidence)) for period,confidence in periods_with_confidence]

    return periods_with_confidence

def decryptText(text,period,manual=False,spanish=False):
    """ Decrypts the text for a given period. For each subsequence
    split using the period, the letter with the highest probability
    (computed using the most common letters)
    is replaced with the letter E and the key is obtained
    (supposing the cipher is Vigenère's).
    It supposes that the ciphertext is in English by default.
    If manual is True, the user can choose the
    encryption of the letter E (which determine the
    decryption of the whole subsequence)
    """
    log.debug('Using period %s to decrypt',period)

    subsequences = [[] for i in range(period)]
    for pos,letter in enumerate(text):
        subsequences[pos%period].append(letter)

    keyword = ""
    alphabet = string.ascii_uppercase
    subsequences = [''.join(subseq) for subseq in subsequences]
    subsequences_decrypted = ['' for i in range(len(subsequences))]
    for index, subseq in enumerate(subsequences):
        frequency_of_letters = Counter(subseq)
        most_common_letters = frequency_of_letters.most_common(5)
        most_common_letters.sort(key=itemgetter(1,0),reverse=True)

        log.debug('(subseq=%s) Encrypted subsequence: %s',index,subseq)

        most_common_letters_of_language = "ETAOI" if spanish == False else "EAOSR"
        encryptions_of_e = []
        for index_letter,letter in enumerate(most_common_letters):
            encrypted_e = most_common_letters[index_letter][0]
            offset = (ord(encrypted_e) - ord('E'))%len(alphabet)
            matches = 0
            for letter in most_common_letters:
                pos = alphabet.index(letter[0])
                if alphabet[(pos-offset)%len(alphabet)] in most_common_letters_of_language:
                    matches += 1
            encryptions_of_e.append((encrypted_e,matches))
        encryptions_of_e.sort(key=itemgetter(1),reverse=True)
        total_matches = sum([matches for letter,matches in encryptions_of_e])
        encryptions_of_e = [(letter,"{0:.2f}%".format(100*matches/total_matches)) for letter,matches in encryptions_of_e]


        if manual:
            log.info('Possible encryptions of E with their confidence: %s',encryptions_of_e)
            while True:
                encrypted_e = input("\nEncryption of E: ").upper()
                if encrypted_e in string.ascii_letters:
                    break
                else:
                    log.warning("Bad character found. Type a letter.")
            print()
        else:
            log.debug('(subseq=%s) Possible encryptions of E with their confidence: %s',index, encryptions_of_e)
            encrypted_e = encryptions_of_e[0][0]

        offset = (ord(encrypted_e) - ord('E'))%len(alphabet)
        log.debug('(subseq=%s) Supposing Enc(E) = %s', index, encrypted_e)

        ## cipher = vigener
        keyletter = chr(ord('A')+offset-1)
        if manual:
             log.info('Subsequence %s. Key: %s', index, keyletter)
        else:
            log.debug('(subseq=%s) Keyletter: %s <-> %s', index, keyletter, offset)

        subseq_deciphered = subseq
        for pos, letter in enumerate(alphabet):
            #log.debug('Enc(%s) = %s',alphabet[(pos-offset)%len(alphabet)],letter)
            subseq_deciphered = subseq_deciphered.replace(letter,alphabet[(pos-offset)%len(alphabet)].lower())

        log.debug('(subseq=%s) Decrypted subsequence: %s',index,subseq_deciphered)
        subsequences_decrypted[index] = subseq_deciphered
        keyword += keyletter

    subsequences_decrypted_mixed = zip_longest(*subsequences_decrypted,fillvalue='')
    subsequences_decrypted_mixed = [''.join(subseq_mix) for subseq_mix in subsequences_decrypted_mixed]

    plaintext = ''.join(subsequences_decrypted_mixed)

    return keyword, plaintext


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="decrypt a polyalphabetic substitution ciphered text")
    parser.add_argument("-m", "--manual", action="store_true", help="interacts with the user")
    parser.add_argument("-spa", "--spanish", action="store_true", help="suppose the ciphertext is in Spanish (English by default")
    parser.add_argument("-i", "--input-file", type=str, help="the input file with the encrypted text")
    parser.add_argument("-o","--output-file", type=str, help="the output file with the decrypted text")
    parser.add_argument("-nc", "--no-colors", action="store_true", help="don't color the output")
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        banner = "Note: if you want to read/write from/to a file, print more information or interact "   \
            + "with the decryption, use command-line arguments. For more information, type:"    \
            + "\n\n\tpython3 " + sys.argv[0] + " --help\n"
        print(banner)

    if args.verbosity:
        if not args.no_colors:
            log.addLevelName( log.INFO, "\033[1;36m%s\033[1;0m" % log.getLevelName(log.INFO))
            log.addLevelName( log.WARNING, "\033[1;31m%s\033[1;0m" % log.getLevelName(log.WARNING))
            log.addLevelName( log.DEBUG, "\033[1;33m%s\033[1;0m" % log.getLevelName(log.DEBUG))
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    else:
        if not args.no_colors:
            log.addLevelName( log.INFO, "\033[1;36m%s\033[1;0m" % log.getLevelName(log.INFO))
            log.addLevelName( log.WARNING, "\033[1;31m%s\033[1;0m" % log.getLevelName(log.WARNING))
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)

    if args.input_file:
        log.info('Getting encrypted text from %s',args.input_file)
        with open(args.input_file) as filehandler:
            ciphertext = filehandler.read()
    else:
        ciphertext = input("Introduce the ciphertext: ")
        print()

    log.debug('Ciphertext: %s',ciphertext)
    clean_ciphertext = cleanText(ciphertext).upper()
    log.debug('Clean ciphertext: %s',clean_ciphertext)

    if not isValidCipherText(clean_ciphertext):
        log.warning("The ciphertext contains strange characters. Aborting...")
        sys.exit(1)

    ngrams = getNgrams(clean_ciphertext)
    log.debug('All n-grams: %s',ngrams)

    if not ngrams:
        log.warning("Kasiski's method failed: no ngrams (n>=3) found. Aborting...")
        sys.exit(1)

    all_possible_periods = []
    for jgrams in ngrams:
        jgrams_without_occurrences = [jgram[0] for jgram in jgrams]
        possible_periods, distances = KasiskiMethod(clean_ciphertext,jgrams_without_occurrences)
        all_possible_periods +=possible_periods

        j = len(jgrams_without_occurrences[0])
        log.debug('(n-grams, n=%s) Distances: %s',j,distances)
        log.debug('(n-grams, n=%s) Possible periods: %s',j,possible_periods)

    all_possible_periods = Counter(all_possible_periods).most_common(5)
    if all_possible_periods[0][1] == 1:
        log.warning("Kasiski's method failed: insufficient ngrams. Aborting...")
        sys.exit(1)

    periods_to_remove = []
    for period in all_possible_periods:
        if period[1] == 1:
            periods_to_remove.append(period)

    if len(all_possible_periods) - len(periods_to_remove) >= 5:
        for period in periods_to_remove:
            all_possible_periods.remove(period)
    log.debug('Most common periods with their occurrences: %s',all_possible_periods)

    all_possible_periods_without_occurrences = [a_p_p[0] for a_p_p in all_possible_periods]
    log.info("Periods guessed using Kasiski's Method %s",all_possible_periods_without_occurrences)

    avg_ics = []
    for period in all_possible_periods_without_occurrences:
        avg_ics.append(averageIndexOfCoincidece(clean_ciphertext,period))
    log.debug('Average IC values for each guessed period: %s',avg_ics)

    language_ic = 0.66895 if not args.spanish else 0.0
    language = 'English' if not args.spanish else 'Spanish'
    log.debug('%s IC: %s',language, language_ic)

    pos_element_closest = elementClosestToValue(avg_ics, language_ic)
    period_closest_english_ic = all_possible_periods_without_occurrences[pos_element_closest]
    log.info('Period with closest IC to %s IC: %s',language, period_closest_english_ic)

    ciphertext_ic = indexOfCoincidence(clean_ciphertext)
    log.debug('Ciphertext IC: %s',ciphertext_ic)

    periods_ic = [0.0066,0.0520,0.0473,0.0450,0.0436,0.0427,0.0420,0.0415,0.0411,0.0408,
        0.0405,0.0403,0.0402,0.0400,0.0399,0.0397,0.0396,0.0396,0.0395,0.0394 ]
    log.debug('IC related to periods from 1 to 20: %s',periods_ic)

    pos_element_closest = elementClosestToValue(periods_ic, ciphertext_ic)
    period_closest_ciphertext_ic = pos_element_closest+1
    log.info('Period with closest IC to ciphertext IC: %s', period_closest_ciphertext_ic)

    periods_with_confidence = guessPeriod(all_possible_periods,period_closest_english_ic,period_closest_ciphertext_ic)
    log.info('Periods with their confidence: %s', periods_with_confidence)

    if not args.manual:
        guessed_period = periods_with_confidence[0][0]
        key, plaintext = decryptText(clean_ciphertext,guessed_period,spanish=args.spanish)
        plaintext = rebuildText(ciphertext,plaintext)
        log.debug('Key: %s',key)
        log.debug('Decrypted text: %s',plaintext)

    else:
        while True:
            while True:
                try:
                    guessed_period = int(input("\nIntroduce period: "))
                except ValueError:
                    log.warning("Bad character found. Type a number")
                    continue
                break
            print()

            key, plaintext = decryptText(clean_ciphertext,guessed_period,manual=True, spanish=args.spanish)
            plaintext = rebuildText(ciphertext,plaintext)

            log.info('Key: %s',key)
            log.info('Decrypted text: %s',plaintext)

            option = input("\nTry again [y/N]: ")
            if not option.upper() == 'Y':
                break

    print("--------------")
    log.info('Key: %s',key)
    if args.output_file:
        log.info('Saving decrypted text in %s.',args.output_file)
        with open(args.output_file,'w') as filehandler:
            filehandler.write('Key: ' + key)
            filehandler.write('\n==========\n')
            filehandler.write(plaintext)
    else:
        log.info('Decrypted text: %s',plaintext)
