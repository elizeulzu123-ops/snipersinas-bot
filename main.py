import os
import logging
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, CommandHandler, filters
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# O seu ID de afiliado oficial do Mercado Livre
AFFILIATE_TAG = "Fe20250121204050"

# O seu ID pessoal de Administrador no Telegram para receber os avisos
MEU_ADMIN_ID = "7780082282" 

# Conjunto para guardar os IDs únicos dos utilizadores
utilizadores_unicos = set()

# Configuração básica de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa o cliente da Groq
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    user_name = user.first_name

    # Se for um novo utilizador, guarda e envia um aviso privado para si
    if user_id not in utilizadores_unicos:
        utilizadores_unicos.add(user_id)
        
        if MEU_ADMIN_ID:
            try:
                aviso_admin = f"🚨 *Novo cliente no bot!*\n\n👤 Nome: {user_name}\n🆔 ID: `{user_id}`\n👥 Total de clientes: {len(utilizadores_unicos)}"
                await context.bot.send_message(chat_id=int(MEU_ADMIN_ID), text=aviso_admin, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Erro ao enviar aviso para o admin: {e}")

    welcome_message = (
        f"Olá, {user_name}! 🔥 Seja muito bem-vindo!\n\n"
        "Eu sou o seu assistente de compras inteligente. O meu objetivo é ajudar-lo a encontrar "
        "as melhores promoções, descontos e os preços mais baixos do mercado!\n\n"
        "Pode escolher uma das categorias rápidas abaixo ou simplesmente **digitar o que procura** (Ex: furadeira, smart TV, tênis)..."
    )

    # Botões interativos de categorias rápidas
    keyboard = [
        [
            InlineKeyboardButton("📱 Celulares & Acessórios", callback_data="celular"),
            InlineKeyboardButton("🛠️ Ferramentas", callback_data="ferramentas")
        ],
        [
            InlineKeyboardButton("🏠 Casa e Cozinha", callback_data="utilidades para casa"),
            InlineKeyboardButton("💻 Informática", callback_data="notebook e eletronicos")
        ],
        [
            InlineKeyboardButton("🔥 Ver Ofertas do Dia", callback_data="ofertas imperdíveis no mercado livre")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Comando para ver as estatísticas
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_pessoas = len(utilizadores_unicos)
    await update.message.reply_text(
        f"📊 *Estatísticas do Bot:*\n\n"
        f"👥 Total de pessoas únicas que já acederam: **{total_pessoas}**"
    )

# Função central que processa o texto (seja por mensagem digitada ou clique em botões)
async def processar_busca(update_obj, context, chat_id, user, user_text):
    if user.id not in utilizadores_unicos:
        utilizadores_unicos.add(user.id)

    # Mostra o indicador "a escrever..."
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    ai_response = ""

    try:
        if groq_client:
            system_instruction = (
                "Tu és um assistente de vendas altamente persuasivo, especialista em encontrar promoções, "
                "descontos e as melhores ofertas do Mercado Livre para os utilizadores. "
                "O teu objetivo é analisar o que o cliente procura, dar conselhos úteis e entusiasmados "
                "sobre os produtos e incentivá-los a verificar as ofertas. Sê dinâmico, usa emojis adequados "
                "e escreve respostas curtas, cativantes e amigáveis."
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

    if not ai_response:
        ai_response = f"Encontrei ótimas opções e promoções imperdíveis para '{user_text}' com os melhores preços do mercado!"

    # Gera o link dinâmico com o código de afiliado
    query_encoded = urllib.parse.quote(user_text)
    affiliate_link = f"https://lista.mercadolivre.com.br/{query_encoded}#D[A:{query_encoded},ontrend:true]&matt_tool={AFFILIATE_TAG}"

    keyboard = [
        [InlineKeyboardButton("🛒 Ver Oferta no Mercado Livre", url=affiliate_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=ai_response,
        reply_markup=reply_markup
    )

# Handler para mensagens de texto comuns
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    user = update.effective_user
    await processar_busca(update, context, chat_id, user, user_text)

# Handler para quando o utilizador clica num botão de categoria
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Fecha o loading do botão no Telegram
    
    user_text = query.data  # O valor guardado no callback_data vira a busca
    chat_id = query.message.chat_id
    user = query.from_user

    await processar_busca(update, context, chat_id, user, user_text)

def main():
    if not TOKEN:
        logger.error("Erro: TOKEN do Telegram não definido.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot com botões de categorias e IA ativo...")
    application.run_polling()

if __name__ == "__main__":
    main()
