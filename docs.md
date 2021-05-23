[![tgflix](app/static/img/app.png)](https://github.com/xw108/TGFlix.git)
> A simple python3 Web App which serve files from telegram groups in a better organised way.



## Highlights
* Insert Movie, Series, Genres
* Delete Movie, Series, Genres
* Toogle public visibility of  Movie, Series
* Set part/season
* Enable/Disable Download

## Movies/Series

| Command | Description 
|---------|---------------
|` /ism` | Set to uploading movies.
|` /iss ` | Set to uploading series.
|` /p {part} ` | Set to upload part. eg : `/p6` to upload part 6
|` /s {season} ` | Set to upload season. eg : `/s6` to upload season 6
|` /mshow {id} ` | Make movie/series visible. eg : `/mshow 6` to make the movie with `id 1` visible.
|` /mhide {id} ` | Make movie/series hidden.
|` /mdel {id} ` | Delete movie/series.



## Files

| Command | Description 
|---------|---------------
|` /eshow {id} ` | Make file visible. eg : `/eshow 6` to make the series with `id 1` visible.
|` /ehide {id} ` | Make file hidden.
|` /edel {id} ` | Delete file.

## Genre

| Command | Description 
|---------|---------------
|` /genre {name}\|{description}\|{img_url} ` | Create new genre.See [below](#new-genre) for more details
|` /gdel {id} ` | Delete genere


## Other

| Command | Description 
|---------|---------------
|` /info ` | Get current uploading deatils  
|` /set {id} ` | Set current uploading to `id`. eg : `/set 6` to upload movie/series having `id 6`


# Examples

>Remember that bot should have admin rights &  all the commands should be send from groups

* ### New Movie/Series

    Movie details should be added along with the cover image as caption.

    ![new-movie](https://i.ibb.co/6J2X9Gf/new-movie.jpg)

    #### Format
    `{title}|{genre1,genre2,...}|{description}`

* ### New File
    After adding/loading movie just forward/upload the file

    >Episode number and file quality should be tagged along

    ![new-file](https://i.ibb.co/tz1jqrD/new-file.jpg)

* ## New Genre 
    Genre details should be added along with the cover image as caption or image url can be added after description.

    ![#new-genre](https://i.ibb.co/hR5VPyZ/newg.jpg)

    or 

    ![new-genre-url](https://i.ibb.co/c87Pjx8/newgu.jpg)


    #### Format
    `{title}|{description}|{img_url}`
    >If message includes photo img_url can be discarded