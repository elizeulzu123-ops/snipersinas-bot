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
# IMAGEM DE BOAS-VINDAS
# ============================================================

IMAGEM_URL = "https://i.ibb.co/JRvr5XjN/file-00000000e2f4820e905136c406931929.png"


# ============================================================
# CATÁLOGO
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
    }
}


# ============================================================
# TECLADO FIXO DO RODAPÉ
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
# MENU DE MARCAS
# ============================================================

def teclado_marcas() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "BOSCH",
                callback_data="marca_BOSCH",
                style="primary"
            ),

            InlineKeyboardButton(
                "MAKITA",
                callback_data="marca_MAKITA",
                style="primary"
            )
        ],

        [
            InlineKeyboardButton(
                "DEWALT",
                callback_data="marca_DEWALT",
                style="primary"
            ),

            InlineKeyboardButton(
                "BLACK+DECKER",
                callback_data="marca_BLACK+DECKER",
                style="primary"
            )
        ],

        [
            InlineKeyboardButton(
                "STANLEY",
                callback_data="marca_STANLEY",
                style="primary"
            ),

            InlineKeyboardButton(
                "MONDIAL",
                callback_data="marca_MONDIAL",
                style="primary"
            )
        ],

        [
            InlineKeyboardButton(
                "PHILCO",
                callback_data="marca_PHILCO",
                style="primary"
            ),

            InlineKeyboardButton(
                "VONDER",
                callback_data="marca_VONDER",
                style="primary"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ VOLTAR",
                callback_data="menu_inicial",
                style="danger"
            )
        ]
    ])


# ============================================================
# /START — MENSAGEM DE BOAS-VINDAS
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
            "SEJA MUITO BEM-VINDO!\n\n"

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
# BOTÕES DO RODAPÉ
# ============================================================

async def mensagem_rodape(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    texto = update.message.text.strip()


    # --------------------------------------------------------
    # INÍCIO
    # --------------------------------------------------------

    if texto == "🔴 INÍCIO":

        await start(update, context)


    # --------------------------------------------------------
    # FERRAMENTAS
    # --------------------------------------------------------

    elif texto == "🔵 FERRAMENTAS":

        await update.message.reply_text(

            "🛠️ FERRAMENTAS\n\n"
            "Escolha o que você está procurando:",

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        "🔩 PARAFUSADEIRAS",
                        callback_data="lista_parafusadeira",
                        style="primary"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "⬅️ VOLTAR AO INÍCIO",
                        callback_data="menu_inicial",
                        style="danger"
                    )
                ]

            ])
        )


    # --------------------------------------------------------
    # SOBRE NÓS
    # --------------------------------------------------------

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
# AÇÕES DOS BOTÕES INLINE
# ============================================================

async def acao_botao(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    dados = query.data


    # --------------------------------------------------------
    # VOLTAR AO MENU INICIAL
    # --------------------------------------------------------

    if dados == "menu_inicial":

        await start(update, context)


    # --------------------------------------------------------
    # LISTA DE PARAFUSADEIRAS
    # --------------------------------------------------------

    elif dados == "lista_parafusadeira":

        await query.edit_message_text(

            "🔩 PARAFUSADEIRAS — ESCOLHA A MARCA!\n\n"

            "Clique na marca para ver as ofertas disponíveis! 🎯",

            reply_markup=teclado_marcas()
        )


    # --------------------------------------------------------
    # MARCA SELECIONADA
    # --------------------------------------------------------

    elif dados.startswith("marca_"):

        marca = dados.replace("marca_", "")

        link = CATALOGO["parafusadeira"]["marcas"][marca]


        await query.edit_message_text(

            f"✅ EXCELENTE ESCOLHA!\n\n"

            f"🔹 PRODUTO: PARAFUSADEIRA\n"
            f"🔹 MARCA: {marca}\n\n"

            "🛒 Acesse agora e confira os melhores preços:",

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        f"🛒 VER {marca} NO MERCADO LIVRE",
                        url=link,
                        style="primary"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "⬅️ VOLTAR ÀS MARCAS",
                        callback_data="lista_parafusadeira",
                        style="danger"
                    )
                ]

            ])
        )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

def main():

    app = Application.builder().token(TOKEN).build()


    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # Botões inline
    app.add_handler(
        CallbackQueryHandler(
            acao_botao
        )
    )


    # Botões do rodapé
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensagem_rodape
        )
    )


    logger.info("=" * 60)

    logger.info(
        "🐠 MARLIN DAS OFERTAS — BOTÕES AZUIS!"
    )

    logger.info(
        "✅ Nova imagem de ferramentas configurada"
    )

    logger.info(
        "✅ Imagem aparece na mensagem de boas-vindas"
    )

    logger.info(
        "✅ Rodapé persistente"
    )

    logger.info(
        "✅ Todas as marcas em azul"
    )

    logger.info(
        "✅ Botões VOLTAR em vermelho"
    )

    logger.info(
        "✅ Parafusadeiras dentro de Ferramentas"
    )

    logger.info("=" * 60)


    # Inicia o bot
    app.run_polling(
        drop_pending_updates=True
    )


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()
