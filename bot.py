from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8620336521:AAG_u9AYArtryE9fGjJ1R8gny8NtoO4tUgo"

async def start(update, context):
    await update.message.reply_text("🤖 Bot Online!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("BOT ONLINE")

app.run_polling()
