[![tgflix](app/static/img/app.png)](https://github.com/xw108/TGFlix.git)
> A simple python3 Web App which serve files from telegram groups in a better organised way.

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](.)  [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

## Highlights

* Fully controlable from telegram
* Categorization based on Movie,Series,Genre,Season,Episodes,Quality,Size,etc...
* View files on the browser.
* Search through the movie list.
* Download/Stream files.

## Demo

Hosted [demo site](https://tgflix.herokuapp.com/)

-----------

## Deploy Guide ( Local machine )

* **Clone to local machine.**

    ``` bash
    git clone https://github.com/xw108/TGFlix.git
    cd tgflix
    ```

* **Setup virtual environment.**

    ``` bash
    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```

* **Install dependencies.**

    ``` bash
    pip3 install -r requirements.txt
    ```

* **Environment Variables.**

    Export the following enviornment variables


* **Setup Database**

    ``` bash
    psql $DATABASE_URL < scripts/migrate.sh
    ```

* **Run app.**

    ``` bash
    uvicorn app.main:app
    ```

## Deploy Guide ( Heroku )

* **Fork this repo**
* **Create new [heroku](https://www.heroku.com) app & deploy from the forked repo**
* **Add postgres databse**
* **Setup the enviornment variables**
* **Setup Database**

    Run this command

    ``` bash
    psql $DATABASE_URL < scripts/migrate.sh
    ```
* **Re-deploy the app**


## Enviornmental Variables
| Name | Value | Required
|------------- | ------------- | -------------
| `DEBUG` | Set to False in production |
| `TG_APP_ID` | Telegram api_id obtained from <https://my.telegram.org/apps>.|✔
| `TG_APP_HASH` | Telegram api_hash obtained from <https://my.telegram.org/apps>.|✔
| `ADMIN_UID` | Userid of admin user.Can be obtained from msg details.|✔
| `SESSION_STRING` | Can be obtained by running `python3 scripts/gen_sess_string.py`.|✔
| `DATABASE_URL` | Postgres database url.|✔
| `APP_NAME` | Name of your app.
| `APP_DESC` | Description for your app.
| `APP_URL` | public url of your app.|✔
| `MAX_ITEMS_PER_PAGE` | Number of results to be shown per page (default 20).
| `MAX_SIMULTANIOUS_DOWNLOAD` | Number of parallel downloads allowed (default 20).
| `DOWNLOAD_ENABLED` | Disable or Enable download (default True).

## Documentation

[Check out this](docs.md)

## Features of free version

- [x] Series/Movies
- [x] Parts/Seasons and Episodes
- [x] Genres
- [x] Quality & Size
- [x] Hide/Show
- [ ] File download/stream
- [ ] Telegram download
- [ ] Auto Posting
- [ ] User login
- [ ] Ratings & Review
- [ ] Staring
- [ ] Web admin

## Contributions

Contributions are welcome.

## Contact

You can contact me [@xw108](https://tx.me/xw108).

## License

Code released under [The GNU General Public License](LICENSE).