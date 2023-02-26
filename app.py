import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import math

# nltk.download("brown")

###################################
# FUNCTIONS
###################################


def altair_bar_chart(df, x_name, y_name):
    c = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(x_name, sort=None),
            y=y_name,
        )
    )

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

with header:
    st.title("Optimizing Morse for Swedish")

with body:
    se_alphabet
    st.table(se_freq)

    altair_bar_chart(se_freq, "Symbol", "Percentage")
    altair_bar_chart(seq_len, "Sequence", "Length")

    st.table(optimal_se)
