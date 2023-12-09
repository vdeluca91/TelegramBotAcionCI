from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application,Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler, ContextTypes
from datetime import datetime, timedelta

from logging import Logger
from src.lib.MySQLclass import *
db = MySQLDatabase()
# Definizione degli stati
NAME, PHONE, RESERVED_SEATS, DAY, TIME_SLOT, CONFIRMATION, BUTTON_HANDLER = range(7)

