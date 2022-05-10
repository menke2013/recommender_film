## importing libraries
import streamlit as st
import pandas as pd
import numpy as np

import functions_recommender_module

## creating some dataframes and variables

st.markdown("<h1 style='text-align: center; color: red;'>What are we doing tonight?</h1>", unsafe_allow_html=True)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
 
df_ratings = pd.read_csv('cleanratings.csv')
df_movies = pd.read_csv('cleanmovies.csv')

#df_ratings = pd.read_csv('https://raw.githubusercontent.com/menke2013/recommender_test/main/cleanratings.csv')
#df_movies = pd.read_csv('https://raw.githubusercontent.com/menke2013/recommender_test/main/cleanmovies.csv')

df_ratings_movies_merge = df_ratings.merge(df_movies, how='left', on='movieId')

##### Interface for user

selection_options = ['Top Films of a Genre', 'Comparable Films List']
selected_option = st.sidebar.radio('Selection', selection_options)

if selected_option == 'Top Films of a Genre':
    
    genre_choice = st.sidebar.selectbox(
     'Which genre are you interested in?',
     ('Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
       'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror',
       'Mystery', 'Sci-Fi', 'War', 'Musical', 'Documentary', 'IMAX',
       'Western', 'Film-Noir'))
    genre_choice2 = []
    genre_choice2.append(genre_choice)
    
    number_of_top_films = st.sidebar.selectbox(
    'How many films should be suggested to you?', (5,10,15,20))
        
    st.dataframe(functions_recommender_module.get_best_films(df_ratings_movies_merge,df_movies=df_movies,num_of_films=number_of_top_films, genre=genre_choice2, n_min_rating_counts=5),1000,1000)

    
if selected_option == 'Comparable Films List':
    
    user_selected_film = st.sidebar.text_input('Select a film or keyword:').lower()
    
    df_user_selection_films = df_movies[df_movies['title'].str.lower().str.contains(user_selected_film)][['title', 'genres']]
    st.write('Movie(s) found in our database. Select the preferred one in the menu on the left.')
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df_user_selection_films)
    
    list_selection_table_films = df_user_selection_films['title'].to_list()
    
    user_selected_film_exact = st.sidebar.selectbox(
    'Which film precisely?', (list_selection_table_films))
    st.write(user_selected_film_exact)
            
    number_of_suggested_films = st.sidebar.selectbox(
    'How many films should be suggested to you?', (5,10,15,20))
           
    df_returm_film_suggestion = pd.DataFrame(functions_recommender_module.film_based_recommender(df_ratings_movies_merge,df_movies=df_movies, film=user_selected_film_exact, n=number_of_suggested_films))
    
    st.table(df_returm_film_suggestion)
    

    #st.write(df.to_html(), unsafe_allow_html=True)
#def get_sparse_matrix(dense_matrix: pd.DataFrame, var_index: str='userId', var_columns: str='title', var_values: str='rating'): 
#
#    return(
#    dense_matrix
#        .pivot_table(index=var_index, columns=var_columns, values=var_values, aggfunc='mean'))

#def film_based_recommender2(dense_matrix: pd.DataFrame, film: str, n: int=5):

#    sparse_matrix = get_sparse_matrix(dense_matrix)
#    var_film = sparse_matrix.filter(like=film).columns[0]
#    print(var_film)
#    sparse_matrix = sparse_matrix[sparse_matrix.get(var_film).notnull()]
#    sparse_matrix = sparse_matrix.dropna(axis='columns', thresh=2)
#    
#    return(
#    sparse_matrix
#        .corrwith(sparse_matrix[var_film])
#        .sort_values(ascending=False)#.head(n)
#        .index
#        .to_list()[1:n+1]
#    )

#st.dataframe(film_based_recommender2(df_ratings_movies_merge, 'Grumpier Old Men', n=10))
