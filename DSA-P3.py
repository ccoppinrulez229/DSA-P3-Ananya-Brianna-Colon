#install cinemagoerng and pandas packages within PyCharm
#skibidi

from cinemagoerng import web
from pandasql import sqldf
import pandas as pd
import numpy as np
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    genres = data.get('genres', [])
    speed = data.get('speed', 'fast')

    if speed == 'fast':
        heap = Movie_Max_Heap(10000)
        for id in titlesList:
            movie = web.get_title(id)
            if movie and movie.rating and hasattr(movie, 'genres'):
                if any(g.lower() in [x.lower() for x in movie.genres] for g in genres):
                    heap.insert(movie)
        movies = []
        for _ in range(3):
            max_rating = heap.ReturnMax()
            if max_rating in heap.map:
                title = heap.map[max_rating].pop()
                movies.append({
                    'title': title,
                    'rating': max_rating,
                    'genres': genres,
                    'posterUrl': ''
                })
        return jsonify({'movies': movies})

    elif speed == 'slow':
        rbt = redBlackTree()
        for id in titlesList:
            movie = web.get_title(id)
            if movie and movie.rating and hasattr(movie, 'genres'):
                if any(g.lower() in [x.lower() for x in movie.genres] for g in genres):
                    rbt.insert(movie)
        top_movies = rbt.get_top_k(3)
        return jsonify({'movies': [{
            'title': m.title,
            'rating': m.rating,
            'genres': m.genres,
            'posterUrl': ''
        } for m in top_movies]})

    return jsonify({'movies': []})

#Referred to GeeksForGeeks for assisting with creating Max Heap structure
#max heap will be sorted by ratings. Highest rated on top, lowest rated on bottom

#referred to geeksforgeeks for assisting with Red-Black Tree
class Movie:
    def __init__(self, title, year, runtime, genres, plot, rating, numOfVotes):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.genres = [genres]
        self.plot = plot
        self.rating = rating
        self.numOfVotes = numOfVotes



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
                        currNode.left = newNode
                        newNode.parent = currNode
                        break
                    else:
                        currNode = currNode.left

                # node is in the right subtree
                else:
                    if currNode.right is None:
                        newNode = rbNode(rating)
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

    # function to perform inorder traversal
    def inorderTraversal(self, node):
        if node is not None:
            self.inorderTraversal(node.left)
            print(node.value, end=" ")
            self.inorderTraversal(node.right)


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

    def left(self, i):
        return 2 * i

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
        self.heap_array[self.current_num_of_elements] = float(movie.rating)
        i = self.current_num_of_elements
        while self.heap_array[i] > self.heap_array[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

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


if __name__ == "__main__":
    #Download title.basics.tsv.gz file from imdb to use for project, placing it in the same directory as the py file.
    # Might have to remove from directory before pushing to git
    #referred to pandas documentation to figure out how to traverse tsv file
    imdb_movies = pd.read_csv("movie_and_ratings.csv", low_memory=False)

    # #imdb_titles is our table of movies. filter out any non-movies or adult content.
    # #referred to IDMB's non commercial dataset documentation to figure out the syntax for identifying movies
    # imdb_titles = imdb_movies[(imdb_movies['titleType'] == 'movie') | (imdb_movies['titleType'] == 'tvMovie')]
    # imdb_titles = imdb_titles[(imdb_titles['startYear'] >= '1990') & (imdb_titles['startYear'] <= '2025')]
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

    print(
        "Welcome to Kuromi's Movie Picker! \n1.Action \n2.Adventure\n3.Animation\n4.Comedy\n5.Horror\n6.Dystopian\n7.Mystery")
    genre = int(input("\nChoose a genre (Type the number): "))
    while (genre < 1) | (genre > 7):
        genre = int(input("\nInvalid genre! Try again: "))

    rating = (input(
        "\nWhat rating on a scale of 1.0 - 10.0 are you looking for? Ratings must be written as a number followed by one decimal place, such as 1.0, 1.1, 1.2...\n"))

    while True:
        if '.' not in rating:
            rating = (input("\nMissing decimal point! Try again: "))
            continue
        if ((float(rating) < 1.0) | (float(rating) > 10.0)) | (len(rating.split('.')[1]) > 1):
            rating = (input("\nOut of range! Try again: "))
            continue
        break
    rating = float(rating)

    method = (input("What method would you like to use? Type 'heap' for a Max Heap, or type 'tree' for Red-Black Tree.\n"))
    while True:
        if (method == "heap") | (method=="tree"):
            break
        method = (input("Invalid option! Try again: \n"))

    #converting the imdb ID column (tconst) into a list to iterate through
    titlesList = imdb_movies['tconst'].values.tolist()
    print(len(titlesList))

    #max heap created with a limit of 10000

    if method == "heap":
        max_heap = Movie_Max_Heap(10000)

        #traverse the movie list and add valid movies to the heap

        for id in titlesList:
            movie = web.get_title(id)
            #will only insert movies into the heap that are present in the list and have a rating that isn't None
            if (movie != None) and (movie.rating != None):
                #create a new node for the movie that will then be inserted into the data structure
                movie_node = Movie(movie.title, movie.year, movie.runtime, movie.genres, movie.plot, movie.rating, movie.vote_count)
                print(f"Movie: {movie_node.title} | Year: {movie_node.year} | Runtime: {movie_node.runtime} | Genres: {movie_node.genres} | Plot: {movie_node.plot} | Rating: {movie_node.rating} | Vote Count: {movie_node.numOfVotes}")
                max_heap.insert(movie_node)

    else:

        rbTree = redBlackTree()

        for id in titlesList:
            movie = web.get_title(id)
            #will only insert movies into the heap that are present in the list and have a rating that isn't None
            if (movie != None) and (movie.rating != None):
                #create a new node for the movie that will then be inserted into the data structure
                movieObj = Movie(movie.title, movie.year, movie.runtime, movie.genres, movie.plot, movie.rating, movie.vote_count)
                rbTree.insert(movieObj)





