import streamlit as st

quiz_page = st.Page("quiz_Year8_Science.py", title="Run Quiz", icon="🤔")
comments_page = st.Page("comments.py", title="Comment Page", icon="✒️")

pg = st.navigation([quiz_page, comments_page])
st.set_page_config(page_title="Saavi Quizzzs", page_icon="🧭")
pg.run()
