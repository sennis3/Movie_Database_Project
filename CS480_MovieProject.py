#Sean Ennis
#sennis3, 653900061
#CS 480
#12/11/2020

from tkinter import *
import tkinter.messagebox
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

movie_dict = {}
actor_dict = {}
movie_list = []
actor_list = []
movie_list_index = 0
actor_list_index = 0


def six_degrees_fn(actor1, actor2):
    #Clear all data structures
    movie_dict.clear()
    actor_dict.clear()
    movie_list.clear()
    actor_list.clear()
    movie_list_index = 0
    actor_list_index = 0

    target_found = False

    #Set up results display window
    root=Tk()
    root.title('Actor/Movie Connections')
    iList = Listbox(root, height=18, width=50, font=('arial',10,'bold'), justify=CENTER, bg="powder blue")
    scroll = Scrollbar(root, command=iList.yview)
    iList.configure(yscrollcommand = scroll.set)
    iList.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)
    
    #print(actor1)
    #print(actor2)
    actor1_id = get_actor_id(actor1)
    #print(actor1_id)
    target_id = get_actor_id(actor2)

    actor_dict[actor1_id] = 0
    actor_list.append(actor1_id)

    while not target_found:
        if len(actor_list) == 0:
            print("No results found")
            iList.insert(END, "No results found")
            root.mainloop()
            return
        
        for curr_actor_id in actor_list:
            find_movies_with_actor(curr_actor_id)
        actor_list.clear()

        if len(movie_list) == 0:
            print("No results found")
            iList.insert(END, "No results found")
            root.mainloop()
            return

        for curr_movie_id in movie_list:
            find_actors_with_movie(curr_movie_id)
            if target_id in actor_dict.keys():
                target_found = True
                break;
        movie_list.clear()

    traceback_list = []
    actor_name = get_actor_name(target_id)
    traceback_list.append(actor_name)
    curr_id = target_id
    while True:
        curr_id = actor_dict[curr_id] #new curr_id is a movie_id
        movie_name = get_movie_name(curr_id)
        traceback_list.insert(0, movie_name)
        curr_id = movie_dict[curr_id] #new curr_id is a actor_id
        actor_name = get_actor_name(curr_id)
        traceback_list.insert(0, actor_name)

        if curr_id == actor1_id:
            break

    print(traceback_list)

##    root=Tk()
##    root.title('Listbox and Scrollbar')
##    iList = Listbox(root, height=18, width=50, font=('arial',10,'bold'), justify=CENTER, bg="powder blue")
##    scroll = Scrollbar(root, command=iList.yview)
##
##    iList.configure(yscrollcommand = scroll.set)
##    iList.pack(side=LEFT)
##
##    scroll.pack(side=RIGHT, fill=Y)

    for item in traceback_list:
        iList.insert(END, item)

    root.mainloop()

        


def find_movies_with_actor(actor_id):
    lookup_d = actor_id
    query = f"(SELECT movies.movie_id FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE actors.actor_id = '{lookup_d}' ORDER BY movies.votes DESC)"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    for item in query_results:
        #Check to make sure its not already in dictionary
        if item[0] not in movie_dict.keys():
            movie_dict[item[0]] = actor_id
            movie_list.append(item[0])


def find_actors_with_movie(movie_id):
    lookup_d = movie_id
    query = f"(SELECT actors.actor_id FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE movies.movie_id = '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    for item in query_results:
        #Check to make sure its not already in dictionary
        if item[0] not in actor_dict.keys():
            actor_dict[item[0]] = movie_id
            actor_list.append(item[0])


def get_actor_id(actorName):
    lookup_d = actorName
    query = f"(select actor_id from actors where actor_name = '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    actor_id = query_results[0][0]
    return actor_id

def get_actor_name(actor_id):
    lookup_d = actor_id
    query = f"(select actor_name from actors where actor_id = '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    actor_name = query_results[0][0]
    return actor_name

def get_movie_name(movie_id):
    lookup_d = movie_id
    query = f"(select title from movies where movie_id = '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    movie_name = query_results[0][0]
    return movie_name

def connect_db(): 
    db_name = 'movies'
    try:
        conn = mysql.connector.connect(
            user='root', password='password',
            host='localhost', database=db_name)
        return conn
    except:
        print(f"Cannot connect to database: '{db_name}'!")
        return None

def compare_directors_ratings(director1, director2):

##    lookup_d = "%" + director1 +"%"  
##    query = f"(SELECT director_id FROM directors WHERE director_name LIKE '{lookup_d}')"
##    cursor= conn.cursor()
##    cursor.execute(query)
##    result=cursor.fetchall()
##    dir1_id = result[0][0]
##
##    lookup_d = "%" + director2 +"%"  
##    query = f"(SELECT director_id FROM directors WHERE director_name LIKE '{lookup_d}')"
##    cursor= conn.cursor()
##    cursor.execute(query)
##    result=cursor.fetchall()
##    dir2_id = result[0][0]
##
##    msg = "Director 1: " + str(dir1_id) +", Director 2: " + str(dir2_id)
##    tkinter.messagebox.showinfo(title="Information msg", message=msg)


    ave_ratings = []
    max_ratings = []
    min_ratings = []
    directors = []

    lookup_d = "%" + director1 + "%"
    #print(lookup_d)
    query = f"(SELECT avg(avg_vote), director, max(avg_vote), min(avg_vote) FROM movies WHERE director like '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    #print(query_results)
    rating=query_results[0][0]
    director = query_results[0][1]
    max_rating = query_results[0][2]
    min_rating = query_results[0][3]
    #print(rating)
    ave_ratings.append(rating)
    directors.append(director)
    max_ratings.append(max_rating)
    min_ratings.append(min_rating)

    lookup_d = "%" + director2 + "%"
    #print(lookup_d)
    query = f"(SELECT avg(avg_vote), director, max(avg_vote), min(avg_vote) FROM movies WHERE director like '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    #print(query_results)
    rating=query_results[0][0]
    director = query_results[0][1]
    max_rating = query_results[0][2]
    min_rating = query_results[0][3]
    #print(rating)
    ave_ratings.append(rating)
    directors.append(director)
    max_ratings.append(max_rating)
    min_ratings.append(min_rating)

    df = pd.DataFrame({'Min Rating': min_ratings, 'Avg Rating': ave_ratings, 'Max Rating': max_ratings}, index=directors)
    ax = df.plot.bar(rot=0)
    ax.set_ylim(0,10)
    ax.set_ylabel('IMDb Movie Rating Out Of 10')
    #plt.show()
    
    return

def compare_actors_ratings(actor1, actor2):

    ave_ratings = []
    max_ratings = []
    min_ratings = []
    actors = []

    lookup_d = "%" + actor1 + "%"
    #print(lookup_d)
    query = f"(SELECT avg(movies.avg_vote), actors.actor_name, max(movies.avg_vote), min(movies.avg_vote) FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE actors.actor_name Like '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    #print(query_results)
    rating=query_results[0][0]
    actor = query_results[0][1]
    max_rating = query_results[0][2]
    min_rating = query_results[0][3]
    #print(rating)
    ave_ratings.append(rating)
    actors.append(actor)
    max_ratings.append(max_rating)
    min_ratings.append(min_rating)

    lookup_d = "%" + actor2 + "%"
    #print(lookup_d)
    query = f"(SELECT avg(movies.avg_vote), actors.actor_name, max(movies.avg_vote), min(movies.avg_vote) FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE actors.actor_name Like '{lookup_d}')"
    cursor= conn.cursor()
    cursor.execute(query)
    query_results = cursor.fetchall()
    #print(query_results)
    rating=query_results[0][0]
    actor = query_results[0][1]
    max_rating = query_results[0][2]
    min_rating = query_results[0][3]
    #print(rating)
    ave_ratings.append(rating)
    actors.append(actor)
    max_ratings.append(max_rating)
    min_ratings.append(min_rating)

    df = pd.DataFrame({'Min Rating': min_ratings, 'Avg Rating': ave_ratings, 'Max Rating': max_ratings}, index=actors)
    ax = df.plot.bar(rot=0)
    ax.set_ylim(0,10)
    ax.set_ylabel('IMDb Movie Rating Out Of 10')
    #plt.show()
    
    return

def compare_directors_gross(director1, director2):

    ave_grosses = []
    max_grosses = []
    directors = []

    lookup_d = "%" + director1 + "%"
    query = f"(SELECT avg(worldwide_gross_dollar), director, max(worldwide_gross_dollar) FROM movies WHERE director like '{lookup_d}')"
    cursor.execute(query)
    query_results = cursor.fetchall()
    avg_gross=query_results[0][0] / 1000000
    director = query_results[0][1]
    max_gross = query_results[0][2] / 1000000
    ave_grosses.append(avg_gross)
    directors.append(director)
    max_grosses.append(max_gross)

    lookup_d = "%" + director2 + "%"
    query = f"(SELECT avg(worldwide_gross_dollar), director, max(worldwide_gross_dollar) FROM movies WHERE director like '{lookup_d}')"
    cursor.execute(query)
    query_results = cursor.fetchall()
    avg_gross=query_results[0][0] / 1000000
    director = query_results[0][1]
    max_gross = query_results[0][2] / 1000000
    ave_grosses.append(avg_gross)
    directors.append(director)
    max_grosses.append(max_gross)

    df = pd.DataFrame({'Avg gross': ave_grosses, 'Max Gross': max_grosses}, index=directors)
    ax = df.plot.bar(rot=0)
    ax.set_ylabel("Worldwide Gross (millions)")
    #plt.show()
    
    return

def compare_actors_gross(actor1, actor2):

    ave_grosses = []
    max_grosses = []
    actors = []

    lookup_d = "%" + actor1 + "%"
    query = f"(SELECT avg(movies.worldwide_gross_dollar), actors.actor_name, max(movies.worldwide_gross_dollar) FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE actors.actor_name Like '{lookup_d}')"
    cursor.execute(query)
    query_results = cursor.fetchall()
    avg_gross=query_results[0][0] / 1000000
    actor = query_results[0][1]
    max_gross = query_results[0][2] / 1000000
    ave_grosses.append(avg_gross)
    actors.append(actor)
    max_grosses.append(max_gross)

    lookup_d = "%" + actor2 + "%"
    query = f"(SELECT avg(movies.worldwide_gross_dollar), actors.actor_name, max(movies.worldwide_gross_dollar) FROM (movies INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE actors.actor_name Like '{lookup_d}')"
    cursor.execute(query)
    query_results = cursor.fetchall()
    avg_gross=query_results[0][0] / 1000000
    actor = query_results[0][1]
    max_gross = query_results[0][2] / 1000000
    ave_grosses.append(avg_gross)
    actors.append(actor)
    max_grosses.append(max_gross)

    df = pd.DataFrame({'Avg Gross': ave_grosses, 'Max Gross': max_grosses}, index=actors)
    ax = df.plot.bar(rot=0)
    ax.set_ylabel("Worldwide Gross (millions)")
    #plt.show()
    
    return


def compare_directors(director1, director2):

    director1 = director1.strip()
    director2 = director2.strip()
    
    msg = ""
    if len(director1) == 0:
        msg="Missing name for Director #1"
        
    elif len(director2) == 0:
        msg="Missing name for Director #2"
        
    if len(msg) == 0:   # No error so far...
        lookup_d = "%" + director1 +"%"  
        query = f"(SELECT count(*) FROM directors WHERE director_name LIKE '{lookup_d}')"
        cursor= conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        if len(result) == 1:
            if result[0][0] == 1:
                msg=""
                lookup_d = "%" + director2 +"%"  
                query = f"(SELECT count(*) FROM directors WHERE director_name LIKE '{lookup_d}')"
                cursor= conn.cursor()
                cursor.execute(query)
                result=cursor.fetchall()
                if len(result) == 1:
                    if result[0][0] == 1:
                        msg=""
                    else:
                        msg="Use Lookup button for Director 2"
                else:
                    msg="Seomthing went wrong!"
            else:
                msg = "Use lookup button for Director 1"
        else:
            msg = "Seomthing went wrong!"
        
    if len(msg) > 0:
        tkinter.messagebox.showinfo(title="Information msg", message=msg)
    else:
        compare_directors_ratings(director1, director2)
        compare_directors_gross(director1, director2)
        plt.show()

def compare_actors(actor1, actor2):

    actor1 = actor1.strip()
    actor2 = actor2.strip()
    
    msg = ""
    if len(actor1) == 0:
        msg="Missing name for Actor #1"
        
    elif len(actor2) == 0:
        msg="Missing name for Actor #2"
        
    if len(msg) == 0:   # No error so far...
        lookup_d = "%" + actor1 +"%"  
        query = f"(SELECT count(*) FROM actors WHERE actor_name LIKE '{lookup_d}')"
        cursor= conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        if len(result) == 1:
            if result[0][0] == 1:
                msg=""
                lookup_d = "%" + actor2 +"%"  
                query = f"(SELECT count(*) FROM actors WHERE actor_name LIKE '{lookup_d}')"
                cursor= conn.cursor()
                cursor.execute(query)
                result=cursor.fetchall()
                if len(result) == 1:
                    if result[0][0] == 1:
                        msg=""
                    else:
                        msg="Use Lookup button for Actor 2"
                else:
                    msg="Seomthing went wrong!"
            else:
                msg = "Use lookup button for Actor 1"
        else:
            msg = "Seomthing went wrong!"
        
    if len(msg) > 0:
        tkinter.messagebox.showinfo(title="Information msg", message=msg)
    else:
        compare_actors_ratings(actor1, actor2)
        compare_actors_gross(actor1, actor2)
        plt.show()

    
def director_genres(director1):
    genres = []
    numMovies = []

    lookup_d = "%" + director1 + "%"
    #print(lookup_d)
    query = f"(SELECT Count(movies.title) AS CountOftitle, genres.genre FROM (((movies INNER JOIN movies_genres ON movies.movie_id = movies_genres.movie_id) INNER JOIN genres ON movies_genres.genre_id = genres.genre_id) INNER JOIN movies_directors ON movies.movie_id = movies_directors.movie_id) INNER JOIN directors ON movies_directors.director_id = directors.director_id WHERE (((directors.director_name) Like '{lookup_d}')) GROUP BY genres.genre)"
    cursor.execute(query)
    query_results = cursor.fetchall()

    for item in query_results:
        genres.append(item[1])
        numMovies.append(item[0])

    df = pd.DataFrame({'': numMovies},
                  index=genres)
    plot = df.plot.pie(y='', figsize=(5, 5))
    plt.show()

def actor_genres(actor1):
    genres = []
    numMovies = []

    lookup_d = "%" + actor1 + "%"
    #print(lookup_d)
    query = f"(SELECT Count(movies.title) AS CountOftitle, genres.genre FROM (((movies INNER JOIN movies_genres ON movies.movie_id = movies_genres.movie_id) INNER JOIN genres ON movies_genres.genre_id = genres.genre_id) INNER JOIN movies_actors ON movies.movie_id = movies_actors.movie_id) INNER JOIN actors ON movies_actors.actor_id = actors.actor_id WHERE (((actors.actor_name) Like '{lookup_d}')) GROUP BY genres.genre)"
    cursor.execute(query)
    query_results = cursor.fetchall()

    for item in query_results:
        genres.append(item[1])
        numMovies.append(item[0])

    df = pd.DataFrame({'': numMovies},
                  index=genres)
    plot = df.plot.pie(y='', figsize=(5, 5))
    plt.show()
    
    
    
def mainwin():

    def lookup_people(person_type, person_name):

        popupwin=Tk()
        popupwin.title('Full names matching:')
        iList = Listbox(popupwin, height=18, width=35, font=('arial',10,'bold'), justify=LEFT, bg="white")
        scroll = Scrollbar(popupwin, command=iList.yview)

        iList.configure(yscrollcommand = scroll.set)
        iList.pack(side=LEFT)

        scroll.pack(side=RIGHT, fill=Y)

        lookup_d = "%" + person_name +"%"  
        if person_type == "D":
            query = f"(SELECT director_name FROM directors WHERE director_name LIKE '{lookup_d}')"
        else:
            query = f"(SELECT actor_name FROM actors WHERE actor_name LIKE '{lookup_d}')"
            
        cursor= conn.cursor()
        cursor.execute(query)
        result=cursor.fetchall()

        for item in result:
            iList.insert(END, item[0])
        
        popupwin.mainloop()

        return
        

    def lookup_fn1(person_name):
        lkwin = Tk()
        lkwin.title('Lookup Names')
        lkwin.geometry('500x100')
        person_label = Label(lkwin, text="Person to Search: ")
        person_label.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        person = Entry(lkwin, width = 30)
        person.grid(row=0, column = 1, padx=20)
        btn_director = Button(lkwin, text="Director search",
                            command=lambda:lookup_people("D",person.get()))
        btn_director.grid(row=1, column=1, sticky='WE', padx=5, pady=2)
        btn_actor = Button(lkwin, text="Actor search",
                            command=lambda:lookup_people("A", person.get()))
        btn_actor.grid(row=2, column=1, sticky='WE', padx=5, pady=2)
        if len(person_name.strip()) > 0:
            person.insert(0, person_name)
            
        lkwin.mainloop()

        return
    

    topwin = Tk()  # create top window object
    
    topwin.title('Movies Database')
    topwin.geometry('530x500')

    frm1=LabelFrame(topwin, text=" Compare Stats on Directors/Actors ")
    frm1.grid(row=0, columnspan=7, sticky='W', \
                 padx=15, pady=5, ipadx=5, ipady=5)
    director1_label = Label(frm1, text="First Person: ")
    director1_label.grid(row=0, column=0, sticky='E', padx=9, pady=2)
    director1 = Entry(frm1, width = 30)
    director1.grid(row=0, column = 1, padx=20)
    lookup1_btn = Button(frm1, text="Lookup...",
                         command=lambda:lookup_fn1(director1.get()))
    lookup1_btn.grid(row=0, column=8, sticky='W', padx=5, pady=2)
    director2_label = Label(frm1, text="Second Person: ")
    director2_label.grid(row=1, column=0,sticky='E', padx=9, pady=2)
    director2 = Entry(frm1, width = 30)
    director2.grid(row=1, column = 1, padx=20)
    lookup2_btn = Button(frm1, text="Lookup...",
                         command=lambda:lookup_fn1(director2.get()))
    lookup2_btn.grid(row=1, column=8, sticky='W', padx=5, pady=2)
   
    btn1 = Button(frm1, text="Compare Directors",
                  command=lambda:compare_directors(director1.get(),director2.get()))
    btn1.grid(row=15, column=1)

    btn2 = Button(frm1, text="Compare Actors",
                  command=lambda:compare_actors(director1.get(),director2.get()))
    btn2.grid(row=16, column=1)

    

    frm2=LabelFrame(topwin, text=" Genre Percentages")
    frm2.grid(row=17, columnspan=7, sticky='W', \
                 padx=15, pady=5, ipadx=5, ipady=5)
    director3_label = Label(frm2, text="Person: ")
    director3_label.grid(row=17, column=0, sticky='E', padx=33, pady=2)
    director3 = Entry(frm2, width = 30)
    director3.grid(row=17, column = 1, padx=20)
    lookup3_btn = Button(frm2, text="Lookup...",
                         command=lambda:lookup_fn1(director3.get()))
    lookup3_btn.grid(row=17, column=8, sticky='W', padx=5, pady=2)
   
    btn1 = Button(frm2, text="Director",
                  command=lambda:director_genres(director3.get()))
    btn1.grid(row=18, column=1)

    btn2 = Button(frm2, text="Actor",
                  command=lambda:actor_genres(director3.get()))
    btn2.grid(row=19, column=1)


    frm3=LabelFrame(topwin, text=" Six Degrees of Separation ")
    frm3.grid(row=20, columnspan=7, sticky='W', \
                 padx=15, pady=5, ipadx=5, ipady=5)
    actor1_label = Label(frm3, text="First Actor: ")
    actor1_label.grid(row=20, column=0, sticky='E', padx=14, pady=2)
    actor1 = Entry(frm3, width = 30)
    actor1.grid(row=20, column = 1, padx=20)
    lookup3_btn = Button(frm3, text="Lookup...",
                         command=lambda:lookup_fn1(actor1.get()))
    lookup3_btn.grid(row=20, column=8, sticky='W', padx=5, pady=2)
    actor2_label = Label(frm3, text="Second Actor: ")
    actor2_label.grid(row=21, column=0,sticky='E', padx=14, pady=2)
    actor2 = Entry(frm3, width = 30)
    actor2.grid(row=21, column = 1, padx=20)
    lookup4_btn = Button(frm3, text="Lookup...", command=lambda:lookup_fn1(actor2.get()))
    lookup4_btn.grid(row=21, column=8, sticky='W', padx=5, pady=2)
   
    btn1 = Button(frm3, text="Connect Actors",
                  command=lambda:six_degrees_fn(actor1.get(),actor2.get()))
    btn1.grid(row=22, column=1)
    
    
    topwin.mainloop()
    return


# Open connection to database
conn = connect_db()
if conn != None:
    print('Connected')
    # Open a cursor
    cursor = conn.cursor()

    mainwin()
    conn.close()

