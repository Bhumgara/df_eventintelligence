import streamlit as st
import pandas as pd
import pathlib
import sys

print("then:", sys.path[0])
import pathlib
filepath = pathlib.Path(__file__).parent.parent.resolve()
sys.path.insert(0, filepath)

print("now:", sys.path[0])
print (filepath)

from utility import api_handler as ah

# initialize session state for data
@st.fragment(None)
def init_data():
    st.session_state.setdefault('data', pd.DataFrame())
@st.fragment(None)
def update_data():
    st.session_state.update({'data': ah.update_ticketmaster_data()})


def main():
    init_data()

    # ----- Page title & headers -----
    logo, left, right = st.columns([2,5,2])
    with logo:
        st.image("eventintelligence-logo.png", width=300)

    with left:
        st.write("# Gaps in the UK live music calendar")

    with right:
        st.button("Refresh", on_click=update_data, key="GenreRefreshBt")


    st.write("---")
    st.write("### Notes on data limitations")
    st.write(
        "- This analysis uses Ticketmaster festival events and the summer from May through August. ",
        "\n",
        "- A quiet weekend on Ticketmaster may still host events ticketed through other platforms (Skiddle, Eventbrite, direct box office). Low count is a signal, not proof of absence. ",
        "\n",
        "- The festival-keyword filter catches common naming patterns but will miss festivals with non-obvious names. Check gap candidates against known festival directories before concluding.",
        "\n",
        "- A lot of events have no genres associated"
    )

if __name__ == "__main__":
    main()