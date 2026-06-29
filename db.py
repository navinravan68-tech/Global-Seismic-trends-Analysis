from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

engine = create_engine(
    "postgresql://postgres:Navin1430@localhost:5432/earthquake_db"
)

@st.cache_data
def run_query(query):
    return pd.read_sql(query, engine)