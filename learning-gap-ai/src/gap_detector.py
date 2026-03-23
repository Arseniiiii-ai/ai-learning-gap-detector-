from src.knowledge_graph import knowledge_graph

def detect_gaps(student_accuracy, threshold=0.3):
    gaps = []
    for topic, acc in student_accuracy.items():
        if acc < threshold:
            gaps.append(topic)
            prerequisites = knowledge_graph.get(topic, [])
            gaps.extend(prerequisites)

    return list(set(gaps))