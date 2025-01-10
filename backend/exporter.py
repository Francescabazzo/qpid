from backend import get_matches, calculate_scores
import pickle

def main():
    with open('get_matches.pkl', 'wb') as f:
        pickle.dump(get_matches, f)
    with open('calculate_scores.pkl', 'wb') as f:
        pickle.dump(calculate_scores, f)

if __name__ == '__main__':
    main()