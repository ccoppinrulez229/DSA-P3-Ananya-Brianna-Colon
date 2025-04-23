#install cinemagoerng and pandas packages within PyCharm
#skibidi

#from pandasql import sqldf
import pandas as pd
import numpy as np
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests

poster_cache = {}

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
from flask import send_file

@app.route('/sunghoon')
def serve_sunghoon():
    return send_file('sunghooned.jpg', mimetype='image/jpg')


def fetch_poster(title):

    api_key = "44166db2"

    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"OMDb result for '{title}':", data)
            poster_url = data["Poster"]
            if poster_url and poster_url != "N/A":
                return poster_url
            else:
                return "/sunghoon"    
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")




#referred to geeksforgeeks for assisting with Red-Black Tree
class Movie:
    def __init__(self, title, year, runtime, genres, plot, rating, numOfVotes):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.genres = [g.strip() for g in genres.split(',')]
        self.plot = plot
        self.rating = rating
        self.num_votes = numOfVotes
        self.posterUrl = None

#function will choose a random movie from the list of movie classes based on rating
def ChooseMovie(movies):
    movie_list = list(movies)
    returned_movie_list = list()
    if len(movie_list)==0:
        return None
    while (len(returned_movie_list)!=3) | (len(movie_list)!=0):
        if (len(movie_list)==0) | (len(returned_movie_list)==3):
            break
        movie = random.choice(movie_list)
        movie_list.remove(movie)
        returned_movie_list.append(movie)


    return returned_movie_list

class rbNode:
    def __init__(self, rating, color='red'):
        self.movies = []
        self.rating = rating
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


class redBlackTree:
    def __init__(self):
        self.root = None

    def insertRotations(self, newNode):
        # can't have two red nodes in a row, requires rotation
        while newNode.parent and newNode.parent.color == 'red':
            #if parent is left child of grandparent
            if newNode.parent == newNode.grandparent().left:
                uncle = newNode.uncle()
                if uncle and uncle.color == 'red':
                    newNode.parent.color = 'black'
                    uncle.color = 'black'
                    newNode.grandparent().color = 'red'
                    newNode = newNode.grandparent()
                else:
                    if newNode == newNode.parent.right:
                        newNode = newNode.parent
                        self.rotateLeft(newNode)
                    newNode.parent.color = 'black'
                    newNode.grandparent().color = 'red'
                    self.rotateRight(newNode.grandparent())

            # if the parent is right child of grandparent
            else:
                uncle = newNode.uncle()
                if uncle and uncle.color == 'red':
                    newNode.parent.color = 'black'
                    uncle.color = 'black'
                    newNode.grandparent().color = 'red'
                    newNode = newNode.grandparent()
                else:
                    if newNode == newNode.parent.left:
                        newNode = newNode.parent
                        self.rotateRight(newNode)
                    newNode.parent.color = 'black'
                    newNode.grandparent().color = 'red'
                    self.rotateLeft(newNode.grandparent())
        self.root.color = 'black'

    def insert(self, movie):
        rating = movie.rating

        if self.root is None:
            newNode = rbNode(rating)
            newNode.movies.append(movie)
            self.root = newNode
        else:
            currNode = self.root
            while True:

                if rating == currNode.rating:
                    currNode.movies.append(movie)
                    return

                # node is in the left subtree
                if rating < currNode.rating:
                    if currNode.left is None:
                        newNode = rbNode(rating)
                        newNode.movies.append(movie)
                        currNode.left = newNode
                        newNode.parent = currNode
                        break
                    else:
                        currNode = currNode.left

                # node is in the right subtree
                else:
                    if currNode.right is None:
                        newNode = rbNode(rating)
                        newNode.movies.append(movie)
                        currNode.right = newNode
                        newNode.parent = currNode
                        break
                    else:
                        currNode = currNode.right

        # do any rotations if needed on newNode
        self.insertRotations(newNode)

    def rotateLeft(self, node):
        rightChild = node.right
        node.right = rightChild.left

        if rightChild.left is not None:
            rightChild.left.parent = node

        rightChild.parent = node.parent

        if node.parent is None:
            self.root = rightChild
        elif node == node.parent.left:
            node.parent.left = rightChild
        else:
            node.parent.right = rightChild

        rightChild.left = node
        node.parent = rightChild

    def rotateRight(self, node):
        leftChild = node.left
        node.left = leftChild.right

        if leftChild.right is not None:
            leftChild.right.parent = node

        leftChild.parent = node.parent

        if node.parent is None:
            self.root = leftChild
        elif node == node.parent.right:
            node.parent.right = leftChild
        else:
            node.parent.left = leftChild

        leftChild.right = node
        node.parent = leftChild

    # given a rating, find a random movie of that rating
    def selectMovie(self, rating):
        currNode = self.root
        while currNode is not None:
            if currNode.rating == rating:
                if (len(currNode.movies) <= 3 and len(currNode.movies) > 0):
                    return currNode.movies
                else:
                    return random.sample(currNode.movies, 3)
            elif rating < currNode.rating:
                currNode = currNode.left
            else:
                currNode = currNode.right

        return None


    # function to perform inorder traversal
    def inorderTraversal(self, node):
        if node is not None:
            self.inorderTraversal(node.left)
            for movie in node.movies:
                print(movie.title, movie.rating)
            self.inorderTraversal(node.right)


#Referred to GeeksForGeeks for assisting with creating Max Heap structure
#max heap will be sorted by ratings. Highest rated on top, lowest rated on bottom
class Movie_Max_Heap:
    def __init__(self, limit):
        self.map = {}
        self.limit = limit
        self.root_index = 1
        self.current_num_of_elements = 0
        self.heap_array = [0] * (limit + 1)
        self.heap_array[0] = sys.maxsize

    def parent(self, i):
        return i // 2

    #returns index for left child of node at index i
    def left(self, i):
        return 2 * i

    #returns right child index of node at index i
    def right(self, i):
        return 2 * i + 1

    def isLeaf(self, i):
        return i > (self.current_num_of_elements // 2) and i <= self.current_num_of_elements

    def swap(self, i, j):
        self.heap_array[i], self.heap_array[j] = self.heap_array[j], self.heap_array[i]

    def Heapify(self, i):
        if not self.isLeaf(i):
            largest = i
            if self.left(i) <= self.current_num_of_elements and self.heap_array[i] < self.heap_array[self.left(i)]:
                largest = self.left(i)
            if self.right(i) <= self.current_num_of_elements and self.heap_array[largest] < self.heap_array[self.right(i)]:
                largest = self.right(i)
            if largest != i:
                self.swap(i, largest)
                self.Heapify(largest)

    def insert(self, movieNode):
        #first, add movie to specific movie rating in map
        if movieNode.rating not in self.map:
            self.map[movieNode.rating] = set()
        self.map[movieNode.rating].add(movieNode)
        #print(self.map)
        if self.current_num_of_elements >= self.limit:
            return
        self.current_num_of_elements += 1
        self.heap_array[self.current_num_of_elements] = float(movieNode.rating)
        i = self.current_num_of_elements
        while self.heap_array[i] > self.heap_array[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def TraverseToRating(self,rating): #traverses to the rating input by the user and chooses a movie
        for i in range (1,self.current_num_of_elements+1):
            #checks parent for a matching rating
            if (self.heap_array[i]==rating):
                return ChooseMovie(self.map[rating])
            #if parent does not have rating, check left child
            elif (self.left(i)<=self.current_num_of_elements) and (self.heap_array[self.left(i)]==rating):
                return ChooseMovie(self.map[rating])
            #if left child does not have rating, check right child
            elif (self.right(i)<=self.current_num_of_elements) and (self.heap_array[self.right(i)]==rating):
                return ChooseMovie(self.map[rating])
        return None

    def ReturnMax(self):
        if self.current_num_of_elements == 0:
            return None
        max_val = self.heap_array[self.root_index]
        self.heap_array[self.root_index] = self.heap_array[self.current_num_of_elements]
        self.current_num_of_elements -= 1
        self.Heapify(self.root_index)
        return max_val

    def printHeap(self):
        for i in range(1, (self.current_num_of_elements // 2) + 1):
            print(f"Parent: {self.heap_array[i]}", end=" ")
            if self.left(i) <= self.current_num_of_elements:
                print(f"Left: {self.heap_array[self.left(i)]}", end=" ")
            if self.right(i) <= self.current_num_of_elements:
                print(f"Right: {self.heap_array[self.right(i)]}", end=" ")
            print()
from flask_cors import cross_origin
from flask import request

@app.route('/get_recommendations', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_recommendations():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight success'}), 200

    genres = request.args.getlist('genres')
    method = request.args.get('method', 'fast')

    imdb_movies = pd.read_csv("movie_ratings_plots.csv", low_memory=False)
    if genres:
        genre_pattern = '|'.join([g.lower() for g in genres])
        imdb_movies = imdb_movies[imdb_movies['genres'].str.lower().str.contains(genre_pattern, na=False)]


    min_rating_string = request.args.get('minrating')
    max_rating_string = request.args.get('maxrating')
    try:
        if min_rating_string:
            min_rating = float(min_rating_string)
            imdb_movies = imdb_movies[imdb_movies['averageRating'] >= min_rating]
        if max_rating_string:
            max_rating = float(max_rating_string)
            imdb_movies = imdb_movies[imdb_movies['averageRating'] <= max_rating]
    except ValueError:
        pass
    if imdb_movies.empty:
        return jsonify({'movies': []})

    movies = []

    if method == 'fast':  # Max Heap
        heap = Movie_Max_Heap(10000)
        for row in imdb_movies.itertuples():
            movie = Movie(
                row.primaryTitle,
                row.startYear,
                row.runtimeMinutes,
                row.genres,
                row.plot,
                row.averageRating,
                row.numVotes
            )
            print(row.plot)
            heap.insert(movie)

        movie_objs = []
        visited_ratings = set()

        while len(movie_objs) < 3 and heap.current_num_of_elements > 0:
            max_rating = heap.ReturnMax()
            if max_rating is None or max_rating in visited_ratings:
                continue
            visited_ratings.add(max_rating)

            # Safely copy movie objects to avoid modifying the map during traversal
            movie_set = heap.map.get(max_rating, set())
            for movie in movie_set:
                if len(movie_objs) < 3:
                    movie_objs.append(movie)
                else:
                    break

        for movie_obj in movie_objs:
            movie_obj.posterUrl = fetch_poster(movie_obj.title)
            movies.append({
                'title': movie_obj.title,
                'rating': movie_obj.rating,
                'genres': movie_obj.genres,
                'posterUrl': movie_obj.posterUrl,
                'plot': movie_obj.plot
            })



    else:  # Red-Black Tree
        rbt = redBlackTree()
        for row in imdb_movies.itertuples():
            movie = Movie(
                row.primaryTitle,
                row.startYear,
                row.runtimeMinutes,
                row.genres,
                row.plot,
                row.averageRating,
                row.numVotes
            )
            rbt.insert(movie)

        movie_objs = []

        def reverse_inorder(node):
            nonlocal movie_objs
            if node is None or len(movie_objs) >= 3:
                return
            reverse_inorder(node.right)
            if node.movies:
                for m in node.movies:
                    if len(movie_objs) < 3:
                        movie_objs.append(m)
            reverse_inorder(node.left)

        reverse_inorder(rbt.root)

        for movie_obj in movie_objs:
            movie_obj.posterUrl = fetch_poster(movie_obj.title)
            movies.append({
                'title': movie_obj.title,
                'rating': movie_obj.rating,
                'genres': movie_obj.genres,
                'posterUrl': movie_obj.posterUrl,
                'plot': movie_obj.plot
            })


    return jsonify({'movies': movies})

if __name__ == "__main__":
    #Download title.basics.tsv.gz file from imdb to use for project, placing it in the same directory as the py file.
    # Might have to remove from directory before pushing to git
    #referred to pandas documentation to figure out how to traverse tsv file
    print("Loading movie dataset...\n")
    imdb_movies = pd.read_csv("movie_ratings_plots.csv", low_memory=False)
    app.run(debug=True)
#     print(
#         "Welcome to Kuromi's Movie Picker! \n1.Action \n2.Adventure\n3.Animation\n4.Comedy\n5.Horror\n6.Dystopian\n7.Mystery")
#     genre = (input("\nChoose a genre (Type the number): "))
#     while True:
#         if not genre.isdigit():
#             genre = int(input("\nInput is not a number! Try again: "))
#             continue
#         if (int(genre) < 1) | (int(genre) > 7):
#             genre = int(input("\nInvalid genre! Try again: "))
#             continue;
#         break

#     method = (input("What method would you like to use? Type 'heap' for a Max Heap, or type 'tree' for Red-Black Tree.\n"))
#     while True:
#         if (method == "heap") | (method=="tree"):
#             break
#         method = (input("Invalid option! Try again: \n"))

#     rating = (input("\nWhat rating on a scale of 1.0 - 10.0 are you looking for? Ratings must be written as a number followed by one decimal place, such as 1.0, 1.1, 1.2...\n"))
# # comedy, drama, romance, crime, action, mystery, thriller, adventure, animation, horror, biography, Sci-Fi, music, sport, war, fantasy, documentary
#     genre_map = {"1":"Action",
#                  "2":"Adventure",
#                  "3":"Animation",
#                  "4":"Comedy",
#                  "5":"Horror",
#                  "6":"Dystopian",
#                  "7":"Mystery"
#                  }

#     while True:
#         if '.' not in rating:
#             rating = (input("\nMissing decimal point! Try again: "))
#             continue
#         if ((float(rating) < 1.0) | (float(rating) > 10.0)) | (len(rating.split('.')[1]) > 1):
#             rating = (input("\nOut of range! Try again: "))
#             continue
#         break
#     rating = float(rating)

#     # only leaving movies that are of the selected genre in the dataframe
#     imdb_movies = imdb_movies[imdb_movies['genres'].str.contains(genre_map[genre], na=False)]

#     #variable for the movie class that ends up being chosen at the end of program execution.
#     movie_chosen = None

#     movie_count=0

#     if method == "heap":
#         max_heap = Movie_Max_Heap(10000)

#         #traverse the movie list and add valid movies to the heap

#         for row in imdb_movies.itertuples():

#             # tconst,titleType,primaryTitle,originalTitle,startYear,runtimeMinutes,genres,averageRating,numVotes
#             movieID = row.tconst
#             movieTitle = row.primaryTitle
#             movieYear = row.startYear
#             movieRuntime = row.runtimeMinutes
#             movieGenres = row.genres
#             movieRating = row.averageRating
#             movieVoteCount = row.numVotes
#             moviePlot = "none"

#             movieObj = Movie(movieTitle, movieYear, movieRuntime, movieGenres, moviePlot, movieRating, movieVoteCount)
#             max_heap.insert(movieObj)

#         #once all movies added to heap, traverse the heap to select a movie
#         movie_chosen = max_heap.TraverseToRating(rating)



#     else:
#         rbTree = redBlackTree()

#         for row in imdb_movies.itertuples():

#             # tconst,titleType,primaryTitle,originalTitle,startYear,runtimeMinutes,genres,averageRating,numVotes
#             movieID = row.tconst
#             movieTitle = row.primaryTitle
#             movieYear = row.startYear
#             movieRuntime = row.runtimeMinutes
#             movieGenres = row.genres
#             movieRating = row.averageRating
#             movieVoteCount = row.numVotes
#             moviePlot = row.plot

#             movieObj = Movie(movieTitle, movieYear, movieRuntime, movieGenres, moviePlot, movieRating, movieVoteCount)
#             rbTree.insert(movieObj)

#         movie_chosen = rbTree.selectMovie(rating)

#         # for id in titlesList:
#         #     print(f"{movie_count}/{len(titlesList)} movies inserted",end='\r')
#         #     movie = web.get_title(id)
#         #     #will only insert movies into the heap that are present in the list and have a rating that isn't None
#         #     if (movie != None) and (movie.rating != None):
#         #         #create a new node for the movie that will then be inserted into the data structure
#         #         movieObj = Movie(movie.title, movie.year, movie.runtime, movie.genres, movie.plot, movie.rating, movie.vote_count)
#         #         rbTree.insert(movieObj)
#         #         movie_count+=1

#     if movie_chosen == None:
#         print(f"Movie with rating {rating} could not be found!")
#     else:
#         print(f"\nKuromi has made a decision. Tonight's top 3 movies chosen for movie night will be.... ")
#         for movie in movie_chosen:
#             print(f"\n{movie.title}\nRating: {movie.rating}\nYear: {movie.year}\nGenres: {movie.genres}\nPlot: {movie.plot}\nNumber of Votes: {movie.num_votes}")
#             print("\n--------------")


######################### code to test RB Tree ###############################
    # movie1 = Movie("movie1", 2000, 100, "action", "plot", 9.5, 1000)
    # movie2 = Movie("movie2", 2000, 100, "action", "plot", 9.0, 1000)
    # movie3 = Movie("movie3", 2000, 100, "action", "plot", 10.0, 1000)
    # movie4 = Movie("movie4", 2000, 100, "action", "plot", 9.5, 1000)
    # movie5 = Movie("movie5", 2000, 100, "action", "plot", 9.5, 1000)
    # movie6 = Movie("movie6", 2000, 100, "action", "plot", 10.0, 1000)
    # movie7 = Movie("movie7", 2000, 100, "action", "plot", 9.5, 1000)
    # movie8 = Movie("movie8", 2000, 100, "action", "plot", 9.0, 1000)
    # movie9 = Movie("movie9", 2000, 100, "action", "plot", 9.5, 1000)
    #
    # movieList = [movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9]
    #
    # rbTree = redBlackTree()
    # for movie in movieList:
    #     rbTree.insert(movie)
    #
    # rbTree.inorderTraversal(rbTree.root)

    ################ code for shrinking imdb dataset file #############################
    # #imdb_titles is our table of movies. filter out any non-movies or adult content.
    # #referred to IDMB's non commercial dataset documentation to figure out the syntax for identifying movies
    # imdb_titles = pd.read.csv("title.basics.tsv", sep='\t', low_memory=False)
    # imdb_titles = imdb_movies[(imdb_movies['titleType'] == 'movie') | (imdb_movies['titleType'] == 'tvMovie')]
    # imdb_titles = imdb_titles[(imdb_titles['startYear'] >= '1960') & (imdb_titles['startYear'] <= '2025')]
    # imdb_titles = imdb_titles[imdb_titles['isAdult'] == '0']
    # imdb_titles = imdb_titles.replace(to_replace='\\N', value='NA')
    # imdb_titles = imdb_titles.drop(['isAdult', 'endYear'], axis=1)
    #
    # title_ratings = pd.read_csv("title.ratings.tsv", sep='\t', low_memory=False)
    #
    # pysqldf = lambda q: sqldf(q, globals())
    #
    # q = """SELECT t.*, r.averageRating, r.numVotes
    # FROM imdb_titles t
    # LEFT JOIN title_ratings r
    # ON t.tconst = r.tconst
    # """
    #
    # movie_and_ratings = pysqldf(q)
    #
    # movie_and_ratings = movie_and_ratings.replace(np.nan, 0)
    #
    # movie_and_ratings = movie_and_ratings[movie_and_ratings['numVotes'] > 10000]
    #
    # movie_and_ratings.to_csv("movie_and_ratings.csv", index=False)
