import streamlit as st
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

pagetitle = "Musikerkennung42069"

st.set_page_config(layout="wide", page_title=pagetitle, page_icon=":headphones:")
st.write(f"# {pagetitle}")
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Teach Songs", "Recognize Songs", "About"])
col1, col2 = st.columns([0.5, 0.5])
with col1:
    if option == "Teach Songs":
        st.write("## Teach new Songs")
        with st.container(border=True):
            selected_file = st.file_uploader("Upload file to teach song", type=["mp3", "wav"], accept_multiple_files=False)
            if selected_file is not None:
                st.audio(selected_file, format='audio/wav')
            
        with st.form(key='teach_songs', border=True):
            title = st.text_input("Title")
            artist = st.text_input("Artist")
            album = st.text_input("Album")
            if st.form_submit_button('Add to Library'):          

                if selected_file is not None:
                
                    print(selected_file.name) #debug
                    #Insert logic to save to database here. 
                    #file has to be fingerprinted, id and hashes have to be stored in the database

                    st.success("Song added to library") #somehow this does not work
                    st.rerun()
                else:
                    st.error("Must upload a file to teach a song.")
                     

    elif option == "Recognize Songs":
        st.write("## Recognize Songs from Snippet")
        with st.container(border=True):
            selected_snippet = st.file_uploader("Upload file to recognize song", type=["mp3", "wav"])
            if selected_snippet is not None:
                st.audio(selected_snippet, format='audio/wav')
            if st.button('Recognize'):
                #Insert logic to recognize song here
                #file has to be fingerprinted, hashes have to be compared to the database
                #if a match is found, the song has to be displayed
                #song info should be read from a separate table in the database
                #if no match is found, an error message has to be displayed
                print("Recognizing song...") #debug
                #if not found:
                st.error("No matches found, either teach the song or upload a different snippet.")
                #else:
                st.success("Song recognized") 

        with st.container(border=True):
            st.write("## Recognize from recording")
            if st.button('Start Recording'):
                #function to record audio from microphone and save it in recording.wav
                #st.write("Recording complete")
                st.audio('recording.wav', format='audio/wav')
                #insert logic to recognize song from recording here
                #file has to be fingerprinted, hashes have to be compared to the database
                #if a match is found, the song has to be displayed
                #song info should be read from a separate table in the database
                #if no match is found, an error message has to be displayed
                print ("Recognizing song from recording...") #debug
                #if found:
                print("Song recognized") #debug
                #else:
                print("Song ID not found in the database.")#debug

    else :
        st.write(f"## About {pagetitle}")
        st.write(f"{pagetitle} is a song recognition app that uses audio fingerprinting to recognize songs. It uses the Fingerprinting algorithm from the existing project abracadabra to generate hashes from audio files and stores them in a database. When a snippet is uploaded, it generates hashes from the snippet and compares them to the database to find a match. It can also record audio from the microphone and recognize songs from it.")
        st.write(f"{pagetitle} has been developed by Pavlo Slyvka, Vella Nedelcheva and Benedikt Reimeir as a final project for the course Softwaredesign at the MCI Innsbruck.")

with col2:
    st.write("Include Output, History and Song Info here")






