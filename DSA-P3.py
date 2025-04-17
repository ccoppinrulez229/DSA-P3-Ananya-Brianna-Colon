#install cinemagoerng and pandas packages within PyCharm
from cinemagoerng import web
import pandas as pd
import sys


#Referred to GeeksForGeeks for assisting with creating Max Heap structure
#max heap will be sorted by ratings. Highest rated on top, lowest rated on bottom
class Movie_Max_Heap:
    def __init__(self,limit):
        self.limit=limit
        self.n=0
        self.a=[0]* (limit+1)
        self.a[0]=sys.maxsize
        self.root = 1
        self.map = {}

    def parent(self,i):
        return i//2

    def left(self,i):
        return 2*i

    def right(self,i):
        return 2*i+1

    def isLeaf(self,i):
        return i>(self.n//2) and i <= self.n

    def swap(self,i,j):
        self.a[i],self.a[j]=self.a[j],self.a[i]

    def Heapify(self,i):
        if not self.isLeaf(i):
            largest=i
            if self.left(i) <= self.n and self.a[i] < self.a[self.left(i)]:
                largest = self.left(i)
            if self.right(i) <= self.n and self.a[largest]<self.a[self.right(i)]:
                largest = self.right(i)
            if largest != i:
                self.swap(i,largest)
                self.Heapify(largest)

    def insert(self,movie):
        #first, add movie to specific movie rating in map
        if movie.rating not in self.map:
            self.map[movie.rating]=set()
        self.map[movie.rating].add(movie.title)
        #print(self.map)
        if self.n >= self.limit:
            return
        self.n+=1
        self.a[self.n]=float(movie.rating)
        i=self.n
        while self.a[i] > self.a[self.parent(i)]:
            self.swap(i,self.parent(i))
            i = self.parent(i)

    def ReturnMax(self):
        if self.n == 0:
            return None
        max_val = self.a[self.root]
        self.a[self.root] = self.a[self.n]
        self.n -= 1
        self.Heapify(self.root)
        return max_val

    def printHeap(self):
        for i in range(1, (self.n // 2) + 1):
            print(f"Parent: {self.a[i]}", end=" ")
            if self.left(i) <= self.n:
                print(f"Left: {self.a[self.left(i)]}", end=" ")
            if self.right(i) <= self.n:
                print(f"Right: {self.a[self.right(i)]}", end=" ")
            print()

#Download title.basics.tsv.gz file from imdb to use for project, placing it in the same directory as the py file.
# Might have to remove from directory before pushing to git
imdb_movies=pd.read_csv("title.basics.tsv",sep='\t')

#imdb_titles is our table of movies. filter out any non-movies or adult content.
imdb_titles = imdb_movies[(imdb_movies['titleType']=='movie') | (imdb_movies['titleType']=='tvMovie') | (imdb_movies['titleType']=='short')]
imdb_titles = imdb_titles[imdb_titles['isAdult']=='0']
imdb_titles = imdb_titles.replace(to_replace='\\N',value='NA')
imdb_titles = imdb_titles.drop(['isAdult','endYear'], axis = 1)

print("Welcome to Kuromi's Movie Picker! \n1.Action \n2.Adventure\n3.Animation\n4.Comedy\n5.Horror\n6.Dystopian\n7.Mystery")
genre = int(input("\nChoose a genre (Type the number): "))
while (genre<1) | (genre>7):
    genre = int(input("\nInvalid genre! Try again: "))

rating = (input("\nWhat rating on a scale of 1.0 - 10.0 are you looking for? Ratings must be written as a number followed by one decimal place, such as 1.0, 1.1, 1.2...\n"))
while '.' not in rating:
    rating = (input("\nMissing decimal point! Try again: "))
while ((float(rating)<1.0) | (float(rating)>10.0)) | (len(rating.split('.')[1])>1):
    rating = (input("\nOut of range! Try again: "))

rating = float(rating)

#converting the imdb ID column (tconst) into a list to iterate through
titlesList = imdb_titles['tconst'].values.tolist()
print(len(titlesList))

#max heap created with a limit of 10000
max_heap = Movie_Max_Heap(10000)

#traverse the movie list and add valid movies to the heap
for id in titlesList:
    movie = web.get_title(id)
    #will only insert movies into the heap that are present in the list and have a rating that isn't None
    if (movie!=None) and (movie.rating!=None):
        print(f"Movie: {movie.title}   |   Rating: {movie.rating}")
        max_heap.insert(movie)