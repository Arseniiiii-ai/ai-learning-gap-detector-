from collections import defaultdict 

def build_auto_knowledge_graph(sequences):
    transitions = defaultdict(lambda: defaultdict(int))
    
    for student, seq in sequences.items():
        for i in range(len(seq) - 1):
            skill_a, _ = seq[i]
            skill_b, _ = seq[i + 1]
            transitions[skill_a][skill_b] += 1
            
    graph = {}
    for skill, next_skills in transitions.items():
        graph[skill] = sorted(
            next_skills,
            key = next_skills.get,
            reverse = True
        )[:3] 
        
    return graph
    