from os import getenv
from dotenv import load_dotenv

load_dotenv()
bot_token = getenv('TELEGRAM_TOKEN')
stripe_token = getenv('STRIPE_TOKEN')
mail_login = getenv('MAIL_LOGIN')
mail_password = getenv('MAIL_PASSWORD')
mail_app_pass = getenv('MAIL_APP_PASS')
# id
admins = [5181177911, 1449983348]
staff = [608871088, 1449983348]
