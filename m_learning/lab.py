import pandas as pd
import spacy

# Загрузка модели NLP
nlp = spacy.load("en_core_web_sm")

# Загрузка датасета
data = pd.read_csv("music_recommendations.csv")

# Удаляем дубликаты
data = data.drop_duplicates()

# Функция для ввода предпочтений пользователя
def get_user_preferences():
    """
    Функция для ввода предпочтений пользователя.
    """
    print("Enter parameters")
    preferences = input("Your preferences (e.g. 'I like pop, rock, hip-hop'): ").strip()
    mood = input("Context or mood (e.g. 'sad, happy, romantic'): ").strip()
    language = input("Preferred language (eg 'English', 'Spanish', 'Korean'): ").strip()
    return preferences, mood, language

# Функция для извлечения ключевых слов из предпочтений пользователя
def extract_keywords(preferences):
    """
    Извлекает ключевые слова из пользовательских предпочтений.
    """
    doc = nlp(preferences)
    keywords = [token.text.lower() for token in doc if token.pos_ in ("NOUN", "PROPN", "ADJ")]
    return keywords

# Рекомендации музыки
def recommend_music(preferences_keywords, mood, language, data, top_n=5):
    """
    Рекомендует треки на основе предпочтений и настроения.
    """
    # Приведение языка пользователя в нижний регистр
    language = language.lower()

    # Фильтрация по ключевым словам (жанр или артист)
    filtered = data[
        data['genre'].str.contains('|'.join(preferences_keywords), case=False, na=False) |
        data['artist'].str.contains('|'.join(preferences_keywords), case=False, na=False)
    ]
    
    # Фильтрация по настроению, если оно указано
    if mood.lower() != "none" and mood.lower():
        filtered = filtered[filtered['mood'].str.contains(mood.lower(), case=False, na=False)]
    
    # Фильтрация по языку
    if language != "none" and language:
        filtered = filtered[filtered['language'].str.lower() == language]
    
    # Если результат пустой, ничего не возвращаем
    if filtered.empty:
        print("No matching tracks were found for your preferences. Try other keywords.")
        return pd.DataFrame()

    # Сортировка по популярности
    recommendations = filtered.sort_values(by='popularity', ascending=False)
    return recommendations.head(top_n)

# Сбор обратной связи о треках
def get_feedback(recommendations):
    """
    Сбор обратной связи о треках.
    """
    print("\nRate the suggested tracks (like, dislike, skip):")
    feedback = {}
    for i, (_, row) in enumerate(recommendations.iterrows(), 1):
        print(f"{i}. {row['artist']} - {row['track_name']} (genre - {row['genre']}, language - {row['language']})")
        feedback[i] = input(f"Track Rating #{i} (like/dislike/skip): ").strip().lower()
    return feedback

# Создание персонализированного плейлиста
def create_playlist(feedback, recommendations):
    """
    Создаёт персонализированный плейлист на основе лайков.
    """
    # Важно учитывать, что индексы в feedback начинаются с 1, а в recommendations с 0
    liked_tracks = [i-1 for i, rating in feedback.items() if rating == "like" and i-1 < len(recommendations)]
    playlist = recommendations.iloc[liked_tracks]
    return playlist

# Главная функция
def main():
    # Получение предпочтений
    preferences, mood, language = get_user_preferences()
    
    # Извлечение ключевых слов
    keywords = extract_keywords(preferences)
    
    # Генерация рекомендаций
    recommendations = recommend_music(keywords, mood, language, data)
    
    # Вывод рекомендаций
    if recommendations.empty:
        print("\nUnfortunately, we did not find any suitable tracks.")
    else:
        print("\nRecommended tracks:")
        for i, row in recommendations.iterrows():
            print(f"{row['artist']} - {row['track_name']}, genre - {row['genre']}, language - {row['language']}, rating - {row['popularity']}")
    
    # Сбор обратной связи
    feedback = get_feedback(recommendations)
    
    # Создание плейлиста
    playlist = create_playlist(feedback, recommendations)
    
    print("\nYour personalized playlist:")
    if not playlist.empty:
        for _, row in playlist.iterrows():
            print(f"{row['artist']} - {row['track_name']} (genre - {row['genre']}, language - {row['language']})")
    else:
        print("Playlist empty.")

# Запуск программы
if __name__ == "__main__":
    main()
