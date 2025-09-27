import string
from ps4a import get_permutations


### HELPER CODE ###
def load_words(file_name):
    print("Loading word list from file...")
    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


WORDLIST_FILENAME = 'words.txt'

# constants
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation):
        transpose_dict = {}
        # vowels
        for i in range(len(VOWELS_LOWER)):
            transpose_dict[VOWELS_LOWER[i]] = vowels_permutation[i]
            transpose_dict[VOWELS_UPPER[i]] = vowels_permutation[i].upper()
        # consonants
        for c in CONSONANTS_LOWER:
            transpose_dict[c] = c
        for c in CONSONANTS_UPPER:
            transpose_dict[c] = c
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        encrypted = ""
        for char in self.message_text:
            if char in transpose_dict:
                encrypted += transpose_dict[char]
            else:
                encrypted += char
        return encrypted


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        permutations = get_permutations("aeiou")
        best_decryption = self.message_text
        max_valid = 0

        for perm in permutations:
            transpose_dict = self.build_transpose_dict(perm)
            decrypted = self.apply_transpose(transpose_dict)
            words = decrypted.split()
            valid_count = sum([is_word(self.valid_words, w) for w in words])

            if valid_count > max_valid:
                max_valid = valid_count
                best_decryption = decrypted

        return best_decryption


if __name__ == '__main__':
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # More test cases
    message2 = SubMessage("Python is fun!")
    permutation2 = "uoiea"
    enc_dict2 = message2.build_transpose_dict(permutation2)
    encrypted2 = message2.apply_transpose(enc_dict2)
    print("Original:", message2.get_message_text())
    print("Encrypted:", encrypted2)
    enc_message2 = EncryptedSubMessage(encrypted2)
    print("Decrypted:", enc_message2.decrypt_message())
