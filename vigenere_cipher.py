#!/usr/bin/env python3

from itertools import cycle
import string

class VigenereCipher(object):
    """Encrypt/decrypt a text using Vigenère's cipher """
    def __init__(self,language='English'):
        if language == 'English':
            self.alphabet = string.ascii_uppercase
        elif language == 'Spanish':
            self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        else:
            raise ValueError('Language must be English or Spanish')

    def _clean_text(self,text):
        """Extract the characters that belong to the alphabet"""
        clean_text = ""
        for letter in text.upper():
            if letter in self.alphabet:
                clean_text = ''.join((clean_text,letter))

        return clean_text

    def _rebuilt_text(self,text,original_text):
        """Add the characters extracted before with _clean_text() """
        rebuilt_text = list(text)
        for pos,letter in enumerate(original_text.upper()):
            if letter not in self.alphabet:
                rebuilt_text.insert(pos,letter)

        return ''.join(rebuilt_text)

    def encrypt(self,text,key):
        """Encrypt the text using Vigeneré's cipher."""
        plaintext = self._clean_text(text)
        encrypted_text = []
        for letter,keyletter in zip(plaintext.upper(),cycle(key.upper())):
            offset = self.alphabet.index(keyletter) + 1
            pos = self.alphabet.index(letter)
            encrypted_text.append(self.alphabet[(pos+offset)%len(self.alphabet)])
        encrypted_text = ''.join(encrypted_text)

        return self._rebuilt_text(encrypted_text,text)

    def decrypt(self,text,key):
        """Decrypt the text using Vigeneré's cipher."""
        ciphertext = self._clean_text(text)
        decrypted_text = []
        for letter,keyletter in zip(ciphertext.upper(),cycle(key.upper())):
            offset = self.alphabet.index(keyletter) + 1
            pos = self.alphabet.index(letter)
            decrypted_text.append(self.alphabet[(pos-offset)%len(self.alphabet)])
        decrypted_text = ''.join(decrypted_text)

        return self._rebuilt_text(decrypted_text,text)


if __name__ == '__main__':
    text = "El Índice de coincidencia es un método desarrollado por William Friendman, en 1920, para atacar cifrados de sustitución polialfabética con claves periódicas. La idea se fundamenta en analizar la variación de las frecuencias relativas de cada letra, respecto a una distribución uniforme. En un texto cifrado, no se cuenta con información suficiente para hallar tal variación. Sin embargo, se puede obtener por medio del IC. Al hacerlo, será posible aproximar el periodo de la clave. Encontrado el periodo y conociendo el algoritmo de cifrado y el lenguaje (inglés, español, ruso, etc.), se puede usar el método Kasiski para encontrar la clave."
    key = "IDC"

    text = text.upper()
    text = text.replace('Á','A')
    text = text.replace('É','E')
    text = text.replace('Í','I')
    text = text.replace('Ó','O')
    text = text.replace('Ú','U')
    text = text.replace('Ü','U')

    vigenere_spanish = VigenereCipher('Spanish')
    encrypted_text = vigenere_spanish.encrypt(text,key)
    decrypted_text = vigenere_spanish.decrypt(encrypted_text,key)

    print(encrypted_text)
    print(decrypted_text)