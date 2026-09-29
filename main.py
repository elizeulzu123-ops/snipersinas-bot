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

# Substitua pelo seu nome de utilizador (username) do Telegram no suporte
SEU_USER_TELEGRAM = "SeuUsuarioTelegram"

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

    if user_id not in utilizadores_unicos:
        utilizadores_unicos.add(user_id)
        
        if MEU_ADMIN_ID:
            try:
                aviso_admin = f"🚨 *NOVO CLIENTE NO BOT!*\n\n👤 Nome: {user_name}\n🆔 ID: `{user_id}`\n👥 Total de clientes: {len(utilizadores_unicos)}"
                await context.bot.send_message(chat_id=int(MEU_ADMIN_ID), text=aviso_admin, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Erro ao enviar aviso para o admin: {e}")

    welcome_message = (
        f"OLÁ, {user_name.upper()}! 🔥 SEJA MUITO BEM-VINDO AO SEU ASSISTENTE DE COMPRAS!\n\n"
        "EU SOU ESPECIALISTA EM ENCONTRAR AS MELHORES OFERTAS, DESCONTOS E PRODUTOS NO **MERCADO LIVRE**!\n\n"
        "👉 *FALE COMIGO SOBRE QUALQUER PRODUTO (EX: QUAL O MELHOR CELULAR, FERRAMENTAS EM PROMOÇÃO) OU ESCOLHA UMA CATEGORIA ABAIXO:*"
    )

    keyboard = [
        [
            InlineKeyboardButton("📱 CELULARES & ACESSÓRIOS", callback_data="celular"),
            InlineKeyboardButton("🛠️ FERRAMENTAS", callback_data="ferramentas")
        ],
        [
            InlineKeyboardButton("🏠 CASA E COZINHA", callback_data="utilidades para casa"),
            InlineKeyboardButton("💻 INFORMÁTICA", callback_data="notebook e eletronicos")
        ],
        [
            InlineKeyboardButton("🔥 VER OFERTAS DO DIA", callback_data="ofertas imperdíveis no mercado livre")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_pessoas = len(utilizadores_unicos)
    await update.message.reply_text(
        f"📊 *ESTATÍSTICAS DO BOT:*\n\n"
        f"👥 Total de pessoas únicas que já acederam: **{total_pessoas}**",
        parse_mode="Markdown"
    )

async def processar_busca(update_obj, context, chat_id, user, user_text):
    if user.id not in utilizadores_unicos:
        utilizadores_unicos.add(user.id)

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    ai_response = ""

    try:
        if groq_client:
            # Instrução inteligente com tratamento de saudações e foco em produtos do Mercado Livre
            system_instruction = (
                "Tu és o assistente de inteligência artificial oficial de vendas do **MERCADO LIVRE**. "
                "O teu foco absoluto é conversar sobre produtos disponíveis no Mercado Livre, dar dicas de compras, "
                "comparar itens e ajudar o cliente a escolher o melhor produto. "
                "REGRA OBRIGATÓRIA 1: Escreve INTEIRAMENTE EM LETRAS MAIÚSCULAS (CAPSLOCK) para dar máximo destaque. "
                "REGRA OBRIGATÓRIA 2: Se o utilizador disser apenas 'olá', 'oi', 'bom dia' ou cumprimentos semelhantes, NÃO digas que encontraste o produto. Em vez disso, cumprimenta-o com muita energia, diz que estás pronto para ajudar a achar os melhores produtos no Mercado Livre e pergunta qual produto ou categoria ele quer procurar hoje! "
                "REGRA OBRIGATÓRIA 3: Sê dinâmico, usa emojis comerciais e incentiva sempre o cliente."
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

    # Verifica se a mensagem foi uma saudação simples para direcionar o link corretamente
    texto_limpo = user_text.strip().lower()
    saudacoes = ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "tudo bem", "eae"]

    if not ai_response:
        ai_response = f"ENCONTREI ÓTIMAS OPÇÕES E PROMOÇÕES IMPERDÍVEIS PARA '{user_text.upper()}' NO MERCADO LIVRE!"

    # Se for saudação, o link aponta para a página geral de ofertas; se for produto, faz a busca exata
    if texto_limpo in saudacoes:
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
        text=ai_response,
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    user = update.effective_user
    await processar_busca(update, context, chat_id, user, user_text)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    
    user_text = query.data  
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

    logger.info("Bot completo com IA conversacional ativado...")
    application.run_polling()

if __name__ == "__main__":
    main()
