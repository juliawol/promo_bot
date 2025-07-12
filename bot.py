import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN     = os.environ["8016960037:AAF1phfRDXw-_s9WwziYXJLqUYRPD8hEsVA"]
CHANNEL_LINK  = os.environ.get("https://t.me/fitolooks")
CHANNEL_ID    = CHANNEL_LINK
PROMO_CODE    = os.environ.get("Telegram_2025")

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    member = await ctx.bot.get_chat_member(CHANNEL_ID, user.id)
    if member.status in ("member", "administrator", "creator"):
        await update.message.reply_text(
            f"🎉 Ваш промокод: **{PROMO_CODE}**\n"
            "Используйте его на сайте fitolooks.com, чтобы получить бесплатный шампунь при любом заказе!",
            parse_mode="Markdown"
        )
    else:
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton("👉 Подписаться", url=CHANNEL_LINK)]]
        )
        await update.message.reply_text(
            "Сначала подпишитесь на канал и снова нажмите /start.",
            reply_markup=kb,
        )

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
