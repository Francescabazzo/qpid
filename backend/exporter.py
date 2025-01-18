from backend.backend import calculate_scores, get_matches
import dill as pickle

def main():
    with open('../artifacts/calculate_scores.pkl', 'wb') as file:
        pickle.dump(calculate_scores,file)

    with open('../artifacts/get_matches.pkl', 'wb') as file:
        pickle.dump(get_matches, file)

if __name__=="__main__":
    main()