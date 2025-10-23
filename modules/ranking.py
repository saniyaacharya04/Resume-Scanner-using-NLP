import pandas as pd

def rank_candidates(candidates_scores):
    df = pd.DataFrame(candidates_scores)
    df_sorted = df.sort_values(by='score', ascending=False).reset_index(drop=True)
    return df_sorted
