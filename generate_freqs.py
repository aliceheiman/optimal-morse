import itertools
import nltk
from nltk.corpus import brown
from sb_corpus_reader import SBCorpusReader
import pandas as pd

# Score each sequence depending on its length
def get_length(seq):
    total = 0

    seq = "X".join(list(seq))
    seq = seq.replace(" ", "Y")
    seq = seq.replace("XYX", "Y")

    total += seq.count("*") * 1
    total += seq.count("-") * 3
    total += seq.count("X") * 1
    total += seq.count("Y") * 3

    return total


symbols = ["●", "-"]
sequences = []

for i in range(1, 6):
    sequences += ["".join(i) for i in itertools.product(symbols, repeat=i)]


lengths = []
for s in sequences:
    lengths.append((s, get_length(s)))

# sort lengths
lengths.sort(key=lambda x: x[1])

length_df = pd.DataFrame(lengths, columns=["Sequence", "Length"])
length_df = length_df.sort_values(by=["Length"], ascending=True)
length_df.to_csv("results/sequence_lengths.csv", index=False)


def get_letter_freq(word_list):
    freq_dict = {}
    freq_list = []
    total = 0

    for word in word_list:
        word = word.replace("`", "'")

        for letter in word:
            if letter not in freq_dict:
                freq_dict[letter] = 0

            total += 1
            freq_dict[letter] += 1

    freq_list = [(letter, count, count / total) for letter, count in freq_dict.items()]
    freq_df = pd.DataFrame(freq_list, columns=["Symbol", "Count", "Percentage"])
    freq_df = freq_df.sort_values(by=["Count"], ascending=False)

    return freq_df


# get swedish letter frequencies
talbanken = SBCorpusReader("data/talbanken.xml")

swedish_words = [w.lower() for w in talbanken.words()]
se_freq = get_letter_freq(swedish_words)
se_freq.to_csv("results/swedish_freq.csv", index=False)

# get english letter frequencis
brown_text = brown.words(categories=["news", "fiction", "mystery", "hobbies", "humor", "editorial"])
english_words = [w.lower() for w in brown_text]
en_freq = get_letter_freq(english_words)
en_freq.to_csv("results/english_freq.csv", index=False)
