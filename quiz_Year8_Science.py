import streamlit as st
import pandas as pd
import random
    
# ====Set layout
st.set_page_config(
    page_title= 'Saavi Quizzzzs',
    page_icon= '👧',
    layout= 'centered',
    initial_sidebar_state= 'expanded'
)
# ==========

# ===== Global CSS to reduce vertical spacing between markdown widgets=====
st.markdown("""
    <style>
    
    /* Reduce gap between vertical elements */
    div[data-testid="stVerticalBlock"] {
        gap: 0.25rem; /* Default is ~1rem */

    </style>
""", unsafe_allow_html=True)
# ============

st.sidebar.header(':rainbow[Welcome!]')
mytext= (
    'This is the first Web App created by me. I must admit that the quest of my '
    'schoolgoing granddaughters Saavi and Shlokaa to learn and raise questions '
    'inspired me for undertaking this experiment. I hope that the App will not '
    'only be helpful in furthering their reading interests '
    'but also will help many others in learning process.'
)
st.sidebar.markdown(f"#####  :gray[{mytext}]")
st.sidebar.write('---')
st.sidebar.markdown(':yellow[DISCLAIMER]')
mytext= (
    'This App is in tests & trial stage. '
    'All efforts have been made for compiling correct information; '
    'however, no guarantee is given for accuracy of the information. '
    'It is advised that the text book may be consulted in case of any doubt. '
    'Any comments from users for correction / improvement in the information is WELCOME; '
    'it will be apprecited if you post your comments regarding the same '
    '(navigate to :blue[comments] tab for posting comments).'
)
st.sidebar.markdown(f"######  :yellow[{mytext}] \n:orange[Thanks for your attention!]")

# Find number of chapters and chapter names from file 'Q_and_A.xlsx' and store them only once during the session
if 'chapters_list' not in st.session_state:
    df_full= pd.read_excel('./DATA/Q_and_A.xlsx')
    chapters= df_full['Chapter'].unique().tolist()
    chapters.sort()
    if 'df_full' not in st.session_state:
        st.session_state.df_full = df_full
    if 'chapters' not in st.session_state:
        st.session_state.chapters= chapters
    st.session_state.chapters_list= 'prepared'
    
st.markdown('### 🦄 :rainbow[Multiple Choice Quiz (GCSE Year-8 Science)]')

# Disaablity Controls for radio buttons
def lock_radio(): 
    st.session_state.locked= True
def unlock_radio():
    st.session_state.locked= False

# Disaablity Controls for Submit Answer button
def lock_SA_button():
    st.session_state.sa_locked= True
def unlock_SA_button():
    st.session_state.sa_locked= False
    
# Disaablity Controls for Next Question button
def lock_NQ_button():
    st.session_state.nq_locked= True
def unlock_NQ_button():
    st.session_state.nq_locked= False

def chapter_changed():
    # Initialisaes the session state variables on change in Selectbox
    if 'Q_list' in st.session_state:
        del st.session_state.Q_list
    if 'chap_complete' in st.session_state:
        del st.session_state.chap_complete
    st.session_state.q_total= 0
    st.session_state.Q_num_index= 0
    st.session_state.btn_SA_pressed= False
    st.session_state.correct_count= 0
    st.session_state.incorrect_count= 0
    unlock_radio()
    unlock_SA_button()
    lock_NQ_button()

# Select a chapter
col1, col2, col3 = st.columns([60,15,25])    #to adjust width of selectbox to 50% of parent width
with col1:
    chapter = st.selectbox(label = ':blue[Select chapter:]',
        options = st.session_state.chapters,
        index = 0,
        on_change= chapter_changed,
        width = 'stretch'
        )

    chap_text = f'Chapter: {chapter}'
    st.markdown(f'#####      :blue[{chap_text}]')

# Select JPG image for the chapter
chap_image = "./JPG/" + chapter + ".jpg"
with col2:
    try:
        st.image(image= chap_image, caption=None, width= 'content')
    except:
        st.image(image= "./JPG/default.jpg", caption=None, width= 'content')

# Load questions for the chapter
if 'Q_list' not in st.session_state:
    condition = st.session_state.df_full['Chapter'] == chapter
    df_filtered= st.session_state.df_full[condition].copy()
    st.session_state.q_total = len(df_filtered)
    st.session_state.questions = df_filtered
    st.session_state.rnd_nums = random.sample(range(0, st.session_state.q_total), st.session_state.q_total)
    st.session_state.Q_list = 'prepared'
    
# Initialise correct_count
if 'correct_count' not in st.session_state:
    st.session_state.correct_count= 0
if 'incorrect_count' not in st.session_state:
    st.session_state.incorrect_count= 0

# Display question
if 'Q_num_index' not in st.session_state:
    st.session_state.Q_num_index= 0

QNo = st.session_state.Q_num_index + 1
iRow = st.session_state.rnd_nums[st.session_state.Q_num_index]
question = st.session_state.questions.iloc[iRow,2]
opt1 = st.session_state.questions.iloc[iRow,3]
opt2 = st.session_state.questions.iloc[iRow,4]
opt3 = st.session_state.questions.iloc[iRow,5]
opt4 = st.session_state.questions.iloc[iRow,6]
answer = st.session_state.questions.iloc[iRow,7]
st.markdown(f"###### 👉Q{QNo}: {question}")
options = [opt1, opt2, opt3, opt4]

match answer:
    case 1:
        correct_answer= opt1
    case 2:
        correct_answer= opt2
    case 3:
        correct_answer= opt3
    case 4:
        correct_answer= opt4
    
col_X, col_Y = st.columns([5, 95])

with col_Y:
    # Show the answers in a radio group
    st.markdown("<p style='margin-left:0px; color: orange; font-size: 1.0em;'><br>Choose your answer from below:</p>", unsafe_allow_html=True)

    # Initalise a variable to control whether the radio group is locked or unlocked
    if 'locked' not in st.session_state:
        st.session_state.locked= False     #the radio group is unlocked in the first run
    
    # Initalise a variable to control whether the submit button is locked or unlocked
    if 'sa_locked' not in st.session_state:
        st.session_state.sa_locked= False     #the Submit button is unlocked in the first run

    #Initalise a variable to control whether the Next Question button is locked or unlocked
    if 'nq_locked' not in st.session_state:
        st.session_state.nq_locked= True     #the Next Question button is locked in the first run

    choice = st.radio(
        "Hide this", options, key= 'radio_choice',
        disabled= st.session_state.locked,          #lock the radio grooup on choosing an option
        label_visibility= "collapsed",
        index= 0
        )

# # Initialize a variable to flag end of chapter
if 'chap_complete' not in st.session_state:
    st.session_state.chap_complete = False

# Create Submit and NextQuestion buttons
col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    # Initialise a state variable btn_SA_pressed with value False
    if 'btn_SA_pressed' not in st.session_state:
        st.session_state.btn_SA_pressed= False
    with st.container(horizontal= True, horizontal_alignment= 'center'):
        if st.button("Submit answer" , key= 'btn_SA', disabled= st.session_state.sa_locked,
                     help= 'Click to check your answer'):
            st.session_state.btn_SA_pressed= True
            if choice == correct_answer:
                st.session_state.correct_count += 1
            else:
                st.session_state.incorrect_count += 1
            if st.session_state.Q_num_index < st.session_state.q_total - 1:
                lock_SA_button()
                lock_radio()
                unlock_NQ_button()
                st.rerun()
            if st.session_state.Q_num_index == (st.session_state.q_total - 1):
                lock_radio()
                lock_SA_button()
                lock_NQ_button()
                st.session_state.chap_complete = True
                st.rerun()
with col2:
    with st.container(horizontal= True, horizontal_alignment= 'center'):
        if st.button(f"Next Question", key= 'btn_NQ', disabled= st.session_state.nq_locked,
                     help= 'Click to get the next question in the chapter'):
            if st.session_state.btn_SA_pressed:
                st.session_state.btn_SA_pressed= False
            unlock_SA_button()
            unlock_radio()
            lock_NQ_button()
            
            if st.session_state.Q_num_index < (st.session_state.q_total - 1):
                st.session_state.Q_num_index += 1
                st.rerun()
                           
if st.session_state.btn_SA_pressed:
    if choice == correct_answer:
        st.markdown("✅ Correct!", width= 500)
    else:
        st.markdown(f"❌ Wrong!<br>Correct answer: :green[{correct_answer}]", width= 500, unsafe_allow_html=True)
ans_ok= st.session_state.correct_count
ans_notok= st.session_state.incorrect_count
#st.write('Q_index=', st.session_state.Q_num_index)
#st.write('Ok=', ans_ok, 'Not-Ok=', ans_notok)
col_1, co_2= st.columns([6, 4])    #to adjust widths
with col_1:
    with st.container(border= True, width= 'stretch'):
        st.write(f"Your cumulative score for this chapter: {ans_ok}/{len(st.session_state.questions)}")
        col_3, col_4 = st.columns([2,3])
        with col_3:
            st.markdown(":blue[Chapter progress:]")
        with col_4:
            progress = int(((ans_ok + ans_notok)/len(st.session_state.questions))*100)
            st.progress(progress)
            
if st.session_state.chap_complete:
    st.balloons()
    st.toast('All questions in the chapter covered.\nYou may select another chapter if you want to continue with the quiz.')
          
