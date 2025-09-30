import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi

# -----------------------------
# DATA: Categories and Questions
# -----------------------------
questions = [
    # Financial & Security
    ("Financial & Security", "Higher salary motivates me"),
    ("Financial & Security", "Would switch jobs for more pay"),
    ("Financial & Security", "Long-term job security is key"),
    ("Financial & Security", "Retirement/benefits matter"),
    ("Financial & Security", "Financial rewards = value"),
    # Recognition & Promotion
    ("Recognition & Promotion", "Promotion motivates more than pay"),
    ("Recognition & Promotion", "Recognition energizes me"),
    ("Recognition & Promotion", "Titles/recognition matter"),
    ("Recognition & Promotion", "Awards increase satisfaction"),
    ("Recognition & Promotion", "Advancement is top motivator"),
    # Leadership & Influence
    ("Leadership & Influence", "I enjoy being in charge"),
    ("Leadership & Influence", "Leading a team motivates me"),
    ("Leadership & Influence", "Influence over strategy excites me"),
    ("Leadership & Influence", "Mentoring others motivates me"),
    ("Leadership & Influence", "Seek leadership roles"),
    # Growth & Learning
    ("Growth & Learning", "Learning new skills motivates me"),
    ("Growth & Learning", "I seek professional development"),
    ("Growth & Learning", "Would trade pay for growth"),
    ("Growth & Learning", "Challenging work excites me"),
    ("Growth & Learning", "Continuous learning is vital"),
    # Purpose & Impact
    ("Purpose & Impact", "Work making a difference matters"),
    ("Purpose & Impact", "I care about societal contribution"),
    ("Purpose & Impact", "Values must align with mission"),
    ("Purpose & Impact", "Prefer purpose over pay"),
    ("Purpose & Impact", "Impact > recognition"),
    # Work-Life Balance & Flexibility
    ("Work-Life Balance & Flexibility", "Value family/personal over advancement"),
    ("Work-Life Balance & Flexibility", "Flexible hours motivate me"),
    ("Work-Life Balance & Flexibility", "Control over schedule boosts productivity"),
    ("Work-Life Balance & Flexibility", "Long hours reduce motivation"),
    ("Work-Life Balance & Flexibility", "Balance is my top priority"),
    # Relationships & Teamwork
    ("Relationships & Teamwork", "Motivated by supportive team"),
    ("Relationships & Teamwork", "Positive boss relationship is essential"),
    ("Relationships & Teamwork", "Thrive in collaboration"),
    ("Relationships & Teamwork", "Culture motivates me"),
    ("Relationships & Teamwork", "Coworker relationships matter"),
    # Autonomy & Creativity
    ("Autonomy & Creativity", "Decide how to do tasks"),
    ("Autonomy & Creativity", "Prefer innovation and creativity"),
    ("Autonomy & Creativity", "Value freedom over strict rules"),
    ("Autonomy & Creativity", "Creativity makes work fulfilling"),
    ("Autonomy & Creativity", "Motivated by independence"),
    # Achievement & Challenge
    ("Achievement & Challenge", "Enjoy setting ambitious goals"),
    ("Achievement & Challenge", "Deadlines/challenges motivate"),
    ("Achievement & Challenge", "Driven by results/targets"),
    ("Achievement & Challenge", "I like to compete"),
    ("Achievement & Challenge", "Difficult tasks > easy wins"),
    # Family & Lifestyle
    ("Family & Lifestyle", "Providing for family motivates"),
    ("Family & Lifestyle", "Career supports lifestyle"),
    ("Family & Lifestyle", "Would trade advancement for family"),
    ("Family & Lifestyle", "Family influences decisions"),
    ("Family & Lifestyle", "Lifestyle > prestige"),
]

# -----------------------------
# Scoring Guide for Dashboard
# -----------------------------
scoring_guide = {
    "Financial & Security": "Motivation driven by salary, benefits, and financial growth.",
    "Recognition & Promotion": "Motivation from promotions, status, and climbing the ladder.",
    "Leadership & Influence": "Motivation from leading teams, making decisions, and guiding others.",
    "Growth & Learning": "Motivation from training, education, and personal/professional growth.",
    "Purpose & Impact": "Motivation from mission alignment, values, and meaningful work.",
    "Work-Life Balance & Flexibility": "Motivation from having flexibility, time off, and manageable workload.",
    "Relationships & Teamwork": "Motivation from collaboration, positive culture, and relationships.",
    "Autonomy & Creativity": "Motivation from independence in tasks and decision-making.",
    "Achievement & Challenge": "Motivation from ambitious goals, challenges, and competition.",
    "Family & Lifestyle": "Motivation from family needs and lifestyle choices.",
}

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.title("Career Motivation Profile")
st.write("Answer the following questions (1 = Strongly Disagree, 5 = Strongly Agree):")

# Collect responses
responses = []
for category, question in questions:
    score = st.slider(question, 1, 5, 3)
    responses.append((category, question, score))

if st.button("Submit"):
    # Convert to DataFrame
    df = pd.DataFrame(responses, columns=["Category", "Question", "Score"])
    category_scores = df.groupby("Category")["Score"].sum().reset_index()

    # -----------------------------
    # Spider/Radar Chart
    # -----------------------------
    st.subheader("Motivation Spider Chart")
    categories = list(category_scores["Category"])
    values = list(category_scores["Score"])
    values += values[:1]  # close the loop
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], categories, color="grey", size=8)
    ax.plot(angles, values, linewidth=2, linestyle="solid")
    ax.fill(angles, values, "skyblue", alpha=0.4)
    st.pyplot(fig)

    # -----------------------------
    # Career Motivation Dashboard
    # -----------------------------
    st.subheader("Career Motivation Dashboard")
    dashboard_data = []

    for _, row in category_scores.iterrows():
        cat = row["Category"]
        score = row["Score"]

        if score <= 12:
            level = "Low"
            insight = f"Low: Less focused on {scoring_guide[cat].replace('Motivation', '').strip()}"
        elif score <= 19:
            level = "Moderate"
            insight = "Moderate: Balanced with other motivators."
        else:
            level = "High"
            insight = f"High: {scoring_guide[cat]}"

        dashboard_data.append({
            "Category": cat,
            "Description": scoring_guide[cat],
            "Score": score,
            "Level": level,
            "Insights": insight
        })

    dashboard_df = pd.DataFrame(dashboard_data)
    st.dataframe(dashboard_df)

    # -----------------------------
    # Highlight strongest motivator
    # -----------------------------
    top_row = category_scores.loc[category_scores["Score"].idxmax()]
    st.success(
        f"Your strongest motivator is **{top_row['Category']}** "
        f"with a score of {top_row['Score']}.\n\n"
        f"{scoring_guide[top_row['Category']]}"
    )
