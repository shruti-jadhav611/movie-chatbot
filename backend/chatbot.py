import nltk
import difflib
import json
import pandas as pd
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load your datasets
movie_det = pd.read_csv("tmdb_5000_movies.csv")
movie_ = pd.read_csv("tmdb_5000_credits.csv")
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------- Core Logic Functions -------

def get_movie_full_info(movie_name):
    movie_name = movie_name.lower()
    all_titles = movie_det['title'].str.lower().tolist()
    close_matches = difflib.get_close_matches(movie_name, all_titles, n=1, cutoff=0.6)
    if not close_matches:
        return None, "No matching movie found."
    closest_match = close_matches[0]
    movie_details = movie_det[movie_det['title'].str.lower() == closest_match].iloc[0]
    movie_cast = movie_[movie_['title'].str.lower() == closest_match].iloc[0]
    try:
        cast_list = json.loads(movie_cast['cast'])
    except Exception as e:
        return None, f"Error parsing cast information: {e}"
    characters = []
    for actor in cast_list:
        if 'character' in actor:
            characters.append(f"{actor['character']} : {actor['name']}")
    crew_list = json.loads(movie_cast['crew'])
    genres_list = json.loads(movie_details['genres'])
    genres = [genre['name'] for genre in genres_list]
    directors = [person['name'] for person in crew_list if person['job'] == 'Director']
    return {
        "title": movie_details['title'],
        "release_date": movie_details['release_date'],
        "overview": movie_details['overview'],
        "revenue": movie_details.get('revenue', 'N/A'),
        "language": movie_details.get('original_language', 'N/A'),
        "tagline": movie_details.get('tagline', 'N/A'),
        "genres": genres,
        "directors": directors,
        "characters": characters[:10]
    }, None

def recommend(movie_name):
    movie_name = movie_name.lower()
    all_titles = movies['title'].str.lower().tolist()
    close_matches = difflib.get_close_matches(movie_name, all_titles, n=1, cutoff=0.6)
    if not close_matches:
        return ["No matching movie found. Please try again."]
    closest_match = close_matches[0]
    index = movies[movies['title'].str.lower() == closest_match].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]]['title'])
    return recommended_movie_names

def extract_movie_name_and_keyword(query):
    stop_words = set(stopwords.words('english'))
    query = query.lower()
    words = word_tokenize(query)
    filtered_words = [word for word in words if word not in stop_words]
    movie_keywords = ['director', 'cast', 'revenue', 'genre', 'recommend', 'actors', 'characters', 'tagline', 'story']
    keyword = None
    for word in movie_keywords:
        if word in filtered_words:
            keyword = word
            break
    if keyword:
        keyword_index = filtered_words.index(keyword)
        movie_name = ' '.join(filtered_words[keyword_index + 1:])
    else:
        movie_name = None
    return keyword, movie_name

def chatbot_query(query):
    query = query.strip().lower()
    if query=="hi" or query=="hello":
        return "hi!!I am your bot and how can I help you"
    if query == 'exit':
        return "Goodbye! Have a great day!"
    keyword, movie_name = extract_movie_name_and_keyword(query)
    if not movie_name:
        return "I couldn't find the movie name in your query. Please try again."
    movie_info, error = get_movie_full_info(movie_name)
    if error:
        return error
    if keyword == 'director':
        directors = movie_info["directors"]
        if directors:
            return f"The director(s) of {movie_name.title()} is/are: {', '.join(directors)}"
        else:
            return f"Sorry, I couldn't find the director of {movie_name.title()}."
    elif keyword == 'cast' or keyword == 'characters':
        characters = movie_info["characters"]
        cast_info = "\n".join([f"{idx + 1}. {char}" for idx, char in enumerate(characters)])
        return f"Top characters of {movie_name.title()}:\n{cast_info}"
    elif keyword == 'revenue':
        revenue = movie_info["revenue"]
        return f"The revenue of {movie_name.title()} is: {revenue}"
    elif keyword == 'genre':
        genres = movie_info["genres"]
        return f"The genres of {movie_name.title()} are: {', '.join(genres)}"
    elif keyword == 'recommend':
        recommendations = recommend(movie_name)
        return f"Here are some recommendations similar to {movie_name.title()}:\n" + "\n".join(recommendations)
    elif keyword == 'tagline':
        tagline = movie_info["tagline"]
        return f"The tagline of {movie_name.title()} is: {tagline}"
    elif keyword == 'story':
        overview = movie_info["overview"]
        return f"The story of {movie_name.title()} is: {overview}"
    else:
        return "Sorry, I didn't understand your question. Please ask about the director, cast, revenue, genres, or recommendations."

# Optional: allow testing from CLI
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(chatbot_query(query))
    else:
        print("Please provide a query as a command line argument.")
