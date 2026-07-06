from discogs_api import discogs_client
from database import initialiseDB
from releases import Releases

def checkTitleInDatabase(connection, title: str, release_format = None):
    sql_query = "SELECT * FROM RELEASE WHERE title = ? AND format = ?"
    cursor = connection.cursor()
    if release_format == None:
        sql_query = "SELECT * FROM RELEASE WHERE title = ?"
        data = cursor.execute(sql_query, (title,))
        return data.fetchall()
    data = cursor.execute(sql_query, (title, release_format,))
    return data.fetchall()

def addReleasesToDatabase(db_connection, release_list):
    sql = "INSERT INTO RELEASE (discog_id, title, year, tracklist, genre, format, image) SELECT discog_id, title, year, tracklist, genre, format, image FROM RELEASE WHERE title <> ? AND year <> ? AND tracklist <>? AND genre <> ? "
    cursor = db_connection.cursor()
    release_data = []
    for release in release_list:
        tracks = []
        formats = []
        for track in release.tracklist:
            tracks.append(track.title)
        for format in release.formats:
            formats.append(format['name'])
        release_data.append((release.title, release.year, ' '.join(tracks), ' '.join(release.genres), ' '.join(formats), "placeholder",))
    cursor.executemany(sql, release_data)
    db_connection.commit()

def searchReleaseByTitle(db_connection, title: str, release_format = None):
    database_check = checkTitleInDatabase(db_connection, title, release_format)
    print(len(database_check))
    if len(database_check) == 0:
        if release_format in ["CD", "Vinyl", "File"]: # Needs expanding?
            search_results = discogs_client.search(
                title, type="release", format=release_format
            )
            print(len(search_results))
        else:
            search_results = discogs_client.search(
                title, type="release"
            )
        
        release_list = []
        for result in search_results:
            if title in result.title:
                release_list.append(result)

        addReleasesToDatabase(db_connection, release_list)

        return release_list
    return database_check

db_connection = initialiseDB()

song_list = searchReleaseByTitle(db_connection, "Mezzanine", "CD")
print(len(song_list))