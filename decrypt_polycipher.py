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
# only vigenere cipher supported -> generalize

def cleanText(text):
    """ Removes the punctuation symbol and whitespaces from text """
    cleantext = text
    chars_to_removed = string.punctuation + string.whitespace
    for c in chars_to_removed:
        cleantext = cleantext.replace(c,'')
    return cleantext

def getNgrams(text):
    """ Gets the n-grams that are repeated in the text.
    The output is a list of list where each (sub)list
    contains all the grams of the same length
    that are repeated and its occcurrences.
    The list and each (sub)list are sorted in reversed order
    with respect to the length and the number of occcurrences.

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
    log.debug('Frequency of letters: %s', frequency_of_letters)
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

    for index,subseq in enumerate(subsequences):
        log.debug('(p=%s) subsequence %s: %s',period, index,''.join(subseq))

    avg_ic = sum( [indexOfCoincidence(subseq) for subseq in subsequences] )/period

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

    log.debug('Distances respect value: %s',distances_repect_value)
    log.debug('Element closest to %s is elements[%s]=%s',value,min_index,elements[min_index])

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
    log.debug('Total occcurrences: %s',total_occurrences)

    periods_with_confidence = []
    for period,occurrences in periods_with_occurrences:
        confidence = 90*occurrences/total_occurrences
        periods_with_confidence.append( [period,confidence] )
    log.debug('(step=1) Periods with confidence: %s', periods_with_confidence)

    pos_element_closest = elementClosestToValue(periods, period_closest_english_ic)
    periods_with_confidence[pos_element_closest][1] += 5
    periods_with_confidence.sort(key=itemgetter(1),reverse=True)
    log.debug('(step=2) Periods with confidence: %s', periods_with_confidence)

    pos_element_closest = elementClosestToValue(periods, period_closest_ciphertext_ic)
    periods_with_confidence[pos_element_closest][1] += 5
    periods_with_confidence.sort(key=itemgetter(1),reverse=True)
    log.debug('(step=3) Periods with confidence: %s', periods_with_confidence)

    periods_with_confidence = [(period,"{0:.2f}%".format(confidence)) for period,confidence in periods_with_confidence]

    return periods_with_confidence

def decryptText(text,period,manual=False):
    """ Decrypts the text for a given period. For each subsequence
    splited usign the period, the most common letter
    is replaced with the letter E and the key is obtained
    (supposing the cipher is Vigenère's)
    """

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
        most_common_letter = most_common_letters[0][0]

        log.debug('Encrypted subsequence %s: %s',index,subseq)

        if manual:
            log.info('Subsequence %s. Most common letters: %s',index,most_common_letters)
            print()
            encrypted_e = input("Letter used to encrypt E: ").upper()
            print()
        else:
            encrypted_e = most_common_letter
            log.debug('(subsequence=%s) most common letters: %s',index,most_common_letters)

        offset = (ord(encrypted_e) - ord('E'))%len(alphabet)
        log.debug('Supposing Enc(E) = %s', encrypted_e)

        ## cipher = vigener
        keyletter = chr(ord('A')+offset)
        if manual:
             log.info('Subsequence %s. Key: %s <-> %s', index, keyletter, offset)
        else:
            log.debug('Keyletter: %s <-> %s', keyletter, offset)

        subseq_deciphered = subseq
        for pos, letter in enumerate(alphabet):
            log.debug('Enc(%s) = %s',alphabet[(pos-offset)%len(alphabet)],letter)
            subseq_deciphered = subseq_deciphered.replace(letter,alphabet[(pos-offset)%len(alphabet)].lower())

        ## cipher = substitution
        # most_common_english_letter = "etrinoa"
        # n = len(most_common_english_letter)
        # for cipherletter_with_occurrences,plainletter in zip(frequency_of_letters.most_common(n),most_common_english_letter):
        #     subseq = subseq.replace(cipherletter_with_occurrences[0] , plainletter)

        log.debug('Decrypted subsequence %s: %s',index,subseq_deciphered)
        subsequences_decrypted[index] = subseq_deciphered
        keyword += keyletter

    subsequences_decrypted_mixed = zip_longest(*subsequences_decrypted,fillvalue='')
    subsequences_decrypted_mixed = [''.join(subseq_mix) for subseq_mix in subsequences_decrypted_mixed]

    plaintext = ''.join(subsequences_decrypted_mixed)

    return keyword, plaintext


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="decrypt a polyalphabetic substitution ciphered text")
    parser.add_argument("-m", "--manual", action="store_true", help="interacts with the user")
    parser.add_argument("-i", "--input-file", type=str, help="the input file with the encrypted text")
    parser.add_argument("-o","--output-file", type=str, help="the output file with the decrypted text")
    parser.add_argument("-nc", "--no-colors", action="store_true", help="don't color the output")
    parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    if not args.manual and not args.verbosity and not args.input_file and not args.output_file:
        banner = "Note: if you want to read/write from/to a file, print more information or interact  \
        \nwith the decryption, use command-line arguments. For more information, type: \
        \n\n\tpython3 " + sys.argv[0] + " --help\n"
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
        log.info('Getting encrypted text from %s.',args.input_file)
        with open(args.input_file) as filehandler:
            ciphertext = filehandler.read()
    else:
        ciphertext = input("Introduce the ciphertext: ")
        print()

    log.debug('Ciphertext: %s',ciphertext)
    clean_ciphertext = cleanText(ciphertext).upper()
    log.debug('Clean ciphertext: %s',clean_ciphertext)

    ngrams = getNgrams(clean_ciphertext)
    log.debug('n-grams: %s',ngrams)

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

    for k,v in all_possible_periods: # remove possible periods that have only one occurrence
        if v == 1:
            del all_possible_periods[k]
    log.debug('Periods with more occurrences as a factor of distances of ngrams: %s...',all_possible_periods)

    all_possible_periods_without_occurrences = [a_p_p[0] for a_p_p in all_possible_periods]
    log.info("Periods guessed using Kasiski's Method %s",all_possible_periods_without_occurrences)

    avg_ics = []
    for period in all_possible_periods_without_occurrences:
        avg_ics.append(averageIndexOfCoincidece(clean_ciphertext,period))
    log.debug('Average IC values: %s',avg_ics)

    english_ic = 0.66895
    log.debug('English IC: %s',english_ic)

    pos_element_closest = elementClosestToValue(avg_ics, english_ic)
    period_closest_english_ic = all_possible_periods_without_occurrences[pos_element_closest]
    log.info('Period with closest IC to English IC: %s',period_closest_english_ic)

    ciphertext_ic = indexOfCoincidence(clean_ciphertext)
    log.debug('Ciphertext IC: %s',ciphertext_ic)

    periods_ic = [0.0066,0.0520,0.0473,0.0450,0.0436,0.0427,0.0420,0.0415,0.0411,0.0408,
        0.0405,0.0403,0.0402,0.0400,0.0399,0.0397,0.0396,0.0396,0.0395,0.0394 ]
    log.debug('Periods IC: %s',periods_ic)

    pos_element_closest = elementClosestToValue(periods_ic, ciphertext_ic)
    period_closest_ciphertext_ic = pos_element_closest+1
    log.info('Period with closest IC to ciphertext IC: %s', period_closest_ciphertext_ic)

    periods_with_confidence = guessPeriod(all_possible_periods,period_closest_english_ic,period_closest_ciphertext_ic)
    log.info('Periods with confidence: %s', periods_with_confidence)

    if not args.manual:
        guessed_period = periods_with_confidence[0][0]
        key, plaintext = decryptText(clean_ciphertext,guessed_period)
        log.debug('Key: %s',key)
        log.debug('Decrypted text: %s',plaintext)
    else:
        while True:
            print()
            guessed_period = int(input("Introduce period: "))
            print()
            key, plaintext = decryptText(clean_ciphertext,guessed_period,manual=True)

            log.info('Key: %s',key)
            log.info('Decrypted text: %s',plaintext)

            print()
            option = input("Try another period [y/N]: ")
            if not option.upper() == 'Y':
                break

    if args.output_file:
        log.info('Saving decrypted text in %s.',args.output_file)
        with open(args.output_file,'w') as filehandler:
            filehandler.write('Key: ' + key)
            filehandler.write('\nPlaintext: ' + plaintext)
    else:
        log.info('Key: %s',key)
        log.info('Decrypted text: %s',plaintext)
