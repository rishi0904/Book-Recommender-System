"""# -*- coding: utf-8 -*-
Created on Fri Aug 23 10:20:12 2019
@author: Rishi
"""

res=""
#===================================================================
#Helper functions

def clicked():
    global res
    res="\nPython "
    res+="Recommended Books:\n"
    ################recommender code
    bookname=txt.get()
    count=int(combo.get())
    bookID=(bookDF[bookDF['original_title']==bookname]['id'].values[0])
    row = reverseIndexMap[bookID]
    res+="------INPUT BOOK--------\n"
    res+="Title:"+str(bookDF[bookDF['id']==bookID]['original_title'].values[0])+"\n"
    res+="Author:"+str(bookDF[bookDF['id']==bookID]['authors'].values[0])+"\n"
    res+="Printing Book-ID:"+str(bookID)+"\n"
    res+="====================================\n"
    res+="-------RECOMMENDATIONS----------\n"
    count+=2
    for i in np.argsort(pairwiseSimilarity[row])[-count:-2][::-1]:
        print(i)
        bookID=indexMap[i]
        res+="Title:"+str(bookDF[bookDF['id']==bookID]['original_title'].values[0])+"\n"
        res+="Author:"+str(bookDF[bookDF['id']==bookID]['authors'].values[0])+"\n"
        res+="Printing Book-ID:"+str(bookID)+"\n"
        res+="======================================\n"
    print(res)
    l2.configure(text= res)
    
#=========================================================
#importing dependencies

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../Data/" directory.


bookDF=pd.read_csv('C:/Users/Binary/udemy Python DS & ML/Projects/goodreads_CF_item_based_book_recommender _system/data/books.csv')
bookDF=bookDF.drop(['image_url','small_image_url','title','best_book_id','isbn','isbn13'],axis=1)
ratingsDF = pd.read_csv('C:/Users/Binary/udemy Python DS & ML/Projects/goodreads_CF_item_based_book_recommender _system/data/ratings.csv')

bookDF['original_title']=bookDF['original_title'].str.lower()

listOfDictonaries=[]
indexMap = {}
reverseIndexMap = {}
ptr=0
testdf = ratingsDF
testdf=testdf[['user_id','rating']].groupby(testdf['book_id'])
for groupKey in testdf.groups.keys():
    tempDict={}
    groupDF = testdf.get_group(groupKey)
    for i in range(0,len(groupDF)):
        tempDict[groupDF.iloc[i,0]]=groupDF.iloc[i,1]
    indexMap[ptr]=groupKey
    reverseIndexMap[groupKey] = ptr
    ptr=ptr+1
    listOfDictonaries.append(tempDict)

from sklearn.feature_extraction import DictVectorizer
dictVectorizer = DictVectorizer(sparse=True)
#sparse is True means the matrix will not have NaN values instead it'll have zeros in place.
vector = dictVectorizer.fit_transform(listOfDictonaries)

from sklearn.metrics.pairwise import cosine_similarity
pairwiseSimilarity = cosine_similarity(vector)




#==========================================================================
#tkinter code
import tkinter as tk
window=tk.Tk()  #to make a window
window.iconbitmap(r'C:\Users\Binary\udemy Python DS & ML\Projects\goodreads_CF_item_based_book_recommender _system\books.ico')
window.title("Book Recommender System")
window.geometry('420x1000+500+0')
#size and position of the window
window.config(bg="#C8F9C4")
#bg-color of the window 
    

l1 = tk.Label(window, text="Book Recommender System:-",font=("Arial Bold", 20))
#heading
l1.grid (column=1, row=0)
#pack to show the element on the window
#grid() to place the elements in the window 

l3 = tk.Label(window, text="\nEnter the Book Name:\n",font=("Arial", 10))
l3.grid(column=1,row=1)

txt = tk.Entry(window,width=50)
txt.grid(column=1, row=2)

l4 = tk.Label(window, text="\nNumber of Book:\n",font=("Arial", 10))
l4.grid(column=1,row=3)
from tkinter.ttk import *
combo = tk.ttk.Combobox(window)
combo['values']= (1, 3, 5, 7, 10, "Text")
combo.current(1)
combo.grid(column=1, row=4)


bt=tk.Button(window,text="Submit",bg="cyan", fg="black",command=clicked)
bt.grid (column=1, row=5)


l2 = tk.Label(window, text="\nRecommended Books:\n"+res,font=("Arial", 10))
print("\n ----------"+res)
l2.grid(column=1,row=6)

window.mainloop()
