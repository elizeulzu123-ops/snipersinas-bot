import os
import logging
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (Railway / local)
load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# O seu ID/Código oficial de afiliado do Mercado Livre
AFFILIATE_TAG = "Fe20250121204050"

# Configuração básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa o cliente da Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# Mensagem de boas-vindas otimizada para quem vem das redes sociais
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"Olá, {user_name}! 🔥 Seja muito bem-vindo!\n\n"
        "Eu sou o seu assistente de compras inteligente. O meu objetivo é ajudar-lo a encontrar "
        "as **melhores promoções, descontos e os preços mais baixos** do mercado!\n\n"
        "Diga-me: o que é que procura hoje? (Ex: *smartphone A17, fones bluetooth, ferramentas*)..."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# Função que processa as mensagens, gera a resposta da IA e cria o botão com o link rastreado
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    # Mostra o indicador "a escrever..."
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # Instruções especializadas para a IA atuar como caçador de ofertas persuasivo
        system_instruction = (
            "Tu és um assistente de vendas altamente persuasivo, especialista em encontrar promoções, "
            "descontos e as melhores ofertas do mercado para os utilizadores. "
            "O teu objetivo é analisar o que o cliente procura, dar conselhos úteis sobre os melhores "
            "produtos e incentivá-los a verificar as ofertas. Sê dinâmico, usa emojis adequados "
            "e mantém um tom entusiasmado e prestativo."
        )

        # Chamada à API da Groq
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        ai_response = completion.choices[0].message.content

        # Codifica o texto do utilizador para formato de URL (ex: "celular a17" vira "celular+a17")
        query_encoded = urllib.parse.quote(user_text)
        
        # Monta o link de busca oficial do Mercado Livre já incorporando o seu ID de afiliado
        affiliate_link = f"https://lista.mercadolivre.com.br/{query_encoded}#D[A:{query_encoded},ontrend:true]&matt_tool={AFFILIATE_TAG}"

        # Criação do botão interativo para o Telegram
        keyboard = [
            [InlineKeyboardButton("🛒 Ver Oferta no Mercado Livre", url=affiliate_link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Envia a resposta da IA junto com o botão interativo contendo o seu link rastreado
        await update.message.reply_text(
            ai_response, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Erro ao comunicar com a Groq: {e}")
        await update.message.reply_text(
            "Opa! Ocorreu um pequeno erro ao procurar as melhores ofertas neste momento. Tente novamente daqui a pouco!"
        )

def main():
    if not TOKEN or not GROQ_API_KEY:
        logger.error("Erro: TOKEN ou GROQ_API_KEY não definidos nas variáveis de ambiente.")
        return

    # Constrói a aplicação do bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Adiciona os manipuladores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot de afiliados iniciado com sucesso...")
    application.run_polling()

if __name__ == "__main__":
    main()
