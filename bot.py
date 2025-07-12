# file: promo_bot_ycf.py
import os
import json
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---- ENVIRONMENT VARIABLES (set them in Yandex Cloud console) ----
BOT_TOKEN    = os.environ["BOT_TOKEN"]            # e.g. 8016…VA   (never hard‑code!)
CHANNEL_ID   = os.environ["CHANNEL_ID"]           # '@fitolooks'  OR  '-1001234567890'
PROMO_CODE   = os.environ.get("PROMO_CODE", "Telegram_2025")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/fitolooks")
# ------------------------------------------------------------------

# Yandex Cloud Functions entry‑point
def handler(event, context):
    """
    Called once per Telegram webhook delivery.
    event["body"] is a JSON string representing the update.
    """
    # Because python-telegram-bot is asyncio‑based we need one event loop run:
    asyncio.run(process_update(event["body"]))
    return {
        "statusCode": 200,
        "body": "ok",
        "headers": {"Content-Type": "text/plain"},
    }

async def process_update(body: str):
    update = Update.de_json(json.loads(body), None)

    # Build an Application object (lightweight, stateless)
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )
    app.add_handler(CommandHandler("start", start))

    # Feed the single update to the dispatcher
    await app.initialize()
    await app.process_update(update)
    await app.shutdown()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # 1. Verify subscription
    member = await ctx.bot.get_chat_member(CHANNEL_ID, user.id)
    if member.status in ("member", "administrator", "creator"):
        await update.message.reply_text(
            f"🎉 Ваш промокод: **{PROMO_CODE}**\n"
            "Используйте его на сайте fitolooks.com, чтобы получить бесплатный шампунь при любом заказе!",
            parse_mode="Markdown"
        )
    else:
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton("👉 Подписаться", url=CHANNEL_LINK)]]
        )
        await update.message.reply_text(
            "Сначала подпишитесь на канал и снова нажмите /start.",
            reply_markup=kb,
        )
