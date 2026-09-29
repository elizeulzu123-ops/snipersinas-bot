import os
import logging
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters,
)
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AFFILIATE_TAG = "Fe20250121204050"
SEU_USER_TELEGRAM = "SeuUsuarioTelegram"

# Configuração de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa cliente Groq
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Dicionário para guardar o histórico de cada cliente (Chave: user_id, Valor: lista de mensagens)
historicos = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Limpa o histórico ao reiniciar com /start
    if user_id in historicos:
        del historicos[user_id]

    welcome_text = (
        f"OLÁ, {user.first_name.upper()}! 🔥 SEJA MUITO BEM-VINDO AO MARLIN DAS OFERTAS!\n\n"
        "EU SOU O SEU ASSISTENTE VIRTUAL NO **MERCADO LIVRE**. "
        "ESTOU AQUI PARA CONVERSAR COM VOCÊ, TIRAR DÚVIDAS E AJUDAR A ENCONTRAR EXATAMENTE O PRODUTO QUE VOCÊ PRECISA!\n\n"
        "👉 *ME CONTE: O QUE VOCÊ ESTÁ A PROCURAR HOJE?*"
    )
    
    keyboard = [[InlineKeyboardButton("🔥 VER OFERTAS DO DIA", callback_data="ofertas imperdíveis mercado livre")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def processar_mensagem(update, context, chat_id, user, user_text):
    user_id = user.id
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Inicializa o histórico do utilizador se não existir
    if user_id not in historicos:
        system_prompt = (
            "Tu és o assistente de vendas e especialista em produtos do **MERCADO LIVRE**. "
            "O teu objetivo principal é conversar de forma natural e amigável com o cliente, fazendo perguntas inteligentes "
            "para descobrir exatamente o que ele procura (como faixa de preço, marca, finalidade ou tamanho) antes de sugerir links. "
            "REGRA OBRIGATÓRIA 1: Escreve INTEIRAMENTE EM LETRAS MAIÚSCULAS (CAPSLOCK). "
            "REGRA OBRIGATÓRIA 2: Sê dinâmico, usa emojis e faz sempre uma pergunta no final para continuar o diálogo."
        )
        historicos[user_id] = [{"role": "system", "content": system_prompt}]

    # Adiciona a mensagem do cliente ao histórico dele
    historicos[user_id].append({"role": "user", "content": user_text})

    resposta_ia = ""
    try:
        if groq_client:
            # Pede à IA para gerar a resposta com base em toda a conversa anterior
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=historicos[user_id],
                temperature=0.7,
                max_tokens=1024,
            )
            resposta_ia = completion.choices[0].message.content
            
            # Guarda a resposta da IA no histórico para manter o contexto
            historicos[user_id].append({"role": "assistant", "content": resposta_ia})
    except Exception as e:
        logger.error(f"Erro na API da Groq: {e}")

    if not resposta_ia:
        resposta_ia = f"QUE EXCELENTE ESCOLHA! VOU TE AJUDAR A ENCONTRAR AS MELHORES OPÇÕES PARA '{user_text.upper()}' NO MERCADO LIVRE!"

    # Cria o link de afiliado direcionando para a busca ou ofertas gerais
    texto_limpo = user_text.strip().lower()
    if texto_limpo in ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "ofertas"]:
        affiliate_link = f"https://www.mercadolivre.com.br/ofertas?matt_tool={AFFILIATE_TAG}"
    else:
        query_encoded = urllib.parse.quote(user_text)
        affiliate_link = f"https://lista.mercadolivre.com.br/{query_encoded}#D[A:{query_encoded},ontrend:true]&matt_tool={AFFILIATE_TAG}"

    support_link = f"https://t.me/{SEU_USER_TELEGRAM}"

    keyboard = [
        [InlineKeyboardButton("🛒 VER OFERTA NO MERCADO LIVRE", url=affiliate_link)],
        [InlineKeyboardButton("💬 FALAR COM O SUPORTE", url=support_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=resposta_ia,
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await processar_mensagem(update, context, update.effective_chat.id, update.effective_user, update.message.text)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await processar_mensagem(update, context, query.message.chat_id, query.from_user, query.data)

def main():
    if not TOKEN:
        logger.error("Token do Telegram não configurado!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    logger.info("Bot rodando e conectado à IA...")
    app.run_polling()

if __name__ == "__main__":
    main()
