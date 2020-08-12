# Spotify Top 30
In this project, I scraped information from Spotify's website.
I grabbed the information from the top 50 songs each week, saved it
in a csv file and in a database. Then, the information is displayed
in a webpage that is able to sort the songs by position, song's name,
song's title, if they are explicit, and duration by clicking in the 
table's headers.
 

This project implements three scripts:

- spotify.py: This script is in charge of grabbing the information from the webpage, and 
gets the information of each song. Additionally, the script writes a csv file and a 
HTML file. Then the script opens the csv file and gets the information saved in there
and makes a connection to a database and saves all the information in the database as well.

- sort.php: This script is used when the user clicks on the headers to sort the songs as needed.

- style.css: Helps with formatting of the webpage created.


# Video
<a href="https://youtu.be/nx1HSNKCGa8" target="_blank" rel="noopener">Walk through video</a>