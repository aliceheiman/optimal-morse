import streamlit as st
import itertools

header = st.container()
body = st.container()

with header:
    st.title("Optimizing Morse for Swedish")


# SEQUENCES
symbols = ["*", "-"]
sequences = []

for i in range(1, 6):
    sequences += ["".join(i) for i in itertools.product(symbols, repeat=i)]

# Score each sequence depending on its length
def compute_length(sequence):
    