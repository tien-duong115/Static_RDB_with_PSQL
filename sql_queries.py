# DROP TABLES

songplay_table_drop = "songplay_table"
user_table_drop = "user_table"
song_table_drop = "song_table"
artist_table_drop = "artist_table"
time_table_drop = "time_table"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_table (songplay_id SERIAL PRIMARY KEY NOT NULL,\
start_time timestamp Not null , 
user_id int NOT NULL, 
level varchar NULL, 
song_id VARCHAR  NOT NULL, 
artist_id varchar NOT NULL, 
session_id int NOT NULL, 
location varchar NULL, 
user_agent varchar NULL);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users_table \
( user_id int PRIMARY KEY NOT NULL  , 
first_name varchar NOT null  ,
last_name varchar NOT NULL  ,
gender varchar NOT NULL , 
level varchar NOT NULL );
""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists_table \
(artist_id  varchar PRIMARY KEY NOT NULL ,
name varchar ,
location varchar ,
latitude decimal ,
longtitude decimal);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song_table \
( song_id VARCHAR PRIMARY KEY  NOT NULL ,
title varchar, 
artist_id varchar ,
year int ,
duration decimal);
""")


time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table ( start_time timestamp PRIMARY KEY NOT NULL \
,hour int 
,day int 
,week int 
,month int 
,year int 
, weekday int);
 """)

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplay_table (
                            start_time, \
                            user_id, \
                            level, \
                            song_id, \
                            artist_id, \
                            session_id, \
                            location, \
                            user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = (""" INSERT INTO users_table \
(user_id
,first_name 
,last_name 
,gender 
, level) VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (user_id)
DO
    UPDATE SET user_id = users_table.user_id
""")

song_table_insert = (""" INSERT INTO song_table \
(song_id 
,title 
,artist_id 
,year 
,duration) VALUES (%s,%s,%s,%s,%s)
""")

artist_table_insert = (""" INSERT INTO artists_table \
(artist_id 
,name 
,location 
,latitude 
,longtitude) VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (artist_id)
DO 
    UPDATE SET artist_id = EXCLUDED.artist_id || ',' || artists_table.name;
""")


time_table_insert = ("""INSERT INTO time_table \
(start_time 
,hour 
,day 
,week 
,month 
,year 
,weekday) VALUES (%s, %s,%s,%s,%s,%s, %s)

ON CONFLICT (start_time)
DO 
    UPDATE SET start_time = time_table.start_time
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id 
,a.artist_id 
FROM song_table AS s 
LEFT JOIN artists_table AS a 
ON a.artist_id = s.artist_id 
WHERE 
s.title = (%s) AND 
a.name = (%s)  AND 
s.duration = (%s);
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]



