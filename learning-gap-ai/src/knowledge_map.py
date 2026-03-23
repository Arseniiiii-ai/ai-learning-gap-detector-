def build_knowledge_map(encoded_sequences):
    
    knowledge = {}

    for student, seq in encoded_sequences.items():
        if len(seq) == 0:
            continue
        skills = {}
        for skill, correct in seq:
            if skill not in skills:
                skills[skill] = []
            skills[skill].append(correct)
        knowledge[student] = {
            skill: sum(vals) / len(vals)
            for skill, vals in skills.items()
        }
    return knowledge
