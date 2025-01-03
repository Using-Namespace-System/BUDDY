# app.py

import streamlit as st
import requests

# Page layout
st.set_page_config(page_title="Interactive Writing Area", layout="wide")

st.title("Interactive Document Editing")

# Sidebar for user instructions
st.sidebar.header("Instructions")
st.sidebar.write("1. Type your document in the text area below.")
st.sidebar.write("2. Enter prompts in the prompt space to modify or generate content.")
st.sidebar.write("3. Click 'Process Prompt' to generate staged changes.")
st.sidebar.write("4. Accept or reject changes.")

# Text area for the document
document_text = st.text_area("Your Document", "Once upon a time...", height=400)

# Prompt input area
prompt_input = st.text_input("Enter your prompt", "")

# Buttons for interaction
if st.button('Process Prompt'):
    # Send document and prompt to the backend for processing
    response = requests.post("http://127.0.0.1:5000/process_prompt", json={
        'document': document_text,
        'prompt': prompt_input
    })
    
    if response.status_code == 200:
        data = response.json()
        staged_changes = data.get("staged_changes", "")
        
        if staged_changes:
            st.subheader("Suggested Changes")
            st.write(staged_changes)

            # Accept changes button
            if st.button('Accept Changes'):
                document_text += "\n" + staged_changes  # Append changes to the document
                st.write("Changes accepted.")
                
            # Refine changes button (if user wants to make further iterations)
            if st.button('Refine Changes'):
                st.write("Refining changes...")
                response = requests.post("http://127.0.0.1:5000/refine_changes", json={
                    'document': document_text,
                    'prompt': prompt_input
                })
                if response.status_code == 200:
                    refined_changes = response.json().get("staged_changes", "")
                    st.write(f"Refined Changes: {refined_changes}")

        else:
            st.write("No changes generated.")
    else:
        st.error("Error processing the prompt.")
