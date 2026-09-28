import os
import logging
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# O seu ID de afiliado oficial do Mercado Livre
AFFILIATE_TAG = "Fe20250121204050"

# Configuração básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa o cliente da Groq apenas se a chave existir
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"Olá, {user_name}! 🔥 Seja muito bem-vindo!\n\n"
        "Eu sou o seu assistente de compras inteligente. O meu objetivo é ajudar-lo a encontrar "
        "as melhores promoções, descontos e os preços mais baixos do mercado!\n\n"
        "Diga-me: o que é que procura hoje? (Ex: smartphone Motorola, fones bluetooth, ferramentas)..."
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    # Mostra o indicador "a escrever..."
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    ai_response = ""

    # Tenta gerar a resposta com a IA da Groq
    try:
        if groq_client:
            system_instruction = (
                "Tu és um assistente de vendas altamente persuasivo, especialista em encontrar promoções, "
                "descontos e as melhores ofertas do mercado para os utilizadores. "
                "O teu objetivo é analisar o que o cliente procura, dar conselhos úteis sobre os melhores "
                "produtos e incentivá-los a verificar as ofertas. Sê dinâmico, usa emojis adequados "
                "e mantém um tom entusiasmado e prestativo."
            )

            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            ai_response = completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Aviso: Erro na API da Groq: {e}")

    # Se a IA falhar ou estiver sem chave, usa uma resposta comercial padrão
    if not ai_response:
        ai_response = f"Encontrei excelentes opções e ofertas imperdíveis para '{user_text}' com os melhores preços!"

    # Criação do link de busca oficial com o seu ID de afiliado
    query_encoded = urllib.parse.quote(user_text)
    affiliate_link = f"https://lista.mercadolivre.com.br/{query_encoded}#D[A:{query_encoded},ontrend:true]&matt_tool={AFFILIATE_TAG}"

    # Adiciona o link em texto para validação visual neste teste
    mensagem_final = f"{ai_response}\n\n🔗 *Link gerado:* `{affiliate_link}`"

    # Botão interativo do Telegram com o link rastreado
    keyboard = [
        [InlineKeyboardButton("🛒 Ver Oferta no Mercado Livre", url=affiliate_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envia a mensagem com o botão
    await update.message.reply_text(
        mensagem_final, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    if not TOKEN:
        logger.error("Erro: TOKEN do Telegram não definido.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot de teste de pesquisa iniciado com sucesso...")
    application.run_polling()

if __name__ == "__main__":
    main()
