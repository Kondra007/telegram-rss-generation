# -*- coding: utf-8 -*-

channel_id = "@yourchannel" # @username for public channels / chat_id for private channels
token = "token"  # Your bot's token from @BotFather
db_name = "storage.db"  # Name of SQL Database to use
number_of_entries = 15  # How many entries will be included in RSS
admin_ids = [111111, 2222222]  # Allow only people with these IDs to post messages to channel via bot.
webhook_url = "https://example.com/mywebhook/" # URL to set webhook

# --- RSS Config values ---
author_name = "Mr Jack"  # Your name
author_email = "jack@example.com"  # Your e-mail
timezone = 'GMT' # Find yours from here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
bot_link = "https://telegram.me/yourchannel"  # Using your bot URL as ID and Link
feed_link = "https://example.com/rss/atom.xml"  # Self link to RSS/Atom
feed_description = "Your Description"
feed_title = "Your title"
feed_language = "en"  # Optional feed language value