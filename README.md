# final_project

# Movie Recommender

## Overview
The Movie Recommender is a system designed to help users discover similar movies based on a given movie title. Leveraging similarity matrices and optional weighting of factors, the system retrieves relevant movie data via TMDV API and presents users with a curated list of the top N most similar movie titles.

## Features
- Seamless text query input for easy interaction.
- Efficient handling of movie ID verification and data retrieval.
- Optional data preprocessing for enhanced recommendation accuracy.
- Utilization of advanced recommendation algorithms for precise and personalized suggestions.
- User-friendly output format showcasing recommended movies with detailed information.

## Input
- **Movie title:** Unique identifier for the movie.
- **Movie Database:** Collection of movie data.
- **IMDB Database:** 37K Movies obtained from IMDB Non-Commercial Databases, filtered.
- **TMDB Database:** 5K Movies available on Kaggle, retrieved from TMDB Database.

## Process
1. Check Movie ID: The system first checks whether the provided movie ID exists in the database.
Handle Cases:
- ID Not Found in the DB: If the movie ID is not found in the database, the system queries the TMDB API to fetch detailed information about the movie. Once retrieved, the movie data is added to the database.
- ID Found: If the movie ID is found in the database, the system proceeds to retrieve movie data directly.
2. Retrieve Movie Data: Upon locating the movie ID, the system retrieves comprehensive information associated with the movie. This includes details such as title, genre, synopsis, cast, release date, and ratings.
3. Preprocess Data: The retrieved movie data undergoes optional preprocessing steps to ensure data consistency and enhance recommendation accuracy. This may involve tasks such as:
  - Text Cleaning: Removing irrelevant characters, punctuation, or HTML tags from text fields.
  - Stemming or Lemmatization: Normalizing words to their root form to improve text analysis.
  - Feature Engineering: Transforming or enriching features to better represent movie attributes.
  - Vectorization: Transforming features into arrays to calculate cosine similarity.
4. Run Recommendation Algorithm: Utilizing advanced recommendation algorithms, such as collaborative filtering, the system generates recommendations based on the movie data and additional factors. These algorithms analyze item similarity to identify relevant movies for recommendation.

## Output
- List of the N most similar movie titles.

## Implementation Details
- **TF-IDF:** Text representation technique used to vectorize textual data.
- **NLP:** Natural Language Processing techniques employed for text preprocessing.
- **Cosine Similarity:** Measure used for calculating similarity scores between movies based on their feature vectors.
- **Description Similarity Matrix:** Matrix computed by using NLP and TD-IDF vectorization for textual data (overview, keywords, crew, actors, production country) and MinMax Scaling for the numerical data (popularity, release year, ratings) representing movie features' similarity between movies.
- **Genre Similarity Matrix:** Matrix computed by using MLB to encode genres, representing genres similarity between movies.
- **Genre Weight:** Optional weight to prioritize certain factors.
- **Top N:** Number of most similar movies to retrieve.
