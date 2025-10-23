import streamlit as st
import time 
import pandas as pd 
import numpy as np 

_LOREM_IPSUM = """
Lorem Ipsum is simply dummy text of the printing and typesetting
industry. Lorem Ipsum has been the industry's standard dummy text 
ever since the 1500s, when an unknown printer took a galley 
of type and scrambled it to make a type specimen book. 
It has survived not only five centuries, but also the leap 
into electronic typesetting, remaining essentially unchanged. 
It was popularised in the 1960s with the release of Letraset 
sheets containing Lorem Ipsum passages, and more recently with 
desktop publishing software like Aldus PageMaker including 
versions of Lorem Ipsum.
"""

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.1)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

if st.button("Stream data"): #Declarar y condicionar un botón
    st.write_stream(stream_data)
