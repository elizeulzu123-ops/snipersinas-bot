import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (se usar localmente)
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Configuração básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O bot de teste está a funcionar perfeitamente no Railway! 🚀")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # O bot apenas repete o que você escreveu para provar que está a receber e a responder
    await update.message.reply_text(f"Você disse: {user_text}\n\nO bot recebeu a sua mensagem com sucesso! ✅")

def main():
    if not TOKEN:
        logger.error("Erro: TOKEN do Telegram não definido.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    logger.info("Bot de teste iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()
