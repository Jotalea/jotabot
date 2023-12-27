import os
# You can change the color of the embeds
embed_color = 0x9bff30
# Update the bot's version
bot_version = "4.9.5"
# User ID of the bot owner
admin_id = os.environ['OWNER-ID']
# Conversation logging
printlog = True
logging = True
use_async = True
log_webhook = os.environ['WEBHOOK']
# Access to my computer
allowed_users = [admin_id]
ssh_password = os.environ['SSH-PASSWORD']