import openai
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler



# Set up OpenAI credentials


# Define a function to handle the /start command


def start(update, context):
    keyboard = [[InlineKeyboardButton("English 🇺🇸", callback_data='English'),
                 InlineKeyboardButton("Hindi 🇮🇳", callback_data='Hindi')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi! I'm a chatbot powered by CSR DATABASE. Please select your preferred language:",
                             reply_markup=reply_markup)


def language_selection(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"You selected: {query.data}")
    context.user_data['language'] = query.data

# Define a function to handle user messages
def ask(update, context):
    # Get user's message
    user_message = " ".join(context.args)
    print(user_message)
    # Generate a response using OpenAI's GPT-3 module
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=user_message,
        max_tokens=1024,
        n=2,
        stop=None,
        temperature=0.05,
    )
    # Extract the answer from the response
    answer = response.choices[0].text.strip()
    ans=user_message+"\n \n"+"Answer From Database : "+"\n \n"+answer +"\n \n"
    # Send the answer back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=ans)
    print(ans)

# Define a function to handle errors
def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oops! Something went wrong.")


# Define a function to handle the /help command
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="To ask a question, type /ask followed by your question.")

# Set up the Telegram bot
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Add handlers for commands, messages, and errors
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

ask_handler = CommandHandler('ask', ask)
dispatcher.add_handler(ask_handler)

error_handler = MessageHandler(Filters.all, error)
dispatcher.add_error_handler(error_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(language_selection))

# Add a handler for the /help command
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# Start the bot
updater.start_polling()
updater.idle()
