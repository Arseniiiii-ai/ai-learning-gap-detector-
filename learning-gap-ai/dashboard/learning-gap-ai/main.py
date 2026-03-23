import pandas as pd

from src.dkt_data_prep import load_assistments, build_sequences, encode_sequences
from src.skill_encoder import build_skill_map
from src.dkt_dataset import build_dkt_dataset
from src.knowledge_map import build_knowledge_map
from src.gap_detector import detect_gaps
from src.recommender import recommend_topics
from src.skill_encoder import build_skill_lookup
from src.auto_graph import build_auto_knowledge_graph

def run_pipeline():

    print("\nLoading dataset...")
    
    df = load_assistments("data/assistments.csv")
    print("Dataset loaded:", len(df), "rows")
    
    skill_lookup = build_skill_lookup(df)
    print("\nBuilding student sequences...")

    sequences = build_sequences(df)
    knowledge_graph = build_auto_knowledge_graph(sequences)
    print("\nAuto knowledge graph example:")
    for k, v in list(knowledge_graph.items())[:5]:
        print("Skill", k, "→", v)
    print("\nBuilding skill map...")

    skill_map = build_skill_map(df)
    num_skills = len(skill_map)
    print("Number of skills:", num_skills)
    print("\nEncoding sequences...")

    encoded = encode_sequences(sequences, skill_map)
    print("\nBuilding DKT dataset...")

    X, y = build_dkt_dataset(encoded, num_skills)
    print("Tensor dataset shape:", X.shape)
    print("\nBuilding knowledge map...")

    knowledge = build_knowledge_map(encoded)


    # take the first student for demonstration
    student_id = list(knowledge.keys())[0]
    student_knowledge = knowledge[student_id]
    print("\nStudent:", student_id)
    print("Knowledge probabilities:")

    for skill, prob in sorted(student_knowledge.items(), key = lambda x: x[1]):
        name = skill_lookup.get(skill_map.get(skill, skill), f"Skill {skill}")
        print(name, ":", round(prob, 2))

    print("\nDetecting learning gaps...")

    gaps = detect_gaps(student_knowledge)
    print("\n Leaning gaps:")
    
    for g in gaps:
        name = skill_lookup.get(g, f"Skill {g}")
        print("-", name)
        
    print("\nRecommendations:")

    recs = recommend_topics(gaps)
    for r in recs:

        print("-", r)

if __name__ == "__main__":

    run_pipeline()