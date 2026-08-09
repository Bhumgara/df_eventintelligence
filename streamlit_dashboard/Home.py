import streamlit as st
from utility import api_handler as ah
import pandas as pd

# initialize session state for data
st.session_state.setdefault('data', pd.DataFrame())

left, right = st.columns([7,1])
with left:
    st.header("Gaps in the UK live music calendar")

with right:
    st.button("Refresh", on_click=st.session_state.update({'data': ah.call_api()}))