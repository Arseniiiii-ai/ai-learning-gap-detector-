from src.knowledge_graph import knowledge_graph

def detect_learning_gaps(topic_predictions):
    gaps = []
    for topic, understood in topic_predictions.items():
        if not understood:
            gaps.append(topic)
            prerequisites = knowledge_graph.get(topic, [])
            gaps.extend(prerequisites)
    return list(set(gaps))

