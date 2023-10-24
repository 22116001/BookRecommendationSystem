import pandas as pd
from flask import Flask, render_template, request, url_for
import pickle
import numpy as np

# popular_df = pickle.load(open('popular.pkl', 'rb'))
# pt = pickle.load(open('pt.pkl', 'rb'))
# books = pickle.load(open('books.pkl', 'rb'))
# similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_rating'].to_list()
                           )
@app.route('/recommend')
def recommend_ui () :
    return render_template('recommend.html')

@app.route('/recommend_books' )
def recommend():
    user_input = request.form.get('user_input')

    # index = np.where(pt.index == user_input)[0][0]

    index_array = np.where(pt['index'] == user_input)[0]

    if len(index_array) > 0:
        index = index_array[0]
        # Now you can use the value of 'index'
        # ...
    else:
        print("Value not found in the array")


    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

# , methods = ['GET',  'POST']