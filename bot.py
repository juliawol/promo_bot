import os, json, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown
from telegram.error import Forbidden, BadRequest

BOT_TOKEN   = os.environ["BOT_TOKEN"]
_channel    = os.environ.get("CHANNEL_ID", "@fitolooks")
CHANNEL_ID  = int(_channel) if _channel.startswith("-100") else _channel
PROMO_CODE  = os.environ.get("PROMO_CODE", "Telegram_2025")
CHANNEL_URL = "https://t.me/fitolooks"

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Здравствуйте! Я проверю вашу подписку на канал {CHANNEL_URL} "
        "и вышлю промо‑код!"
    )

    try:
        member = await ctx.bot.get_chat_member(CHANNEL_ID, update.effective_user.id)
        subscribed = member.status in ("member", "administrator", "creator")
    except (Forbidden, BadRequest):
        subscribed = False

    if subscribed:
        code_md = escape_markdown(PROMO_CODE, version=2)
        await update.message.reply_text(
            f"🎉 Ваш промокод: *{code_md}*",
            parse_mode="MarkdownV2"
        )
    else:
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton("👉 Подписаться", url=CHANNEL_URL)]]
        )
        await update.message.reply_text(
            "Похоже, вы ещё не подписаны на канал.\n"
            "Нажмите кнопку, подпишитесь и снова отправьте /start.",
            reply_markup=kb,
        )

async def _process(body: str):
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    update = Update.de_json(json.loads(body), app.bot)

    app.add_handler(CommandHandler("start", cmd_start))

    await app.initialize()
    await app.process_update(update)
    await app.shutdown()

def handler(event, context):
    body = event.get("body") if event else None
    if not body:
        return {"statusCode": 400, "body": "Empty request body"}
    try:
        asyncio.run(_process(body))
    except Exception as exc:
        print("ERROR while processing update:", exc)
        return {"statusCode": 400, "body": f"Bad update: {exc}"}
    return {"statusCode": 200, "body": ""}
