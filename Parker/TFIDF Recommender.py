import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_clean_data(data_path):
    df = pd.read_csv(data_path)
    df = df[['Internal ID', 'Name', 'People', 'Topics', 'Clean Text']]
    df.fillna({'People': '', 'Topics': '', 'Clean Text': ''}, inplace=True)
    df['Topics'] = df['Topics'].apply(lambda x: ' '.join(x.split('|')))
    df['People'] = df['People'].apply(lambda x: ' '.join(x.split('|')))
    return df

def create_tfidf_matrix(data, stop_words='english'):
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform(data)
    return tfidf_matrix

def get_row_number_by_internal_id(df, internal_id):
    internal_id = str(internal_id)  # Convert internal_id to string for comparison
    index = df[df['Internal ID'].astype(str).str.strip() == internal_id].index
    if not index.empty:
        return index[0]
    else:
        return None

def get_recommendations(df, row_number, similarity_matrix, threshold=0.2, num_recommendations=3):
    sim_scores = list(enumerate(similarity_matrix[row_number]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [item for item in sim_scores if item[1] > threshold]
    recommended_ids = [df.iloc[item[0]]['Internal ID'] for item in sim_scores if item[0] != row_number]
    return recommended_ids[:num_recommendations]

def main():
    # Choose what row (internal ID) you want to analyze
    internal_id = 91
    
    # Import document
    data_path = 'Desktop/School/current semester/Consulting Wilford Woodruff/recent_wwp_documents.csv'
    df = load_and_clean_data(data_path)

    # Creates 'People' scores to create matrix ([# of rows matrix] x 1)
    tfidf_matrix_people = create_tfidf_matrix(df['People'])
    tfidf_matrix_topics = create_tfidf_matrix(df['Topics'])
    tfidf_matrix_text = create_tfidf_matrix(df['Clean Text'])
    print("(1/5) Scores Created")
    # Uses TFIDF matrix to create
    people_similarity = cosine_similarity(tfidf_matrix_people)
    topics_similarity = cosine_similarity(tfidf_matrix_topics)
    text_similarity = cosine_similarity(tfidf_matrix_text)
    print("(2/5) Matrices Loaded")

    row_number = get_row_number_by_internal_id(df, internal_id)

    #   CLEAN TEXT comparisons
    if row_number is not None:
        recommendations_combined = get_recommendations(df, row_number, text_similarity)
        print(f"(3/5) (Text) Recommended for Internal_ID {internal_id} (row # {row_number + 1}): {recommendations_combined}")
    else:
        print(f"(3/5) Internal_ID {internal_id} not found in the DataFrame.")
        pass
    #   PEOPLE comparisons
    if row_number is not None:
        recommendations_combined = get_recommendations(df, row_number, people_similarity)
        print(f"(4/5) (People) Recommended for Internal_ID {internal_id} (row # {row_number + 1}): {recommendations_combined}")
    else:
        print(f"(4/5) Internal_ID {internal_id} not found in the DataFrame.")
        pass
    #   TOPICS comparisons
    if row_number is not None:
        recommendations_combined = get_recommendations(df, row_number, topics_similarity)
        print(f"(5/5) (Topics) Recommended for Internal_ID {internal_id} (row # {row_number + 1}): {recommendations_combined}")
    else:
        print(f"(5/5) Internal_ID {internal_id} not found in the DataFrame.")
        pass


if __name__ == "__main__":
    main()


