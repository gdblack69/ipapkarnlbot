import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext, ConversationHandler

MOVIE_INPUT, VERIFIED = range(2)

async def start(update: Update, context: CallbackContext) -> int:
    user_first_name = update.message.from_user.first_name
    image_url = "https://static.vecteezy.com/system/resources/previews/000/240/724/original/popcorn-machine-vector.jpg"

    await update.message.reply_text(
        "❗️Just Send Movie Name And Year Correctly.\n\n"
        "➠ Other BOTs : @iPapkornFbot"
    )

    caption = (
        f"Hey 👋 {user_first_name} 🤩\n\n"
        "🍿 Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Wᴏʀʟᴅ's Cᴏᴏʟᴇsᴛ Sᴇᴀʀᴄʜ Eɴɢɪɴᴇ!\n\n"
        "Here You Can Request Movie's, Just Send Movie OR WebSeries Name With Proper [Google](https://www.google.com/) Spelling..!!"
    )

    await update.message.reply_photo(
        photo=image_url,
        caption=caption,
        parse_mode='MarkdownV2'
    )
    return MOVIE_INPUT

async def handle_movie(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Join💥", url="https://t.me/major/start?startapp=1607381212"),
            InlineKeyboardButton("Verify✅", callback_data='verify✅'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Plz First Join The Group And Verify it To Continue 🕵️", reply_markup=reply_markup)
    return VERIFIED

async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'verify✅':
        await query.edit_message_text(text="😍Great Now You Are All Set, Just Send The Movie Name And Year Correctly 🤗")
    return VERIFIED

async def handle_after_verify(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("❗Due To Heavy Load We Have Now Upgraded Our Bot to Response More Efficiently 😊")
    await update.message.reply_text("Just Send Your Movie Name In Our New Upgraded Bot 💪 @iPapkornFbot")
    return VERIFIED

async def repeat_message(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Just Send Your Movie Name In Our New Upgraded Bot 💪 @iPapkornFbot")
    return VERIFIED

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "We're excited to inform you that we've upgraded our bot to better serve your needs. "
        "To ensure a smoother and more efficient experience, we invite you to join us at our new bot, @iPapkornFbot.\n\n"
        "Thank you for your continued support🫶\n\n"
        "Best regards,\n"
        "iPapKornBot"
    )

async def feedback_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Please Let Us Know How Was Your Experience By Sending Your Feedback In Our Main Channel @iPapkornFbot 🤧"
    )

async def error_handler(update: Update, context: CallbackContext) -> None:
    print(f"Update {update} caused error {context.error}")

def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MOVIE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie)],
            VERIFIED: [
                CallbackQueryHandler(button, pattern=r'verify✅'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_after_verify),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("help", help_command),
            CommandHandler("feedback", feedback_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_message)
        ],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
