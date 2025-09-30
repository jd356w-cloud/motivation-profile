

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


# -------------------------------
# Define the 50 questions by theme
# -------------------------------
questions = {
    "Leadership": [
        "I feel confident making important decisions.",
        "I take initiative without waiting to be asked.",
        "I motivate others to perform their best.",
        "I can adapt my leadership style to the situation.",
        "I set clear goals for myself and others.",
        "I handle conflict constructively.",
        "I communicate my vision effectively.",
        "I take responsibility for outcomes.",
        "I build trust within teams.",
        "I provide constructive feedback."
    ],
    "Mindfulness": [
        "I practice being present in the moment.",
        "I manage stress effectively.",
        "I take time to reflect on my experiences.",
        "I am aware of my emotions as they arise.",
        "I can calm myself in difficult situations.",
        "I listen attentively to others.",
        "I have a regular mindfulness or meditation practice.",
        "I notice small details in my daily life.",
        "I balance work and personal life well.",
        "I show patience with myself and others."
    ],
    "Well-Being": [
        "I get enough rest and sleep regularly.",
        "I maintain a healthy diet.",
        "I exercise consistently.",
        "I feel positive about my overall health.",
        "I take time for hobbies or activities I enjoy.",
        "I nurture strong personal relationships.",
        "I feel a sense of purpose in life.",
        "I manage my workload effectively.",
        "I have strategies to recharge when tired.",
        "I feel supported by those around me."
    ],
    "Business/Strategy": [
        "I set long-term goals and work toward them.",
        "I analyze data to guide decisions.",
        "I understand financial impacts of choices.",
        "I manage resources effectively.",
        "I stay current with industry trends.",
        "I approach problems with creative solutions.",
        "I evaluate risks before acting.",
        "I delegate tasks effectively.",
        "I follow through on commitments.",
        "I measure success with clear metrics."
    ],
    "Growth & Learning": [
        "I seek out opportunities to learn.",
        "I embrace feedback to improve.",
        "I challenge myself with new experiences.",
        "I mentor or support others’ growth.",
        "I reflect on mistakes and learn from them.",
        "I stay curious and open-minded.",
        "I invest time in professional development.",
        "I track my progress over time.",
        "I celebrate small wins.",
        "I adapt quickly when facing change."
    ]
}

# -------------------------------
# Streamlit App
# -------------------------------
st.title("Motivation Profile Assessment")
st.write("Answer 50 questions to gain insight into your strengths across leadership, mindfulness, well-being, business strategy, and growth.")

responses = {}

# Collect responses
for category, qs in questions.items():
    st.header(category)
    responses[category] = []
    for q in qs:
        responses[category].append(
            st.slider(q, 1, 5, 3)  # default 3 = neutral
        )

# Process results after submission
if st.button("Generate My Profile"):
    st.subheader("Your Results")

    # Average scores by category
    results = {cat: sum(scores) / len(scores) for cat, scores in responses.items()}
    df = pd.DataFrame.from_dict(results, orient='index', columns=["Score"])

    # Bar chart
    st.bar_chart(df)

    # Radar chart
    categories = list(results.keys())
    values = list(results.values())
    values += values[:1]  # close loop

    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], categories)
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    st.pyplot(fig)

    # Simple text summary
    st.subheader("Summary")
    for cat, score in results.items():
        if score >= 4.0:
            st.write(f"**{cat}:** This is a strong area for you. Keep building on these strengths.")
        elif score >= 3.0:
            st.write(f"**{cat}:** You show balance here, but there’s room for growth.")
        else:
            st.write(f"**{cat}:** This may be a growth area. Consider strategies to strengthen this dimension.")
