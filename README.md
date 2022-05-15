
# Telegram Music Downloader
A Simple Music Downloader Bot For Telegram with Youtube Music, Spotify & Deezer Support.

<p align="center">
    <a href="https://python.org">
        <img src="http://forthebadge.com/images/badges/made-with-python.svg" alt="made-with-python">
    </a>
    <a href="https://GitHub.com/rozari0">
        <img src="http://ForTheBadge.com/images/badges/built-with-love.svg" alt="built-with-love">
    </a> <br>
    <img src="https://img.shields.io/github/license/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="LICENSE">
    <img src="https://img.shields.io/github/contributors/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="Contributors">
    <img src="https://img.shields.io/github/repo-size/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="Repository Size"> <br>
    <img src="https://img.shields.io/badge/python-3.9-green?style=for-the-badge&logo=appveyor" alt="Python Version">
    <img src="https://img.shields.io/github/issues/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="Issues">
    <img src="https://img.shields.io/github/forks/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="Forks">
    <img src="https://img.shields.io/github/stars/rozari0/MusicDownloader?style=for-the-badge&logo=appveyor" alt="Stars">
</p>



## Demo

[You Need Music?](https://t.me/NeedMusicRobot)


## Deployment

To deploy this project run

### Easy Way (Local)
```bash
  cp sample_config.env config.env
  pip3 install -r requirements.txt
  python3 -m mbot
```

### Docker
```bash
  cp sample_config.env config.env
  docker build . -t musicbot
  docker run musicbot
```
### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/rozari0/MusicDownloader/)

## Environment Variables

To run this project, you will need to add the following environment variables to your config.env file

`API_ID`
`API_HASH`
`BOT_TOKEN`
`SPOTIPY_CLIENT_ID`
`SPOTIPY_CLIENT_SECRET`
`UPDATES_CHANNEL`
`LOG_GROUP`
`DATABASE_URL`
`AUTH_CHATS`



## License

[MIT](https://choosealicense.com/licenses/mit/)

