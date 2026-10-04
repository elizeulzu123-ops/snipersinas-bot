#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

IMAGEM_URL = "https://picsum.photos/id/175/800/500"

# ══════════════════════════════════════════════════════════════
#               CATÁLOGO
# ══════════════════════════════════════════════════════════════
CATALOGO = {
    "parafusadeira": {
        "icone": "🔩",
        "nome": "PARAFUSADEIRA",
        "marcas": {
            "BOSCH":        "https://meli.la/1GtWTRG",
            "MAKITA":       "https://meli.la/1MjEzBC",
            "DEWALT":       "https://meli.la/1Lj62wM",
            "BLACK+DECKER": "https://meli.la/2cg9Ew4",
            "STANLEY":      "https://meli.la/2YoHTgT",
            "MONDIAL":      "https://meli.la/2yH2xvM",
            "PHILCO":       "https://meli.la/29EsFhi",
            "VONDER":       "https://meli.la/1NwzU1H",
        }
    }
}

# ══════════════════════════════════════════════════════════════
#               ✅ RODAPÉ AJUSTADO — SEM REPETIÇÃO
# ══════════════════════════════════════════════════════════════
def teclado_rodape() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ["🔴 INÍCIO", "🔵 FERRAMENTAS"],
            ["📋 SOBRE NÓS"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# ══════════════════════════════════════════════════════════════
#               BOTÕES DAS MARCAS
# ══════════════════════════════════════════════════════════════
def teclado_marcas() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔴 BOSCH", callback_data="marca_BOSCH"),
            InlineKeyboardButton("🔵 MAKITA", callback_data="marca_MAKITA")
        ],
        [
            InlineKeyboardButton("🟡 DEWALT", callback_data="marca_DEWALT"),
            InlineKeyboardButton("⚫ BLACK+DECKER", callback_data="marca_BLACK+DECKER")
        ],
        [
            InlineKeyboardButton("🟤 STANLEY", callback_data="marca_STANLEY"),
            InlineKeyboardButton("🟢 MONDIAL", callback_data="marca_MONDIAL")
        ],
        [
            InlineKeyboardButton("🔷 PHILCO", callback_data="marca_PHILCO"),
            InlineKeyboardButton("🟠 VONDER", callback_data="marca_VONDER")
        ],
        [
            InlineKeyboardButton("⬅️ VOLTAR", callback_data="menu_inicial")
        ]
    ])

# ══════════════════════════════════════════════════════════════
#              BOAS-VINDAS
# ══════════════════════════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome = user.first_name or "amigo"

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGEM_URL,
        caption=(
            f"🐠 OLÁ, {nome.upper()}! SEJA MUITO BEM-VINDO!\n\n"
            "Eu sou o MARLIN DAS OFERTAS!\n"
            "Seu parceiro de confiança nas melhores oportunidades do Mercado Livre! 💎\n\n"
            "Aqui você encontra as melhores marcas, os melhores preços e sempre com segurança! 💰\n\n"
            "👇 Escolha uma opção abaixo e vamos lá!"
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
            "🛠️ FERRAMENTAS\n\n"
            "Escolha o que você está procurando:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔩 PARAFUSADEIRAS", callback_data="lista_parafusadeira")],
                [InlineKeyboardButton("⬅️ VOLTAR AO INÍCIO", callback_data="menu_inicial")]
            ])
        )

    elif texto == "📋 SOBRE NÓS":
        await update.message.reply_text(
            "🔥 QUEM SOMOS NÓS?\n\n"
            "Somos o MARLIN DAS OFERTAS — conectando você às melhores promoções do Mercado Livre! 🛒\n\n"
            "✅ Produtos de qualidade\n"
            "✅ Marcas confiáveis\n"
            "✅ Preços direto da fonte\n"
            "✅ Segurança em cada compra\n\n"
            "Escolha uma opção abaixo e comece a economizar! 💸",
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
            "🔩 PARAFUSADEIRAS — ESCOLHA A MARCA!\n\n"
            "Clique na marca para ver as ofertas disponíveis! 🎯",
            reply_markup=teclado_marcas()
        )

    elif dados.startswith("marca_"):
        marca = dados.replace("marca_", "")
        link = CATALOGO["parafusadeira"]["marcas"][marca]

        await query.edit_message_text(
            f"✅ EXCELENTE ESCOLHA!\n\n"
            f"🔹 PRODUTO: PARAFUSADEIRA\n"
            f"🔹 MARCA: {marca}\n\n"
            "Acesse agora e confira os melhores preços:",
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
    logger.info("🐠 MARLIN DAS OFERTAS — RODAPÉ AJUSTADO!")
    logger.info("✅ Rodapé limpo: Início | Ferramentas | Sobre Nós")
    logger.info("✅ Parafusadeira dentro de Ferramentas")
    logger.info("=" * 60)

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
