from keep_alive import keep_alive  # Correct import to keep the bot alive via Flask
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext, ConversationHandler

# Start the keep_alive server
keep_alive()  # Start the Flask server to keep the bot alive

# Set up logging to capture errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
MOVIE_INPUT, VERIFIED = range(2)

# Function to start the bot and send the first message
async def start(update: Update, context: CallbackContext) -> int:
    try:
        user_first_name = update.message.from_user.first_name  # Get the user's first name
        image_url = "https://static.vecteezy.com/system/resources/previews/000/240/724/original/popcorn-machine-vector.jpg"  # URL of the popcorn machine image

        # Send the specified text first
        await update.message.reply_text(
            "❗️Just Send Movie Name And Year Correctly.\n\n"
            "➠ Other BOTs : @iPapkornFbot"
        )

        # Construct the caption for the image with a clickable "Google"
        caption = (
            f"Hey 👋 {user_first_name} 🤩\n\n"
            "🍿 Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Wᴏʀʟᴅ's Cᴏᴏʟᴇsᴛ Sᴇᴀʀᴄʜ Eɴɢɪɴᴇ!\n\n"
            "Here You Can Request Movie's, Just Send Movie OR WebSeries Name With Proper [Google](https://www.google.com/) Spelling..!!"
        )

        # Send photo with caption
        await update.message.reply_photo(
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'  # Enable Markdown for clickable link
        )
        return MOVIE_INPUT
    except Exception as e:
        logger.error(f"Error in start function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return ConversationHandler.END

# Function to handle the user's movie name and year input (2nd message)
async def handle_movie(update: Update, context: CallbackContext) -> int:
    try:
        # Create inline keyboard buttons for "Join" and "Verify"
        keyboard = [
            [
                InlineKeyboardButton("Join💥", url="https://t.me/major/start?startapp=1607381212"),
                InlineKeyboardButton("Verify✅", callback_data='verify✅'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Plz First Join The Group And Verify it To Continue 🕵️", reply_markup=reply_markup)
        return VERIFIED
    except Exception as e:
        logger.error(f"Error in handle_movie function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return ConversationHandler.END

# Function to handle button clicks (3rd message)
async def button(update: Update, context: CallbackContext) -> int:
    try:
        query = update.callback_query
        await query.answer()

        if query.data == 'verify✅':
            # Once "Verify✅" is clicked, the bot sends the 3rd message and removes the buttons
            await query.edit_message_text(text="😍Great Now You Are All Set, Just Send The Movie Name And Year Correctly 🤗")
        return VERIFIED
    except Exception as e:
        logger.error(f"Error in button function: {e}")
        await update.callback_query.answer("An error occurred. Please try again later.")
        return VERIFIED

# Function to handle user's input after clicking "Verify✅" (4th and 5th messages)
async def handle_after_verify(update: Update, context: CallbackContext) -> int:
    try:
        await update.message.reply_text("❗Due To Heavy Load We Have Now Upgraded Our Bot to Response More Efficiently 😊")
        await update.message.reply_text("Just Send Your Movie Name In Our New Upgraded Bot 💪 @iPapkornFbot")
        return VERIFIED
    except Exception as e:
        logger.error(f"Error in handle_after_verify function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return VERIFIED

# Function to send bot 5th message in reply to every next message after bot 4th and 5th
async def repeat_message(update: Update, context: CallbackContext) -> int:
    try:
        await update.message.reply_text("Just Send Your Movie Name In Our New Upgraded Bot 💪 @iPapkornFbot")
        return VERIFIED
    except Exception as e:
        logger.error(f"Error in repeat_message function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return VERIFIED

# Function to handle /help command
async def help_command(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text(
            "We're excited to inform you that we've upgraded our bot to better serve your needs. "
            "To ensure a smoother and more efficient experience, we invite you to join us at our new bot, @iPapkornFbot.\n\n"
            "Thank you for your continued support🫶\n\n"
            "Best regards,\n"
            "iPapKornBot"
        )
    except Exception as e:
        logger.error(f"Error in help_command function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# Function to handle /feedback command
async def feedback_command(update: Update, context: CallbackContext) -> None:
    try:
        await update.message.reply_text(
            "Please Let Us Know How Was Your Experience By Sending Your Feedback In Our Main Channel @iPapkornFbot 🤧"
        )
    except Exception as e:
        logger.error(f"Error in feedback_command function: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

def main() -> None:
    try:
        # Replace with your actual bot token
        application = Application.builder().token("7602665717:AAGf3kgqzkaNkyQsexOkkBgmFSPG2IvxpRk").build()

        # Define the conversation handler with states
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                MOVIE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie)],
                VERIFIED: [
                    CallbackQueryHandler(button, pattern='verify✅'),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_after_verify),
                ],
            },
            fallbacks=[
                CommandHandler("start", start),  # Restart conversation when /start is received
                CommandHandler("help", help_command),
                CommandHandler("feedback", feedback_command),
                MessageHandler(filters.TEXT & ~filters.COMMAND, repeat_message)
            ],
        )

        # Add the conversation handler to the application
        application.add_handler(conv_handler)

        # Start the bot
        application.run_polling()

    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == '__main__':
    main()
