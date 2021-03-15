Instructions for Installation and Loading the Data


I used MySQL to handle the database for my application. To load the data into MySQL, first open MySQL and create a new, empty schema called “movies”. Then go to the Server tab and choose Data Import. Find the unzipped table files in the project folder and select those for import, select the movies schema to import the data tables into, and then click start import.


All of the following changes have already been made to the data included in the project file, so you don’t need to replicate any of these alterations.


One change I made to the original data in my database is the worldwide gross attribute. When I found the data online, it provided all monetary attributes as strings in order to describe what currency it was, such as $, GBP, FRF, JPY, etc. This prevented me from doing any sort of arithmetic to these values such as finding the min, max, or average. To fix this issue, I added a new attribute to the table called worldwide_gross_dollar. I converted this by first eliminating all data of movies with worldwide grosses recorded in other currencies (there were actually very few of these). I then took a substring to take everything after the dollar sign and casted this to a double.


All of the data initially started off as one single table, but I created additional tables in my database design to better handle the actors, directors, and genres. This was especially important for the genres and actors since they were in the original data table as a list for each movie. I separated them and indexed them in their own table so that I could query more easily for what actors and genres are in specific movies.


There were a ton of movies recorded in the original data, and I figured that a lot of it wasn’t useful and was just slowing down the queries and searches, so I decided to decrease the amount of data. I decided to delete all rows of movies that both didn’t have a recorded worldwide gross and had less than 10 thousand votes on IMDb, as these movies aren’t very relevant and may even skew the data.


I also replaced the original imdb_title_id attribute with a numerical movie_id attribute to simplify the primary key for the main movies table.


Instructions For Installing The Application Software


When installing all of the software listed below, make sure you’re installing with root access on your computer.


Python 3.85
This application runs on Python 3.85. The version seemed to be important as Python 3.9 didn’t seem to be compatible with pandas or matplotlib. This version of python can be found online at python.org. Make sure you check the box to add it to PATH.


Mysql-connector-python
This is what I used in my application to connect the MySQL database to the python program.
It can be installed with “pip install msql-connector-python”


Numpy
If you don’t already have numpy installed on your machine, you can install it with “pip install numpy” on the command line


Pandas
Pandas is what is used in my application to plot the graphs and charts. This can be installed with “pip install pandas” on the command line


Matplotlib
Matplotlib is required to use pandas. Install it on the command line with “pip install matplotlib”


Instructions for Running Application


One option for running the application is to open an IDLE window with Python, open the application’s python program, and click Run Module.


Another option is to do it on the command line by navigating to the application project folder and typing “python CS480_MovieProject.py”


What The Application Does And How To Use It


My application has two main features: a graphical way of displaying data about actors and directors, and connecting two actors together like the game “six degrees of separation”.


There are a few options for the user to graphically display the data. At the top of the application, there’s a box called “Compare Stats on Directors/Actors”. In this box the user enters the names of either two directors or two actors. Then, by hitting the correct compare button below, the application will pop up two new windows with a bar graph in each. One compares the two people by their lowest movie rating, highest movie rating, and average movie rating based on ratings from IMDb, and the other graph compares the two on their average movie gross and highest grossing movie.


The second option is the “Genre Percentages”. Once again, the user enters either the name of a director or the name of an actor into the box and selects the correct button. After hitting the button, a new window pops up displaying a pie chart of the distribution of movie genres that person has directed or starred in.


The “six degrees of separation” is the second feature of my application. This takes two designated actors by user and connects them together by movies they’ve been in. This game allows you to connect them by choosing multiple movies and actors in the middle. For example, you could connect George Clooney and Tom Hanks with: George Clooney > Ocean’s Eleven > Matt Damon > Saving Private Ryan > Tom Hanks. My application uses a breadth-first search algorithm to find these connections, and then displays the results in a vertical list in a separate window when it finds them. It should be noted that this search can take a long time, especially when it requires more degrees to connect the actors, so this can require some patience. If the user clicks anywhere while it’s searching (or sometimes just randomly), it will say the application is not responding, but it is still searching so ignore it. Be prepared to wait a few minutes if there’s no easy connection. I’d recommend sticking to well known actors unless you’re willing to wait.


All of the input boxes have a button next to it called “Lookup”. The user can enter part of a name and hit lookup if the user doesn’t remember their full name or can’t remember how to spell it. It will prompt for either an actor or director selection, and then list all of the actors/directors close to what was typed in. These can be used as reference or copied and pasted into the input box.