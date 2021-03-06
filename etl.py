import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Process input data (1 JSON file) and insert into songs and
        artists tables.

    Keyword arguments:
    * cur --        reference to connected db.
    * filepath --   path to file to be processed.

    Output:
    * song_data in songs table.
    * artist_data in artists table.
    """
    # open song file
    df = pd.DataFrame(pd.read_json( filepath,
                                    lines=True,
                                    orient='columns'))
    
    # insert song record
    song_data = (   df.values[0][6],
                    df.values[0][7],
                    df.values[0][1],
                    df.values[0][9],
                    df.values[0][8])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = ( df.values[0][1],
                    df.values[0][4],
                    df.values[0][3],
                    df.values[0][2],
                    df.values[0][2])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Process input data (1 JSON file) and insert into songs and
        artists tables.

    Keyword arguments:
    * cur --        reference to connected db.
    * filepath --   path to file to be processed.

    Output:
    * time_data in time table.
    * user_data in users table.
    * songplay_data in songplay table.
    """
    # open log file
    df = pd.DataFrame(pd.read_json( filepath,
                                    lines=True,
                                    orient='columns'))
    df_orig = df

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = list(zip(   t.dt.strftime('%Y-%m-%d %I:%M:%S'),
                            t.dt.hour,
                            t.dt.day,
                            t.dt.week,
                            t.dt.month,
                            t.dt.year,
                            t.dt.weekday))
    column_labels = (       'start_time',
                            'hour',
                            'day',
                            'week',
                            'month',
                            'year',
                            'weekday')
    time_df = pd.DataFrame( time_data,
                            columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_data = df_orig.get([   'userId',
                                'firstName',
                                'lastName',
                                'gender',
                                'level'])
    # adjust column names
    user_data.columns = [   'user_id',
                            'first_name',
                            'last_name',
                            'gender',
                            'level']
    # remove rows with no user_id
    user_data_clean = user_data[user_data['user_id']!= '']
    user_data_clean = user_data_clean.dropna()

    # remove duplicates
    user_data_duplicates_removed = user_data_clean.drop_duplicates(
                                                        'user_id',
                                                        keep='first')
    user_df = user_data_duplicates_removed

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        start_time = pd.to_datetime(
                            row.ts,
                            unit='ms').strftime(
                            '%Y-%m-%d %I:%M:%S')
        songplay_data = (   start_time,
                            row.userId,
                            row.level,
                            str(songid),
                            str(artistid),
                            row.sessionId,
                            row.location,
                            row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Walk through the whole input data directory strcture,

    Keyword arguments:
    * cur --        reference to connected db.
    * conn --       parameters (host, dbname, user, password) to
                    connect the db.
    * filepath --   path to file to be processed
                    (data/song_data or data/log_data).
    * func --       function to be called (process_song_data or
                    process_log_data)

    Output:
    * console printouts of the data processing.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

    print('All {} files processed OK in {}'.format(num_files, filepath))
def main():
    """Connect to DB and call process_data (2x) to walk through
        all the input data (data/song_data and data/log_data).

#     Keyword arguments:
#     * None

#     Output:
#     * All input data processed in DB tables.
#     """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user= password=")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    


    conn.close()


if __name__ == "__main__":
    main()
