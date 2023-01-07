
import sys
import re


# main() is used to initialize the decipher program.
def main():
    ciphertext, n = read_command_line_args()
    bigram_plaintext_dict, word_count_dict = plaintext_bigram_word_count()
    bigram_ciphertext_dict = ciphertext_bigram_count(ciphertext)
    freq_plaintext = frequent_bigrams(n, bigram_plaintext_dict)
    freq_ciphertext = frequent_bigrams(n, bigram_ciphertext_dict)
    
    cipher_word = input("\nInput: ")
    while cipher_word != "":
        deciphered_words = decipher_word(cipher_word, freq_ciphertext, 
                                         freq_plaintext)
        print_ordered_output(deciphered_words, word_count_dict)
        cipher_word = input("\n\nInput: ")
        
    return


# Arguments from the command line will be assigned to an object and passed.
def read_command_line_args():
    
    n = 3
    ciphertext = sys.argv[1]
    if len(sys.argv) == 3:
        n = sys.argv[2]
    
    return ciphertext, n


# The wells.txt will be opened and all non-alpahbetic characters will be removed
# from the text and split into a list. All overlapping bigrams are counted and
# put into a dictionary while all words are also counted and put into a dictionary.
def plaintext_bigram_word_count():
    bigram_count_dict = {}
    word_count_dict = {}
    file = open("wells.txt", "r")
    text = file.read().lower()
    text = re.sub("[-';,.\"14035?89_2:()!]", "", text)
    word_list = text.split()
 
    for word in word_list:
        word_count_dict[word] = word_count_dict.setdefault(word, 0) + 1
        for i in range(len(word) - 1):
            bi_gram = word[i] + word[i+1]
            if " " not in bi_gram:
                bigram_count_dict[bi_gram] = bigram_count_dict.setdefault(bi_gram, 0) + 1
    
    file.close()
    return bigram_count_dict, word_count_dict


# All non-overlapping bigrams are counted from the ciphertext provided by the user
# and are coounted and placed in a dictionary.
def ciphertext_bigram_count(ciphertext):
    bigram_count_dict = {}
    file = open(ciphertext, "r")
    text = file.read()
    for i in range(0, len(text) - 1, 2):
        bi_gram = text[i] + text[i + 1]
        bi_gram = bi_gram.lower()
        bigram_count_dict[bi_gram] = bigram_count_dict.setdefault(bi_gram, 0) + 1
        
    file.close()
    return bigram_count_dict


# The values from the dictionary are sorted from highest to least. Based on the N
# value, the keys from the N highest values are placed into an ordered list.
def frequent_bigrams(n, bigram_dictionary):
    values_list = sorted(bigram_dictionary.values(), reverse = True)
    frequent_bigram_list = []
    for i in range(n):
        value = values_list[i]
        for key in bigram_dictionary:
            if bigram_dictionary[key] == value:
                frequent_bigram_list.append(key)
    
    return frequent_bigram_list
 
            
# The cipher_word will be deciphered using regular expressions by replacing 
# bigrams found in the ciphere text with plaintext bigrams that are mapped to
# the most frequent ciphertext bigrams. A list of possible words will be returned.
def decipher_word(cipher_word, cipher_bigrams, plaintext_bigrams):
    split_cipher = split_word(cipher_word)

    for i in range(len(cipher_bigrams)):
        bigram = cipher_bigrams[i].upper()
        re1 = ".*?" + bigram + ".*?"
        if re.match(re1, split_cipher):
            split_cipher = re.sub(bigram, plaintext_bigrams[i], split_cipher)

    cipher_word = split_cipher.split("/")
    cipher_word = "".join(cipher_word)
                        
    deciphered_words = find_words(cipher_word)
    if cipher_word[-2:].isupper():
        cipher_word = cipher_word[:-1]
        deciphered_words_odd = find_words(cipher_word)
        deciphered_words = deciphered_words + deciphered_words_odd
        
    return deciphered_words


# The ciphertext's bigrams will be split with "/" in order to subsitiute the
# bigrams properly.
def split_word(cipher_word):
    split_cipher_word = "/"
    for i in range(0, len(cipher_word) - 1, 2):
        bigram = cipher_word[i] + cipher_word[i + 1] + "/"
        split_cipher_word += bigram
    return split_cipher_word
 
               
# Possible words will be found using regular expressions to match words, found in
# the wordlist, to the ciphertext.
def find_words(partial_cipher):
    partial_cipher = partial_cipher + "$"
    partial_cipher = re.sub("[A-Z]", ".", partial_cipher)
    word_list = []
    file = open("wordlist.txt", "r")    
    
    for line in file:
        if re.match(partial_cipher, line[:-1]):
            word_list.append(line[:-1])
    
    file.close()                       
    return word_list

# The count of the words found are extracted from the word_count_dictionary.
# The counts are sorted highest to lowest and the sort_words() function sorts them.
# The words are then outputed on a single line.
def print_ordered_output(word_list, word_count_dict):
    count_list = []
    tuple_word_list = []
    for word in word_list:
        word_count = word_count_dict.get(word, 0)
        count_list.append(word_count)
        tuple_word_list.append((word, word_count))
    count_list = sorted(count_list, reverse = True)
    sorted_word_list = sort_words(count_list, tuple_word_list)
    
    print("\nOutput: ", end = "")
    for word in sorted_word_list:
        print("%s " % word, end = "")

# Based of a sorted count list and a list of tuples, consisting of the words and
# their counts, the words are sorted into a list based on that count.
# Any similar counts are sorted alphabetically.
def sort_words(count_list, tuple_word_list):
    sorted_word_list = []
    rev_count_list = remove_duplicates(count_list)
    for count in rev_count_list:
        if count_list.count(count) == 1:
            for word_tuple in tuple_word_list:
                if word_tuple[1] == count:
                    sorted_word_list.append(word_tuple[0])
        else:
            equivelant_count_words = []
            for word_tuple in tuple_word_list:
                if word_tuple[1] == count:
                    equivelant_count_words.append(word_tuple[0])
            equivelant_count_words = sorted(equivelant_count_words)
            sorted_word_list = sorted_word_list + equivelant_count_words
    return sorted_word_list

# All duplicated counts are removed form the givin list and passed as a new list.
def remove_duplicates(count_list):
    rev_count_list = []
    for count in count_list:
        if count not in rev_count_list:
            rev_count_list.append(count)
    return rev_count_list
                
                       
if __name__ == "__main__":
    main()
    
