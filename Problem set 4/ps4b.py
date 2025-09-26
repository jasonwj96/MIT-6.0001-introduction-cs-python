import string


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


def get_story_string():
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words[:]  # return copy

    def build_shift_dict(self, shift):
        shift_dict = {}
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase

        for i in range(26):
            shift_dict[lower[i]] = lower[(i + shift) % 26]
            shift_dict[upper[i]] = upper[(i + shift) % 26]
        return shift_dict

    def apply_shift(self, shift):
        shift_dict = self.build_shift_dict(shift)
        shifted_text = ""

        for char in self.message_text:
            if char in shift_dict:
                shifted_text += shift_dict[char]
            else:
                shifted_text += char
        return shifted_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        best_shift = 0
        max_real_words = 0
        best_message = ""

        for s in range(26):
            decrypted = self.apply_shift(s)
            words = decrypted.split()
            valid_count = sum([is_word(self.valid_words, w) for w in words])

            if valid_count > max_real_words:
                max_real_words = valid_count
                best_shift = s
                best_message = decrypted

        return (best_shift, best_message)


if __name__ == '__main__':
    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Decrypt story
    story_cipher = CiphertextMessage(get_story_string())
    print("Decrypted story:", story_cipher.decrypt_message())
