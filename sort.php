<html>
<head>
    <title>Spotify Top 30</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<h1 align="center">Spotify Top 30</h1>
<table align = "center">


<?php

# Variables
$host = "localhost";
$user = "root";
$sqlPass = "";
$dbName = "spotify_scrp";
$port = "3306";
$file_name = "spotify.csv";

# Connecting to the database to request information
$connect = mysqli_connect($host, $user, $sqlPass, $dbName, $port) or die ("Connection Failed");

# Making the headers and adding links back to the file to build the queries
echo "<tr class = \"headers\">
        <th><a href=\"sort.php?sort=position\">Position</a></th>
        <th><a href=\"sort.php?sort=song_name\">Song</a></th>
        <th><a href=\"sort.php?sort=artist_name\">Artist</a></th>
        <th><a href=\"sort.php?sort=explicit\">Explicit</a></th>
        <th><a href=\"sort.php?sort=album_name\">Album</a></th>
        <th><a href=\"sort.php?sort=duration\">Duration</a></th>
    </tr>";


$query = "SELECT * FROM top30";

# Depending of the selection of how to sort, the information is displayed using the pre-built queries
if ((isset($_GET['sort']) && $_GET['sort'] == 'position'))
{
    $query .= " ORDER BY position;";
}
elseif ((isset($_GET['sort']) && $_GET['sort'] == 'song_name'))
{
    $query .= " ORDER BY song_name";
}
elseif ((isset($_GET['sort']) && $_GET['sort'] == 'artist_name'))
{
    $query .= " ORDER BY artist_name";
}
elseif((isset($_GET['sort']) && $_GET['sort'] == 'explicit'))
{
    $query .= " ORDER BY explicit, album_name, song_name";
}
elseif((isset($_GET['sort']) && $_GET['sort'] == 'album_name'))
{
    $query .= " ORDER BY album_name";
}
elseif((isset($_GET['sort']) && $_GET['sort'] == 'duration'))
{
    $query .= " ORDER BY duration";
}

# Executing the query
$cursor = $connect->query($query);

# Displaying the information
while ($row = $cursor->fetch_assoc()) {
    /*[position], [song_name], [artist_name], [explicit], [album_name], [duration]*/
    $line = "<tr>
                  <td class= \"position\">" . $row['position'] . "</td>
                  <td>" . $row['song_name'] . "</td>
                  <td>" . $row['artist_name'] . "</td>
                  <td class= \"position\">" . $row['explicit'] . "</td>
                  <td>" . $row['album_name'] . "</td>
                  <td class= \"position\">" . $row['duration'] . "</td>
                  </tr>\n";
    echo $line;
}

// Close connection
mysqli_close($connect);
?>

</table>
</body>
</html>