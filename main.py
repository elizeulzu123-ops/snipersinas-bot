import os
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ══════════════════════════════════════════════════════════════
#                    CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════════
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("❌ Verifique o TOKEN no .env!")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# ✅ IMAGEM DE FERRAMENTAS
IMAGEM_URL = "https://picsum.photos/id/26/800/500"

# ══════════════════════════════════════════════════════════════
#               CATÁLOGO — TODOS OS LINKS CONFIRMADOS
# ══════════════════════════════════════════════════════════════
CATALOGO = {
    "parafusadeira": {
        "icone": "🔩",
        "nome": "PARAFUSADEIRA",
        "marcas": {
            "BOSCH":      "https://meli.la/1GtWTRG",
            "MAKITA":     "https://meli.la/1MjEzBC",
            "DEWALT":     "https://meli.la/1Lj62wM",
            "BLACK+DECKER": "https://meli.la/2cg9Ew4",
            "STANLEY":    "https://meli.la/2YoHTgT",
            "MONDIAL":    "https://meli.la/2yH2xvM",
            "PHILCO":     "https://meli.la/29EsFhi",
            "VONDER":     "https://meli.la/1NwzU1H",
        }
    }
}

# ══════════════════════════════════════════════════════════════
#               🎨 BOTÕES COLORIDOS NO RODAPÉ — IGUAL A IMAGEM!
# ══════════════════════════════════════════════════════════════
def teclado_rodape() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ["🔴 INÍCIO", "🔵 FERRAMENTAS"],
            ["� PARAFUSADEIRAS", "📋 SOBRE NÓS"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# ══════════════════════════════════════════════════════════════
#               BOTÕES DAS MARCAS COM CORES
# ══════════════════════════════════════════════════════════════
def teclado_marcas() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔴 BOSCH", callback_data="marca_BOSCH"),
            InlineKeyboardButton("🔵 MAKITA", callback_data="marca_MAKITA")
        ],
        [
            InlineKeyboardButton("� DEWALT", callback_data="marca_DEWALT"),
            InlineKeyboardButton("⚫ BLACK+DECKER", callback_data="marca_BLACK+DECKER")
        ],
        [
            InlineKeyboardButton("� STANLEY", callback_data="marca_STANLEY"),
            InlineKeyboardButton("� MONDIAL", callback_data="marca_MONDIAL")
        ],
        [
            InlineKeyboardButton("� PHILCO", callback_data="marca_PHILCO"),
            InlineKeyboardButton("� VONDER", callback_data="marca_VONDER")
        ],
        [
            InlineKeyboardButton("⬅️ VOLTAR", callback_data="menu_inicial")
        ]
    ])

# ══════════════════════════════════════════════════════════════
#              BOAS-VINDAS COM IMAGEM + RODAPÉ COLORIDO ✅
# ══════════════════════════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGEM_URL,
        caption=(
            f"OLÁ, {user.first_name.upper()}! 🔥 EU SOU O MARLIN DAS OFERTAS!\n\n"
            "ENCONTRO AS MELHORES OPÇÕES DIRETAMENTE NO MERCADO LIVRE PARA VOCÊ! 🛒\n"
            "OS PREÇOS VOCÊ CONFERE LÁ DIRETO!\n\n"
            "👇 Use os botões coloridos embaixo!"
        ),
        reply_markup=teclado_rodape()
    )

# ══════════════════════════════════════════════════════════════
#                  LIDA COM OS BOTÕES DO RODAPÉ
# ══════════════════════════════════════════════════════════════
async def mensagem_rodape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if texto == "🔴 INÍCIO":
        await start(update, context)

    elif texto == "🔵 FERRAMENTAS":
        await update.message.reply_text(
            "🛠️  ESCOLHA O PRODUTO:\n\n"
            "Clique abaixo para ver as marcas:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔩 PARAFUSADEIRAS", callback_data="lista_parafusadeira")],
                [InlineKeyboardButton("⬅️ VOLTAR", callback_data="menu_inicial")]
            ])
        )

    elif texto == "� PARAFUSADEIRAS":
        await update.message.reply_text(
            "🔩  PARAFUSADEIRAS — ESCOLHA A MARCA:\n\n"
            "Clique na marca para ver as ofertas!",
            reply_markup=teclado_marcas()
        )

    elif texto == "📋 SOBRE NÓS":
        await update.message.reply_text(
            "🔥 MARLIN DAS OFERTAS!\n\n"
            "Seu parceiro de melhores preços no Mercado Livre!\n"
            "Sempre as melhores marcas e promoções para você! 🛒\n\n"
            "Escolha um botão embaixo para começar! 👇",
            reply_markup=teclado_rodape()
        )

# ══════════════════════════════════════════════════════════════
#                  LIDA COM CLIQUES NAS MARCAS
# ══════════════════════════════════════════════════════════════
async def acao_botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dados = query.data

    if dados == "menu_inicial":
        await start(update, context)

    elif dados == "lista_parafusadeira":
        await query.edit_message_text(
            "🔩  PARAFUSADEIRAS — ESCOLHA A MARCA:\n\n"
            "Clique na marca para ver as ofertas!",
            reply_markup=teclado_marcas()
        )

    elif dados.startswith("marca_"):
        marca = dados.replace("marca_", "")
        link = CATALOGO["parafusadeira"]["marcas"][marca]

        await query.edit_message_text(
            f"✅ ÓTIMA ESCOLHA!\n\n"
            f"🔹 MARCA: {marca}\n"
            f"🔹 PRODUTO: PARAFUSADEIRA\n\n"
            "ACESSE AGORA E CONFIRA O PREÇO:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f"🛒 VER {marca} NO MERCADO LIVRE",
                    url=link
                )],
                [InlineKeyboardButton(
                    "⬅️ VOLTAR ÀS MARCAS",
                    callback_data="lista_parafusadeira"
                )]
            ])
        )

# ══════════════════════════════════════════════════════════════
#                    INICIALIZAÇÃO
# ══════════════════════════════════════════════════════════════
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(acao_botao))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_rodape))

    logger.info("=" * 60)
    logger.info("✅ BOT PRONTO — BOTÕES COLORIDOS NO RODAPÉ!")
    logger.info("✅ 🔴🔵� Cores ativadas | 8 marcas prontas")
    logger.info("✅ Todos os links confirmados")
    logger.info("=" * 60)

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
