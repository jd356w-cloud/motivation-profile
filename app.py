import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
from fpdf import FPDF

# ----------------------------
# Survey Setup
# ----------------------------
categories = [
    "Financial Rewards",
    "Career Advancement",
    "Leadership & Influence",
    "Work-Life Balance",
    "Learning & Growth",
    "Recognition & Value",
    "Autonomy & Independence",
    "Purpose & Impact",
    "Stability & Security",
    "Team & Relationships"
]

questions = { ... }  # (Keep the same 50 questions dictionary from before)

# ----------------------------
# Streamlit App
# ----------------------------
st.title("Motivation Profile")
st.write("Answer the following questions on a scale of 1 (Not Important) to 5 (Extremely Important).")

category_scores = {}
for category, qs in questions.items():
    st.subheader(category)
    answers = [st.slider(q, 1, 5, 3) for q in qs]
    category_scores[category] = np.mean(answers)

# ----------------------------
# Charts + Report
# ----------------------------
if st.button("Generate Results"):
    st.subheader("Your Motivation Profile Results")
    df = pd.DataFrame(list(category_scores.items()), columns=["Category", "Score"])

    # ----- Bar Chart -----
    st.bar_chart(df.set_index("Category"))

    # ----- Radar Chart -----
    N = len(categories)
    values = df["Score"].tolist()
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)
    ax.set_title("Motivation Radar Profile", size=14, weight="bold", pad=20)
    st.pyplot(fig)

    # ----- Interpretation -----
    st.subheader("Your Top Motivators")
    top3 = df.sort_values(by="Score", ascending=False).head(3)
    for i, row in top3.iterrows():
        st.write(f"**{row['Category']}**: This is a key driver of your motivation with a score of {row['Score']:.1f}.")

    st.subheader("Areas of Lower Motivation")
    bottom3 = df.sort_values(by="Score", ascending=True).head(3)
    for i, row in bottom3.iterrows():
        st.write(f"**{row['Category']}**: Less of a priority right now (score {row['Score']:.1f}). May not energize you compared to other factors.")

    # ----- Export CSV -----
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="motivation_profile_results.csv",
        mime="text/csv",
    )

    # ----- Export Full PDF Report -----
    def create_pdf(dataframe, radar_fig, top3, bottom3):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Motivation Profile Report", ln=True, align="C")

        # Add bar chart
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Bar Chart of Motivation Scores", ln=True)
        buf_bar = io.BytesIO()
        dataframe.plot(kind="bar", x="Category", y="Score", legend=False).figure.savefig(buf_bar, format="png", bbox_inches="tight")
        buf_bar.seek(0)
        pdf.image(buf_bar, x=30, y=None, w=150)

        # Add radar chart
        pdf.ln(10)
        pdf.cell(200, 10, "Radar Chart of Motivation Profile", ln=True)
        buf_radar = io.BytesIO()
        radar_fig.savefig(buf_radar, format="png", bbox_inches="tight")
        buf_radar.seek(0)
        pdf.image(buf_radar, x=30, y=None, w=150)

        # Add interpretation
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Top Motivators", ln=True)
        pdf.set_font("Arial", size=12)
        for i, row in top3.iterrows():
            pdf.multi_cell(0, 10, f"- {row['Category']}: Strong driver of your motivation (Score {row['Score']:.1f})")

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Lower Motivators", ln=True)
        pdf.set_font("Arial", size=12)
        for i, row in bottom3.iterrows():
            pdf.multi_cell(0, 10, f"- {row['Category']}: Lower priority for you right now (Score {row['Score']:.1f})")

        # Output PDF
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        return pdf_buffer

    pdf_buffer = create_pdf(df, fig, top3, bottom3)
    st.download_button(
        label="Download Full PDF Report",
        data=pdf_buffer,
        file_name="motivation_profile_report.pdf",
        mime="application/pdf",
    )

