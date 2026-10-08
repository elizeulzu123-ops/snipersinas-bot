#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============================================================
# CONFIGURAÇÃO
# ============================================================
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("❌ Verifique o TOKEN no .env!")

# ============================================================
# LOG
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# ============================================================
# IMAGEM DE BOAS‑VINDAS
# ============================================================
IMAGEM_URL = "https://i.ibb.co/JRvr5XjN/file-00000000e2f4820e905136c406931929.png"

# ============================================================
# CATÁLOGO (CHAVE INTERNA CORRIGIDA PARA EVITAR CONFUSÃO)
# ============================================================
CATALOGO = {
    "parafusadeira": {
        "icone": "🔩",
        "nome": "PARAFUSADEIRA",
        "marcas": {
            "BOSCH":        "https://meli.la/1GtWTR",
            "MAKITA":       "https://meli.la/1MjEzBC",
            "DEWALT":       "https://meli.la/1Lj62wM",
            "BLACK+DECKER": "https://meli.la/2cg9Ew4",
            "STANLEY":      "https://meli.la/2YoHTgT",
            "MONDIAL":      "https://meli.la/2yH2xvM",
            "PHILCO":       "https://meli.la/29EsFhi",
            "VONDER":       "https://meli.la/1NwzU1H",
        }
    },
    "furadeira": {
        "icone": "⚡",
        "nome": "FURADEIRA",
        "marcas": {
            "BOSCH":        "https://meli.la/1rTGEXr",
            "MAKITA":       "https://meli.la/1C5PnoK",
            "DEWALT":       "https://meli.la/2VeMEBq",
            "BLACK+DECKER": "https://meli.la/24oNzgo",
            "VONDER":       "https://meli.la/1KAXyAj",
            "STANLEY":      "https://meli.la/1UgDjh9",
        }
    },
    "serramarmore": {  # ← sem underline no meio para não dar conflito
        "icone": "🔧",
        "nome": "SERRA MÁRMORE",
        "marcas": {
            "BOSCH":        "https://meli.la/16m4wJn",
            "DEWALT":       "https://meli.la/1peLUGn",
            "VONDER":       "https://meli.la/2Hdyim9",
            "STANLEY":      "https://meli.la/2tANx4w",
        }
    },
    "martelete": {
        "icone": "🔨",
        "nome": "MARTELETE",
        "marcas": {
            "BOSCH":        "https://meli.la/1qtahqS",
            "MAKITA":       "https://meli.la/2jUiZos",
            "DEWALT":       "https://meli.la/1ddicJ8",
            "VONDER":       "https://meli.la/2TAS8Tr",
        }
    },
    "esmerilhadeira": {
        "icone": "⚙️",
        "nome": "ESMERILHADEIRA",
        "marcas": {
            "MAKITA":       "https://meli.la/199YrBZ",
            "BOSCH":        "https://meli.la/1x2FruA",
            "DEWALT":       "https://meli.la/1LazRn9",
            "VONDER":       "https://meli.la/1cNSVjo",
        }
    }
}

# ============================================================
# TECLADO FIXO DO RODAPÉ (IGUAL AO ORIGINAL)
# ============================================================
def teclado_rodape() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ["🔴 INÍCIO", "🔵 FERRAMENTAS"],
            ["📋 SOBRE NÓS"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True,
        selective=False
    )

# ============================================================
# GERA TECLADO DE MARCAS
# ============================================================
def criar_teclado_marcas(chave_produto: str) -> InlineKeyboardMarkup:
    marcas = CATALOGO[chave_produto]["marcas"]
    lista_marcas = list(marcas.keys())
    linhas = []
    for i in range(0, len(lista_marcas), 2):
        linha = [InlineKeyboardButton(lista_marcas[i], callback_data=f"marca_{chave_produto}_{lista_marcas[i]}", style="primary")]
        if i+1 < len(lista_marcas):
            linha.append(InlineKeyboardButton(lista_marcas[i+1], callback_data=f"marca_{chave_produto}_{lista_marcas[i+1]}", style="primary"))
        linhas.append(linha)
    linhas.append([InlineKeyboardButton("⬅️ VOLTAR", callback_data="menu_ferramentas", style="danger")])
    return InlineKeyboardMarkup(linhas)

# ============================================================
# /START — MENSAGEM DE BOAS‑VINDAS
# ============================================================
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    nome = user.first_name or "amigo"

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGEM_URL,
        caption=(
            f"🐠 OLÁ, {nome.upper()}! "
            "SEJA MUITO BEM‑VINDO!\n\n"
            "🔧 EU SOU O MARLIN DAS OFERTAS!\n\n"
            "Seu parceiro de confiança nas melhores "
            "oportunidades do Mercado Livre! 💎\n\n"
            "Aqui você encontra as melhores marcas, "
            "os melhores preços e produtos de qualidade! 💰\n\n"
            "🛠️ FERRAMENTAS\n"
            "🔩 PARAFUSADEIRAS\n"
            "⭐ GRANDES MARCAS\n\n"
            "👇 Escolha uma opção abaixo e vamos lá!"
        ),
        reply_markup=teclado_rodape()
    )

# ============================================================
# BOTÕES DO RODAPÉ (ATUALIZADO PARA serramarmore)
# ============================================================
async def mensagem_rodape(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    texto = update.message.text.strip()

    if texto == "🔴 INÍCIO":
        await start(update, context)

    elif texto == "🔵 FERRAMENTAS":
        await update.message.reply_text(
            "🛠️ FERRAMENTAS\n\nEscolha o que você está procurando:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔩 PARAFUSADEIRAS", callback_data="lista_parafusadeira", style="primary")],
                [InlineKeyboardButton("⚡ FURADEIRAS", callback_data="lista_furadeira", style="primary")],
                [InlineKeyboardButton("🔧 SERRAS MÁRMORE", callback_data="lista_serramarmore", style="primary")],
                [InlineKeyboardButton("🔨 MARTELETES", callback_data="lista_martelete", style="primary")],
                [InlineKeyboardButton("⚙️ ESMERILHADEIRAS", callback_data="lista_esmerilhadeira", style="primary")],
                [InlineKeyboardButton("⬅️ VOLTAR AO INÍCIO", callback_data="menu_inicial", style="danger")]
            ])
        )

    elif texto == "📋 SOBRE NÓS":
        await update.message.reply_text(
            "🔥 QUEM SOMOS NÓS?\n\n"
            "Somos o MARLIN DAS OFERTAS — conectando você "
            "às melhores promoções do Mercado Livre! 🛒\n\n"
            "✅ Produtos de qualidade\n"
            "✅ Marcas confiáveis\n"
            "✅ Preços direto da fonte\n"
            "✅ Segurança em cada compra\n\n"
            "Escolha uma opção abaixo e comece a economizar! 💸",
            reply_markup=teclado_rodape()
        )

# ============================================================
# AÇÕES DOS BOTÕES INLINE (LEITURA CORRIGIDA)
# ============================================================
async def acao_botao(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    dados = query.data

    if dados == "menu_inicial":
        await start(update, context)

    elif dados == "menu_ferramentas":
        await query.edit_message_text(
            "🛠️ FERRAMENTAS\n\nEscolha o que você está procurando:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔩 PARAFUSADEIRAS", callback_data="lista_parafusadeira", style="primary")],
                [InlineKeyboardButton("⚡ FURADEIRAS", callback_data="lista_furadeira", style="primary")],
                [InlineKeyboardButton("🔧 SERRAS MÁRMORE", callback_data="lista_serramarmore", style="primary")],
                [InlineKeyboardButton("🔨 MARTELETES", callback_data="lista_martelete", style="primary")],
                [InlineKeyboardButton("⚙️ ESMERILHADEIRAS", callback_data="lista_esmerilhadeira", style="primary")],
                [InlineKeyboardButton("⬅️ VOLTAR AO INÍCIO", callback_data="menu_inicial", style="danger")]
            ])
        )

    elif dados.startswith("lista_"):
        chave_prod = dados.replace("lista_", "")
        info = CATALOGO[chave_prod]
        await query.edit_message_text(
            f"{info['icone']} {info['nome']} — ESCOLHA A MARCA!\n\nClique na marca para ver as ofertas disponíveis! 🎯",
            reply_markup=criar_teclado_marcas(chave_prod)
        )

    elif dados.startswith("marca_"):
        partes = dados.split("_", 2)
        chave_prod = partes[1]
        marca = partes[2]
        link = CATALOGO[chave_prod]["marcas"][marca]
        info = CATALOGO[chave_prod]
        await query.edit_message_text(
            f"✅ EXCELENTE ESCOLHA!\n\n🔹 PRODUTO: {info['nome']}\n🔹 MARCA: {marca}\n\n🛒 Acesse agora e confira os melhores preços:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🛒 VER {marca} NO MERCADO LIVRE", url=link, style="primary")],
                [InlineKeyboardButton("⬅️ VOLTAR ÀS MARCAS", callback_data=f"lista_{chave_prod}", style="danger")]
            ])
        )

# ============================================================
# INICIALIZAÇÃO
# ============================================================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comecar", start))
    app.add_handler(CallbackQueryHandler(acao_botao))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_rodape))

    logger.info("=" * 60)
    logger.info("🐠 MARLIN DAS OFERTAS — ERRO DA SERRA MÁRMORE CORRIGIDO!")
    logger.info("✅ Visual e cores mantidos")
    logger.info("=" * 60)

    app.run_polling(drop_pending_updates=True)

# ============================================================
# EXECUTAR
# ============================================================
if __name__ == "__main__":
    main()
