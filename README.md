# Create RSS/Atom feed for Telegram channel

<code> ⚠️ <b>Warning! This code was made a long time ago, lots of API changes happened since then, making some parts of this code useless. For example, bots can already read messages in channels.</b> </code>

This code allows you to form an RSS feed when you post messages to channel via bot. It works fine for me, but there can be some bugs.  
In theory, devs can use this to form RSS/Atom feed for their channels to make content available outside Telegram.

## Prerequisites
* Python 3;
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/) lib to work with Telegram [Bot API](https://core.telegram.org/bots/api);
* [pytz](http://pytz.sourceforge.net/) library to work with timezones;
* [feedgen](https://github.com/lkiesow/python-feedgen) library to create RSS/Atom feeds;
* [CherryPy](http://www.cherrypy.org/) Micro web-server (to use webhooks);
* sqlite3;
* (optional) [nginx](http://nginx.org/) as reverse-proxy

## Installation
To install feedgen you need 1024+ megabytes of RAM, also you need to install some libs first:  

```
sudo apt-get install sqlite3 libxml2 libxml2-dev libxslt1.1 libxslt1.1-dev  
pip3 install feedgen pytz pytelegrambotapi cherrypy  
sqlite3 storage.db < create_db.sql
```

1. Rename `config_example.py` to `config.py` (**Important**)
2. Fill in the necessary fields in `config.py` file
3. Launch bot using webhooks with self-signed certificate (`sample_custom_post.py`) or check sample auto-posting bot (`sample_hourly.py`)

Check that your bot is set as admin in your channel!  
If using custom poster, open chat with your bot and write a message to it. You should see that message in both channel and RSS/Atom feed.

## Notes and restrictions

* It's still unknown, why some RSS Parsers take too long to find updates in feed (though [QuiteRSS](https://quiterss.org/en/node) for Windows finds updates instantly)
* In this version of code, you can only remove one entry from feed at a time. No way to also remove message from channel, only manually with `/remlast` command (Restriction of Bot API).
* Only text messages are supported.
* `parse_mode` argument is set to "HTML" by default (to be compatible with real RSS readers). You can disable it in code or change to "Markdown".

## Any questions?
The code provided here should be self-explanatory, but in case you get stuck somewhere, feel free to e-mail me: groosha @ protonmail.com (remove extra spaces)
