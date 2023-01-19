import telegram.ext
from secrets import TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


def start(update, context):
    update.message.reply_text('Hi! Im your therapist for today')
    update.message.reply_text("What's your name?")
    #pass


def get_chat_id(update,context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def handle_message(update, context):
    update.message.reply_text(f" Hello {update.message.from_user.username} What would you like to do? .")
    names = ['Discuss some issues', 'Speak to a real-life therapist', 'Pay bills']

    options = []
    for i in range(len(names)):
        update.message.reply_text(f"{i+1}) {names[i]}")
        options.append(
            InlineKeyboardButton(
                text=str(i + 1),
                callback_data=str(i + 1)
            )
        )

    reply = InlineKeyboardMarkup([options])
    context.bot.send_message(chat_id=get_chat_id(update,context),
                             text="What do you want to do?",
                             reply_markup=reply,)


def button(update, context):
    choice = update.callback_query
    choice.answer()
    context.bot.send_message(chat_id=get_chat_id(update,context),
                             text=f"You chose {choice.data}",)


def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    disp.add_handler(telegram.ext.CommandHandler("Start", start))
    disp.add_handler(CallbackQueryHandler(button))
    disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print("setup complete")
    main()


