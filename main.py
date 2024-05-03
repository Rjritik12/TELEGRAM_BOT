import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from queue import Queue
import json

def load_pokemon_data() -> dict:
    with open('pokemon_data.json') as f:
        pokemon_data = json.load(f)
    return pokemon_data

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Hello! I\'m Brock, the gym leader from the Pokemon series. Welcome to our group!'
    )

def handle_new_member(update: Update, context: CallbackContext) -> None:
    new_member = update.message.new_chat_members[0]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Welcome to the group, {new_member.first_name}! I\'m Brock, the gym leader from the Pokemon series. Do you have a favorite Pokemon? I\'d love to hear about it!'
    )

def handle_favorite_pokemon(update: Update, context: CallbackContext) -> None:
    favorite_pokemon = update.message.text
    if favorite_pokemon.lower() in pokemon_data:
        characteristic = pokemon_data[favorite_pokemon.lower()]['characteristic']
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'That\'s a great choice! I\'ve always admired {favorite_pokemon} for its {characteristic}.'
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='I\'m sorry, I don\'t recognize that Pokemon. Could you please try again?'
        )

def main() -> None:
    global pokemon_data
    pokemon_data = load_pokemon_data()
    update_queue = Queue()

    # Get bot token from user input
    while True:
        token = input("Enter your Telegram Bot Token: ")
        if token:
            break
        else:
            print("Please enter a valid bot token.")

    print(token)  # Print for verification (optional)

    updater = Updater(token, use_context=True)  # Assuming you have updated telegram.ext

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.StatusUpdate.new_chat_members, handle_new_member))
    dispatcher.add_handler(MessageHandler(filters.Text & (~filters.Command), handle_favorite_pokemon))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
