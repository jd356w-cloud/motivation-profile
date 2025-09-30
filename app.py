import streamlit as st
import pandas as pd

# Title
st.title("Motivation Profile")

st.write("Answer the following questions to get your motivation profile summary.")

# Define 50 placeholder questions
questions = [
    f"Question {i+1}: On a scale of 1 (low) to 5 (high), how motivated do you feel about this area?"
    for i in range(50)
]

# Store responses
responses = []

with st.form("motivation_form"):
    for i, q in enumerate(questions):
        response = st.slider(q, 1, 5, 3, key=f"q{i}")
        responses.append(response)

    submitted = st.form_submit_button("Submit")

if submitted:
    df = pd.DataFrame({
        "Question": [f"Q{i+1}" for i in range(50)],
        "Response": responses
    })

    st.write("### Your Responses")
    st.dataframe(df)

    avg_score = df["Response"].mean()
    st.write(f"**Your average motivation score is:** {avg_score:.2f} / 5")

    if avg_score >= 4:
        st.success("You are highly motivated! Keep pushing forward 🚀")
    elif avg_score >= 2.5:
        st.info("Your motivation is steady, but there’s room to grow 💡")
    else:
        st.warning("It looks like you’re struggling with motivation. Try focusing on one small win at a time 🌱")
