import matplotlib.pyplot as plt

def precision_at_k(recommended_tracks, relevant_tracks, k):
    return len(set(recommended_tracks[:k]).intersection(set(relevant_tracks))) / k

# Пример рекомендованных и релевантных треков
recommended_tracks = ['track1', 'track2', 'track3', 'track4', 'track5']
relevant_tracks = ['track2', 'track4', 'track6']

# Вычисляем Precision@K для K=5
precision_at_k_value = precision_at_k(recommended_tracks, relevant_tracks, k=5)

# Построение графика
plt.figure(figsize=(8, 6))
plt.bar([f"Precision@{k}" for k in range(1, 6)], [precision_at_k(recommended_tracks, relevant_tracks, k) for k in range(1, 6)])
plt.xlabel('Top K Recommendations')
plt.ylabel('Precision')
plt.title('Precision at K for Top K Recommendations')
plt.show()

print(f"Precision@5: {precision_at_k_value}")