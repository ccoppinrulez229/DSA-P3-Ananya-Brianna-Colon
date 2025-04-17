from cinemagoerng import web
import pandas as pd
import sys

#DOWNLOAD TITLE.BASICS.TSV.GZ FILE FROM IMDB DATABASE AND EXTRACT IT TO USE IN PROJECT
imdb_movies=pd.read_csv("title.basics.tsv",sep='\t')

#imdb_titles is our table of movies. filter out any non-movies or adult content.
imdb_titles = imdb_movies[(imdb_movies['titleType']=='movie') | (imdb_movies['titleType']=='tvMovie') | (imdb_movies['titleType']=='short')]
imdb_titles = imdb_titles[imdb_titles['isAdult']=='0']
imdb_titles = imdb_titles.replace(to_replace='\\N',value='NA')
imdb_titles = imdb_titles.drop(['isAdult','endYear'], axis = 1)

#converting the imdb ID column (tconst) into a list to iterate through
titlesList = imdb_titles['tconst'].values.tolist()
print(len(titlesList))

for id in titlesList:
    movie = web.get_title(id)
    if (movie!=None):
        print(f"Movie: {movie.title}   |   Rating: {movie.rating}")


#Referred to GeeksForGeeks for assisting with creating Max Heap structure
#max heap will be sorted by ratings. Highest rated on top, lowest rated on bottom
class Movie_Max_Heap:
    def __init__(self,limit):
        self.limit=limit
        self.n=0
        self.a=[0]* (limit+1)
        self.a[0]=sys.maxsize
        self.root = 10

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
                self.maxHeapify(largest)

    def insert(self,val):
        if self.n >= self.limit:
            return
        self.n+=1
        self.a[self.n]=val
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
        self.maxHeapify(self.root)
        return max_val

    def printHeap(self):
        for i in range(1, (self.n // 2) + 1):
            print(f"Parent: {self.a[i]}", end=" ")
            if self.left(i) <= self.n:
                print(f"Left: {self.a[self.left(i)]}", end=" ")
            if self.right(i) <= self.n:
                print(f"Right: {self.a[self.right(i)]}", end=" ")
            print()