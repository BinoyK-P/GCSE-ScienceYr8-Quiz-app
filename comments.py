import streamlit as st
import sqlite3
from datetime import datetime

# --- Setup SQLite ---
DB_FILE = "comments.db"

# Create table if not exists
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        comment TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
""")
conn.commit()

st.title(':rainbow[Post your comment]')

st.write('Fill out the form below:')
with st.form('Fill in the form below:', clear_on_submit= True, enter_to_submit= False):
    u_name= st.text_input(label= 'x', placeholder= 'Your name', label_visibility= 'collapsed')
    u_comment= st.text_area(label= 'x', placeholder= 'Your comments', label_visibility= 'collapsed')
    submitted = st.form_submit_button("Submit")

# Save new comment
if u_comment:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    my_response= 'Pending'  #Yet To Respond
    c.execute("INSERT INTO comments (name, comment, timestamp) VALUES (?, ?, ?)", (u_name, u_comment, timestamp))
    conn.commit()
    st.success("Comment saved!")

# Display all comments
st.markdown("### All Comments")
c.execute("SELECT name, comment, timestamp FROM comments ORDER BY id DESC")
rows = c.fetchall()
for idx, (name, comment, ts) in enumerate(rows, 1):
    with st.container(border= True):
        col1, col2= st.columns([1, 20])
        with col1:
            st.write(f"{idx}.")
        with col2:
            st.write(f"{name} commented ({ts}):\n:violet[{comment}]")
#            if my_response != 'Pending':                                           #Coding to be done
#                st.write(f":yellow[Admin Response:] {my_response}")

conn.close()
