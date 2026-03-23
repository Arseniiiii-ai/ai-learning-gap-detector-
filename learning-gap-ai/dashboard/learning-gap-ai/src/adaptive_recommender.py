def recommend_next_skills(student_knowledge, skill_lookup, top_k=5):
    sorted_skills = sorted(student_knowledge.items(), key=lambda x: x[1])

    recommendations = []

    for skill, prob in sorted_skills:
        if skill not in skill_lookup:
            continue

        name = skill_lookup[skill]

        recommendations.append({
            "skill_id": skill,
            "skill_name": name,
            "mastery": round(prob, 2)
        })

        if len(recommendations) >= top_k:
            break

    return recommendations