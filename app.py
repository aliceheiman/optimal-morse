import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import math

# nltk.download("brown")

###################################
# FUNCTIONS
###################################


def altair_bar_chart(df, x_name, y_name, title="", out_file=None):
    c = alt.Chart(df).mark_bar().encode(x=alt.X(x_name, sort=None), y=y_name)
    c.title = title

    if out_file:
        print("here")
        c.save(out_file, scale_factor=2.0)

    st.altair_chart(c)


###################################
# SETUP
###################################
morse_dict = {
    "A": "*-",
    "B": "-***",
    "C": "-*-*",
    "D": "-**",
    "E": "*",
    "F": "**-*",
    "G": "--*",
    "H": "****",
    "I": "**",
    "J": "*---",
    "K": "-*-",
    "L": "*-**",
    "M": "--",
    "N": "-*",
    "O": "---",
    "P": "*--*",
    "Q": "--*-",
    "R": "*-*",
    "S": "***",
    "T": "-",
    "U": "**-",
    "V": "***-",
    "W": "*--",
    "X": "-**-",
    "Y": "-*--",
    "Z": "--**",
}

morse_dict = {k: " ".join(list(v)) for k, v in morse_dict.items()}
morse_dict = {k: v.replace("*", "●") for k, v in morse_dict.items()}
morse_dict = {k: v.replace("-", "▄") for k, v in morse_dict.items()}

en_alphabet = ("".join(morse_dict.keys())).lower()
se_alphabet = en_alphabet + "åäö"

en_freq = pd.read_csv("results/english_freq.csv")
se_freq = pd.read_csv("results/swedish_freq.csv")
seq_len = pd.read_csv("results/sequence_lengths.csv")

seq_len["Sequence"] = seq_len["Sequence"].apply(lambda s: " ".join(list(s)))
seq_len["Sequence"] = seq_len["Sequence"].apply(lambda s: s.replace("*", "●"))
seq_len["Sequence"] = seq_len["Sequence"].apply(lambda s: s.replace("-", "▄"))

# filter DataFrames to only include alhabet
en_freq = en_freq[en_freq["Symbol"].isin(list(en_alphabet))]
se_freq = se_freq[se_freq["Symbol"].isin(list(se_alphabet))]

en_freq = en_freq.reset_index(drop=True)
se_freq = se_freq.reset_index(drop=True)

# only take the first n sequences
seq_len = seq_len.head(len(se_alphabet))

# map letters to shortest sequences
en_letters = en_freq["Symbol"].tolist()
se_letters = se_freq["Symbol"].tolist()
seq_list = seq_len["Sequence"].tolist()

# seq_list = [" ".join(s) for s in seq_list]
# seq_list = [s.replace("*", "●") for s in seq_list]
# seq_list = [s.replace("-", "▄") for s in seq_list]

optimal_en = [(let, seq) for let, seq in zip(en_letters, seq_list)]
optimal_se = [(let, seq) for let, seq in zip(se_letters, seq_list)]

optimal_en = pd.DataFrame(optimal_en, columns=["Letter", "Sequence"])
optimal_se = pd.DataFrame(optimal_se, columns=["Letter", "Sequence"])

###################################
# Create dictionaries of freqs
###################################
dict_en = optimal_en.sort_values("Letter")
dict_en = dict(zip(dict_en["Letter"], dict_en["Sequence"]))

dict_se = optimal_se.sort_values("Letter")
dict_se = dict(zip(dict_se["Letter"], dict_se["Sequence"]))

###################################
# Generate chart images
###################################


def generate_morse_chart(chart_dict, x_dim=1200, y_dim=1600, out_file="test.png"):

    # import fonts
    fontLet = ImageFont.truetype("fonts/NotoSansJP-Bold.otf", size=80)
    fontSeq = ImageFont.truetype("fonts/NotoSansJP-Bold.otf", size=40)

    # set up
    img = Image.new("RGB", (x_dim, y_dim), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    x = x_start = 200
    y = y_start = 50

    # create chart
    i = 0
    for letter, sequence in chart_dict.items():
        if i == math.ceil(len(chart_dict) / 2):
            x += 500
            y = y_start

        # Write letter
        d.text((x, y), letter.upper(), fill=(0, 0, 0), font=fontLet)

        # Move over
        x += 80
        y += 35

        # Write sequence
        d.text((x, y), sequence, fill=(0, 0, 0), font=fontSeq)

        # Move back and down
        x -= 80
        y += 80

        i += 1

    img.save(out_file)


# generate_morse_chart(dict_en, x_dim=1200, y_dim=1600, out_file="results/en_optimal.png")
# generate_morse_chart(dict_se, x_dim=1200, y_dim=1830, out_file="results/se_optimal.png")

###################################
# PRESENTATION
###################################

# PAGE PARTS
header = st.container()
body = st.container()
footer = st.container()

with header:
    st.title("Optimizing Morse for Swedish")

with body:

    st.write("The Morse Code maps each letter to a sequence of dots and dashes.")
    st.write(
        "How do you determine which sequence each letter should receive? If you think about it, you would probably want the most common letters to have shorter sequences, and the letters that are not used that much to get the longer sequences."
    )
    st.write("This is roughly what morse code does. Have a look at the chart:")

    st.image("results/en_original.png")

    st.write(
        "I used the NLTK Brown dataset to determine the English letter frequency. By counting how many different letters there are in that corpus, we get the following graph:"
    )
    altair_bar_chart(en_freq, "Symbol", "Count", "Letter Frequencies in the English Language")

    st.write(
        "As you can see, 'E' and 'T' are the most common letters, and it is precisely those two letters who claim the shortest sequences of 'dot' and 'dash' respectively."
    )

    st.write(
        "Now, we can analyze how far this goes. But to do this, we need a way of counting the the total length of every possible sequence."
    )

    st.write(
        "In Morse, the length is always relative to the 'dot' which is defined to be one unit. All lengths are defined as follows:"
    )
    st.markdown(
        """
        * Dot: 1 
        * Dash: 3
        * Intra-character space: 1
        * Inter-character space: 3
        * Word space: 7
    """
    )

    st.write(
        "The intra-character space is the pause between dots and dashes within the *same* character. Inter-character space is the pause between characters."
    )

    st.write("So to compute the total length of a sequence, let's consider the following: ● ● ▄ ●")

    st.write("In total, we have 3 dots, 1 dash, and 3 intra-character spaces. This sums up to: ")
    st.latex(r"3 \cdot 1 + 1 \cdot 3 + 3 \cdot 1 = 9")
    st.write("In short, it has a length of **9 units**.")

    st.write(
        "Generating a list of all possible combinations and computing their length, we can graph the sequences with shortest to longset sequence lengths."
    )
    altair_bar_chart(seq_len, "Sequence", "Length", "Morse Sequence Sorted by Transmission Length")

    st.write(
        "From this graph, we can map the most frequent letters to the sequences with shortest lengths, thus making them fastest to transmit."
    )
    st.write("If we apply this technique to the English language, we get a different Morse Code chart.")

    st.image("results/en_optimal.png")

    st.write("Notice how this alphabet contains many more 'dots' than the original.")

    st.write("Armed with this knowledge, we can apply the same technique to the Swedish language.")
    st.write(
        "I performed a similar letter frequency analysis using the Python NLTK library and Språkbankens corpus 'talbanken' together with their python module 'sb-nltk-tools'."
    )

    altair_bar_chart(se_freq, "Symbol", "Count", "Letter Frequencies in the Swedish Language")

    st.write(
        "Notice that this time, the letters 'e a r n t' are most common. Mapping the Swedish letter frequencies to their respective optimal sequence we get the following new chart:"
    )

    st.image("results/se_optimal.png")

with footer:
    st.header("Conclusion")
    st.write(
        "In short, optimizing Morse Code for different languages could have radical differences depending on the letter frequencies. The optimal French Morse Code would most probably be very different that the German one."
    )
    st.write(
        "To note, however, is that the Morse Code is adapted to languages with the Latin Alphabet. Future work could therefore look into Morse Code adaptations to languages with other alphabets."
    )
    st.write(
        "Moreover, although shorter sequences may optimize for transmission time, they can be more confusing for a human to transcribe because it is harder to differentiate between long sequences of 'dits'. Therefore, one might want to change the 'optimal target' by weighing in both length and internal variation to help humans quickly recognize what they are hearing."
    )
    st.write(
        "And of course, as the current Morse Code is already adopted and learned, it is very unprobable to use this new alhpabet. Nonetheless, it is an example of the thinking behind the creation of future communication schemes."
    )
    st.write("Thank you for reading! Take care 😀")

    st.header("References")
    st.markdown(
        """
    * Phillips, S.C. (no date) Morse code timing, Morse Code Timing | Morse Code World. Available at: https://morsecode.world/international/timing.html (Accessed: February 26, 2023). 
    * Språkbanken Github | Spraakbanken/SB-NLTK-tools: Tools for using Språkbanken resources with NLTK, GitHub. Språkbanken. Available at: https://github.com/spraakbanken/sb-nltk-tools (Accessed: February 26, 2023). 
    * TalbankenSBX | Språkbanken Text. Språkbanken. Available at: https://spraakbanken.gu.se/en/resources/talbanken (Accessed: February 26, 2023).
    """
    )
