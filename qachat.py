import os 
from utills import format_sentiment
import streamlit as st
import os
import google.generativeai as genai
from utills import save_to_csv





Prompt='''Dream Interpretation:
Query: "I got accepted into an internship from a popular art museum(70s futuristic themed). I learned the ways of the museum but found out my favorite artist’s exhibition was being removed. I was sad and driven to steal my favorite artists’ merchandise from the museum’s gift shop."
Response:Dreams are highly personal and subjective, so interpretations can vary. However, I can offer a possible interpretation of your dream: The dream may reflect your desire for success and recognition in the field of art. Being accepted into the internship at a popular art museum represents your aspirations and passion for art. The 70s futuristic theme could symbolize a blend of nostalgia and forward-thinking, suggesting that you are interested in both the past and the future of art. Discovering that your favorite artist's exhibition is being removed may indicate a fear of missed opportunities or a sense of disappointment. It could symbolize a belief that something you hold dear or admire is being lost or taken away. This could reflect a fear of your own creativity, originality, or artistic expression not being valued or appreciated. The act of stealing your favorite artist's merchandise from the museum's gift shop demonstrates a conflicting desire to possess or preserve what you cherish. It may suggest a fear of losing connection to your artistic inspiration or a desire to make a personal connection with the artist's work. Overall, this dream could be indicating a mixture of ambition, disappointment, and internal conflicts regarding your artistic goals. It may be worthwhile to explore these emotions and consider how they relate to your real-life goals and aspirations in the art world.
'''





try:
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
except:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response=chat.send_message(question)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Dream Interpretation")

st.header("Dream Interpretation")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(f'This is a queary:- {input} Give me a output for this one simmilar like below mention\n {Prompt}')

    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    st.write(f"{response.text}", unsafe_allow_html=True)
    st.session_state['chat_history'].append(("Bot", f'{response.text}'))
    save_to_csv(input, response.text)

st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}", unsafe_allow_html=True)
