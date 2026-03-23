import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

from src.dkt_data_prep import load_assistments, build_sequences, encode_sequences
from src.skill_encoder import build_skill_map, build_skill_lookup
from src.knowledge_map import build_knowledge_map
from src.gap_detector import detect_gaps
from src.recommender import recommend_topics
from src.auto_graph import build_auto_knowledge_graph
from src.predict import load_model, predict_student_knowledge
from src.adaptive_recommender import recommend_next_skills

st.title("AI Learning Gap Detector")

# Load dataset
df = load_assistments("data/assistments.csv")

# Build sequences
sequences = build_sequences(df)


# Skill mapping
skill_map = build_skill_map(df)
num_skills = len(skill_map)
model = load_model(num_skills)

# Encode sequences
encoded = encode_sequences(sequences, skill_map)

predicted_knowledge = predict_student_knowledge(
    model, 
    encoded, 
    num_skills
)

skill_lookup = build_skill_lookup(df)


# Knowledge map
knowledge = build_knowledge_map(encoded)

# Auto knowledge graph
knowledge_graph = build_auto_knowledge_graph(sequences)

# Student selector
students = list(knowledge.keys())
selected_student = st.selectbox(
    "Select Student",
    students
)

student_probs = predicted_knowledge[selected_student]

student_knowledge = {
    skill: student_probs[skill]
    for skill in range(len(student_probs))
}

st.header("Student Knowledge")

# Radar chart
skills = []
values = []

sorted_skills = sorted(student_knowledge.items(), key = lambda x: x[1])

for skill, prob in sorted_skills:
    if skill not in skill_lookup:
        continue
    
    name = skill_lookup[skill]
    
    skills.append(name)
    values.append(prob)
    
    if len(skills) >= 8:
        break
    

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=skills,
    fill='toself'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    showlegend=False
)
st.plotly_chart(fig)


# Learning gaps
st.header("Learning Gaps")
gaps = detect_gaps(student_knowledge)
for g in gaps:
    name = skill_lookup.get(g, f"Skill {g}")
    st.warning(name)


# Recommendations
st.header("Recommendations")
recs = recommend_topics(gaps, skill_lookup)
for r in recs:
    st.write("-", r)
    
# Next Best Skills to Practice
st.header("Next Best Skills to Practice")

next_skills = recommend_next_skills(
    student_knowledge,
    skill_lookup,
    top_k=5
)
for skill in next_skills:
    st.info(
        f"{skill['skill_name']}  (mastery: {skill['mastery']})"
    )


# Knowledge graph visualization
st.header("Knowledge Graph")

G = nx.DiGraph()

selected_skills = list(student_knowledge.keys())[:8]
for skill in selected_skills:
    if skill not in knowledge_graph:
        continue

    deps = knowledge_graph[skill]

    for d in deps:
        if skill in skill_lookup and d in skill_lookup:

            name_a = skill_lookup[skill]
            name_b = skill_lookup[d]

            G.add_edge(name_b, name_a)  # prerequisite → skill


fig2 = plt.figure(figsize=(8,6))

pos = nx.kamada_kawai_layout(G)
node_colors = []

for node in G.nodes():
    if node in skills:  # skills из radar chart
        node_colors.append("red")
    else:
        node_colors.append("#87CEEB")


nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=2500,
    font_size=9,
    edge_color="gray",
    arrows=True
)

plt.title("Skill Dependency Graph")

st.pyplot(fig2)