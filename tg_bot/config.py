from environs import Env


env = Env()
env.read_env()

"""Tokens"""
BOT_TOKEN = env.str("BOT_TOKEN")


"""Redis"""
redis_host = env.str("REDIS_HOST", None)
redis_port = env.str("REDIS_PORT", None)


"""Django"""
super_user_name = env.str("SUPER_USER_NAME")
super_user_pass = env.str("SUPER_USER_PASS")


"""Settings UKassa"""
PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")
UKASSA_SECRET_KEY = env.str("UKASSA_SECRET_KEY")
SHOP_ID = env.str("SHOP_ID")


"""Pagination settings"""
PAGINATION_ITEMS: int = 3
