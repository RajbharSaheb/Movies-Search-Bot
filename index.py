# © https://t.me/CyniteBackup
import os
from io import BytesIO
from werkzeug.urls import url_quote
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from movies_scraper import search_movies, get_movie

TOKEN = os.getenv("TOKEN")
URL = "Get It From Vercel"
bot = Bot(TOKEN)

def welcome(update, context):
    update.message.reply_text(f"Hello {update.message.from_user.first_name}, Welcome To Shortner Fly Search Bot.\n"
                              f"🔥 Directly Search From The Bot.")
    update.message.reply_text("👇 Enter Any Movie or Series Name 👇")

def find_movie(update, context):
    search_results = update.message.reply_text("Searching...")
    query = update.message.text
    movies_list = search_movies(query)
    if movies_list:
        keyboards = [[InlineKeyboardButton(movie["title"], callback_data=movie["id"])] for movie in movies_list]
        reply_markup = InlineKeyboardMarkup(keyboards)
        search_results.edit_text('Here Is What I Found...', reply_markup=reply_markup)
    else:
        search_results.edit_text('Sorry, No Results Found')

def movie_result(update, context):
    query = update.callback_query
    movie_data = get_movie(query.data)
    response = requests.get(movie_data["img"])
    img = BytesIO(response.content)
    query.message.reply_photo(photo=img, caption=f"🎥 {movie_data['title']}")
    
    links = "\n\n".join(f"Open Link: {i}\n{movie_data['links'][i]}" for i in movie_data["links"])
    caption = f"⚡ Fast Download Links:\n\n{links}"
    
    if len(caption) > 4095:
        for x in range(0, len(caption), 4095):
            query.message.reply_text(text=caption[x:x+4095])
    else:
        query.message.reply_text(text=caption)

def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.text, find_movie))
    dispatcher.add_handler(CallbackQueryHandler(movie_result))
    return dispatcher

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    return "webhook setup ok" if s else "webhook setup failed"
