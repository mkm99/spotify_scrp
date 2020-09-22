import requests
from bs4 import BeautifulSoup
import mysql.connector


# function writes headers on a file
def write_headers(filename, headers):
    handle = open(filename, "w")
    handle.write(headers)
    print(filename + " has been created.")


# function that will write info in the file
def write_in_file(filename, text):
    handle = open(filename, "a")
    handle.write(text)


"""
Variables
"""
url = 'https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp'
csv_file = "spotify.csv"
html_file = "spotify.html"
host = 'localhost'
user = 'root'
password = ''
port = '3306'
database = 'spotify_scrp'

# grabbing all data from given url
data = requests.get(url).text

# formatting the data to parse
soup = BeautifulSoup(data, 'html.parser')

"""
This section the script writes the headers on the csv file and html file
"""

# Writing in the csv file
csv_headers = "position_num, song_name, artist_name, explicit, album_name, duration\n"
write_headers(csv_file, csv_headers)

# Writing in the html file
html_headers = "<html>\n" \
               "<head>\n" \
               "\t<title>Spotify Top 30</title>\n" \
               "\t<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">\n" \
               "</head>\n" \
               "<body>\n" \
               "<h1 class = \"centered-title\">Spotify Top 30</h1>\n" \
               "<table>\n" \
               "\t<tr class = \"headers\">\n" \
               "\t\t<th><a href=\"sort.php?sort=position\">Position</a></th>\n" \
               "\t\t<th><a href=\"sort.php?sort=song_name\">Song</a></th>\n" \
               "\t\t<th><a href=\"sort.php?sort=artist_name\">Artist</a></th>\n" \
               "\t\t<th><a href=\"sort.php?sort=explicit\">Explicit</a></th>\n" \
               "\t\t<th><a href=\"sort.php?sort=album_name\">Album</a></th>\n" \
               "\t\t<th><a href=\"sort.php?sort=duration\">Duration</a></th>\n" \
               "\t</tr>\n\n"

write_headers(html_file, html_headers)


"""
This section extracts all the information found on the page
"""

# grabbing all lines where <li> tag exists which includes each songs' info
songs_raw = soup.find_all('li')

# iterate on every line to extract the info
for song in songs_raw:
    # get the position of the song
    position = song.get('data-position')

    # get the song's title
    title = song.find('div', class_='tracklist-col name').div.span.text

    # The song might have a coma "," and it gives problems on the csv file
    # So it is being replaced by a "/"
    title = title.replace(",", "/")
    title = title.replace("\'", "")  # line added (09/22/20) to avoid problems with mysql

    # Here is all the info from artists and album
    singers_container = song.find('span', class_='artists-albums')

    # All possible <a> tags that contains the name of the artist and the album
    singers_data = singers_container.find_all('a')

    # making a list that contains the artist and the album's name
    singers_list = []

    for singer in singers_data:
        # saving singers' name and album into a list
        singers_list.append(singer.text)

    # last element in the list is the album
    album = singers_list.pop()

    # album might contain collaborators, which includes a "," or "'"
    # which has to be replaced so it won't give trouble with the csv file
    album = album.replace(",", " / ")
    album = album.replace("\'", "")

    # string which will contain the artists' names
    artists_name = ' - '

    # how many artists for the song
    size = len(singers_data)

    # only 1 singer
    if size == 2:
        artists_name = singers_list[0]
    # more than 1 singer
    else:
        artists_name = artists_name.join(singers_list)

    # took care of comas in artists name which gave errors with csv file (09/22/20)
    artists_name = artists_name.replace(",", " / ")

    # getting the duration of each song
    duration = song.find('span', class_='total-duration').text

    # grab the tag where contains info if the song is explicit or not
    find_explicit = song.find('div', class_='tracklist-col explicit')

    explicit = 'N'

    # it will say "Y" if song is explicit
    if str(find_explicit).find("Explicit") != -1:
        explicit = 'Y'

    """
    Writing all the information in the csv file
    """
    csv_text = position + "," + title + "," + artists_name + "," + explicit + "," + album + "," + duration + "\n"
    write_in_file("spotify.csv", csv_text)


"""
This part the csv file is opened and read to extract the information
Connection to the database and saving all info in it
Creation of the html file 
"""

try:

    # Connecting to the database
    my_db = mysql.connector.connect(host=host, user=user, password=password, port=port, database=database)

    # creating a cursor
    cur = my_db.cursor()

    # Dropping the table if it already exists
    cur.execute("DROP TABLE IF EXISTS top30")

    # Building the query to create the table
    sql_query = "CREATE TABLE top30 (position int(30), song_name varchar(60), " \
                "artist_name varchar(80), explicit char(1), album_name varchar(80), " \
                "duration varchar(5), PRIMARY KEY ( song_name ))"

    # execute the query
    cur.execute(sql_query)
    print("Table Created Successfully")

    # Open the csv file to read the content
    lines = open(csv_file, "r")

    # skip first line of csv file which contains the headers
    next(lines)

    # each line has all the information as a string, separated by a coma
    for line in lines:
        # Saving the information in a list
        values = line.split(',')

        # Getting the information from the list
        position = values[0]
        song_name = values[1]
        artist = values[2]
        explicit_y_n = values[3]
        album_name = values[4]
        duration = values[5].replace('\n', "")

        html_text = "\t<tr>\n" \
                    "\t\t<td class = \"position\">" + position + "</td>\n" \
                    "\t\t<td>" + song_name + "</td>\n" \
                    "\t\t<td>" + artist + "</td>\n" \
                    "\t\t<td class = \"explicit\">" + explicit_y_n + "</td>\n" \
                    "\t\t<td>" + album_name + "</td>\n" \
                    "\t\t<td class = \"duration\">" + duration + "</td>\n" \
                    "\t</tr>\n\n"

        # writing all information in the HTML file
        write_in_file(html_file, html_text)

        # Getting the duration and cleaning the variable
        duration = values.pop()
        duration = duration.replace('\n', "")

        # Making a string of the list
        subQ = "','"
        values = subQ.join(values)

        # Building the query
        sql_query = "INSERT into top30(position, song_name, artist_name, explicit, album_name, duration)" \
                    " values('" + values + "','" + duration + "')"

        # Execute the query
        cur.execute(sql_query)

    # Ending the connection with the database
    my_db.close()

    # Closing tags for the html file
    html_text = "</table>\n" \
                "</body>\n" \
                "</html>"

    # Write in the html file the closing tags
    write_in_file(html_file, html_text)

    print("Information has been added to the database")

except mysql.connector.Error as e:
    print("No connection to database")