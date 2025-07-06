def predict_mood(description):
    description = description.lower()
    moods = []
    if any(word in description for word in ['love', 'romance', 'heart']):
        moods.append('romantic')
    if any(word in description for word in ['happy', 'joy', 'fun']):
        moods.append('happy')
    if any(word in description for word in ['scary', 'ghost', 'horror']):
        moods.append('scary')
    if any(word in description for word in ['thrill', 'action', 'chase']):
        moods.append('thrilling')
    if any(word in description for word in ['sad', 'cry', 'loss']):
        moods.append('sad')
    return ','.join(moods) if moods else 'neutral'
