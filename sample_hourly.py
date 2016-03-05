#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is an example of using Feedgen and pyTelegramBotAPI to send messages to channel
as well as creating an RSS Feed.

Automatically posts current time every hour to your channel and updates RSS.
You can set this script to a cron: 0 * * * * cd /path/to/your/bot/ && python3 sample_hourly.py
"""

from time import gmtime
import telebot
import config
import pytz
from datetime import datetime
from feedgen.feed import FeedGenerator
from email.utils import formatdate
import dbhelper

bot = telebot.TeleBot(config.token)
    
    
def generate_feed():
    tz = pytz.timezone(config.timezone)
    # Get latest X entries from database
    entries = dbhelper.get_latest_entries()

    fg = FeedGenerator()
    # Feed id
    fg.id(config.bot_link)
    # Creator info (for Atom)
    fg.author(name=config.author_name, email=config.author_email, replace=True )
    # Self link to the feed
    fg.link(href=config.feed_link, rel='self')
    # Set description of your feed
    fg.description(config.feed_description)
    # Last time feed updated (use system time with timezone)
    fg.lastBuildDate(formatdate(datetime.timestamp(datetime.now(tz)), localtime=True))
    fg.title(config.feed_title)
    # Set time-to-live (I really don't know why set this)
    fg.ttl(5)
    # Does this parameter mean anything?
    fg.language(config.feed_language)
    
    for entry in entries:
        item = fg.add_entry()
        # Use message id to form valid URL (new feature in Telegram since Feb 2016)
        item.id("{!s}".format(entry["pid"]))
        item.link(href="{!s}/{!s}".format(config.bot_link, entry["pid"]), rel="alternate")
        # Set title and content from message text
        item.title(entry["ptext"])
        item.content(entry["ptext"])
        # Set publish/update datetime
        item.pubdate(entry["pdate"])
        item.updated(entry["pdate"])

    # Write RSS/Atom feed to file
    # It's preferred to have only one type at a time (or just create two functions)
    fg.atom_file('static/atom.xml')
    # fg.rss_file('static/rss.xml')

if __name__ == '__main__':
    message = "It\'s <b>{!s}</b> o\'clock! (GMT)".format(gmtime().tm_hour)
    msg = bot.send_message(config.channel_id, message, disable_notification=True, parse_mode="HTML")
    tz = pytz.timezone(config.timezone)
    dbhelper.insert(message, formatdate(datetime.timestamp(datetime.now(tz)), localtime=True), msg.message_id)
    generate_feed()
    