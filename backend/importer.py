import dill as pickle
import streamlit


@streamlit.cache_resource(ttl=3600)
def load_pickles():
    with open('artifacts/calculate_scores.pkl', 'rb') as file:
        calculate_scores = pickle.load(file)

    with open('artifacts/get_matches.pkl', 'rb') as file:
        get_matches = pickle.load(file)

    return calculate_scores, get_matches
