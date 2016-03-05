#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is an example of using Feedgen and pyTelegramBotAPI to send messages to channel
as well as creating an RSS Feed.
Note that to add new items to feed, you need to post via bot (not directly to channel).

This example uses Webhooks method.
"""

import cherrypy
import pytz
from datetime import datetime
from feedgen.feed import FeedGenerator
from email.utils import formatdate
import random
import telebot
import config
import dbhelper
from cherrypy.lib.static import serve_file

bot = telebot.TeleBot(config.token)


WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

"""
Quick'n'dirty SSL certificate generation:

openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
with the same value in you put in WEBHOOK_HOST
"""

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


@bot.message_handler(commands=["remlast"])
def remove_last_entry(message):
    if message.chat.id in config.admin_ids:
        dbhelper.remove_last_entry()
        generate_feed()

        
# Handle only text messages
@bot.message_handler(func=lambda message: message.chat.id in config.admin_ids, content_types=["text"])
def my_text(message):
    # We don't need this crap in channel
    if message.text == "/start":
        return
    tz = pytz.timezone(config.timezone)
    msg_to_channel = bot.send_message(config.channel_id, message.text, parse_mode="HTML")
    dbhelper.insert(message.text.replace("\n","<br />"), formatdate(datetime.timestamp(datetime.now(tz)), localtime=True), msg_to_channel.message_id)
    generate_feed()

    
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length)
        json_string = json_string.decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        if update.message:
            bot.process_new_messages([update.message])
        if update.inline_query:
            bot.process_new_inline_query([update.inline_query])
            
    @cherrypy.expose
    def rss(self):
        # Return static file with ATOM feed
        return serve_file("/bots/telegram-feedgen-bot/static/atom.xml")
    
    
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

    # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()

    # Set webhook
    bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
                
    print("Webhook set")            

    # Start cherrypy server
    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV,
        'engine.autoreload.on': False
    })

    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
