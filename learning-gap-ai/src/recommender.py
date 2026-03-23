def recommend_topics(gaps, skill_lookup):
    
    recommendations = []
    
    for topic in gaps:
        
        name = skill_lookup.get(topic, f"Skill {topic}")
        recommendations.append(f"Review topic: {name}")
        
    return recommendations
