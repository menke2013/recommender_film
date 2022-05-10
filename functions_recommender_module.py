import pandas as pd
import numpy as np



def get_same_genre(data_frame: pd.DataFrame, list_genres_fav_film, n_half):
    a = 0
    df_iterrow = pd.DataFrame()
    for index, row in data_frame.iterrows():
        if a < (n_half+1):
            if any(x in row['genres'] for x in list_genres_fav_film):
                a = a+1    
                
                df_row = pd.DataFrame(row).T
                df_iterrow = pd.concat([df_iterrow, df_row])

        else:
            break
    return df_iterrow    

def get_the_best_films_func1(data_frame: pd.DataFrame, n_min_rating_counts: int=2):
    
    df_return = (data_frame
                 .groupby('movieId')
                 .agg(movie_rating_counts = ('movieId', 'count'), movie_rating_mean = ('rating', 'mean'))
                 .query('movie_rating_counts >= @n_min_rating_counts')
                 .sort_values(by='movie_rating_mean', ascending=False))
                 
    
    return df_return

def get_best_films(data_frame: pd.DataFrame, df_movies: pd.DataFrame, genre , num_of_films: int=20, n_min_rating_counts: int=2):
    
    genre = list(genre)
    print (type(genre))
    df_top_rated_1 = (pd.merge(df_movies,get_the_best_films_func1(data_frame,n_min_rating_counts=n_min_rating_counts)
                               .reset_index(), on='movieId').sort_values(by='movie_rating_mean', ascending=False))
    
    df_top_rated_2 = get_same_genre(df_top_rated_1, genre, num_of_films)
    df_top_rated_2 = df_top_rated_2.drop(['movieId', 'movie_rating_counts'], axis=1)
    df_top_rated_2 = (df_top_rated_2.head(num_of_films)
                      .rename(columns={'movie_rating_mean': 'Rating', 'title': 'Title', 'genres': 'Genre'})
                      .reset_index(drop=True))
    df_top_rated_2.index=df_top_rated_2.index+1
                      
    
    return df_top_rated_2


def get_sparse_matrix(dense_matrix: pd.DataFrame, var_index: str='userId', var_columns: str='title', var_values: str='rating'): 

    return(
    dense_matrix
        .pivot_table(index=var_index, columns=var_columns, values=var_values, aggfunc='mean'))
        
def film_based_recommender(dense_matrix: pd.DataFrame, df_movies: pd.DataFrame, film: str, n: int=5):

    n_half = int(n/2)
    sparse_matrix = get_sparse_matrix(dense_matrix)
    var_film = sparse_matrix.filter(like=film).columns[0]
    list_genres_fav_film = (df_movies['genres'].loc[df_movies['title']==film].to_list()[0]).split('|')
    var_genre_fav_film = df_movies['genres'].loc[df_movies['title']==film].to_list()[0]
    sparse_matrix = sparse_matrix[sparse_matrix.get(var_film).notnull()]
    sparse_matrix = sparse_matrix.dropna(axis='columns', thresh=2)
    
    corr = pd.DataFrame(sparse_matrix
        .corrwith(sparse_matrix[var_film])
        .sort_values(ascending=False)
        .index
        .to_list()).rename(columns={0:'title'})
    
    corr_2 = corr.merge(df_movies, on='title', how = 'left')
    
    df_final_1 = get_same_genre(corr_2, list_genres_fav_film, n_half)
    df_final_1 = pd.concat([df_final_1, corr_2])
    df_final_1.drop_duplicates(subset='title', inplace=True)
    df_final_1.drop(df_final_1[df_final_1['title'] == var_film].index, axis=0, inplace=True)
    df_final_1.drop('movieId', axis=1, inplace=True)
    df_final_1 = df_final_1.head(n)
    
    return df_final_1