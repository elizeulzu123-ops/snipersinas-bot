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
# REGISTRO
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
# CATÁLOGO DE FERRAMENTAS E MARCAS
# ============================================================

CATALOGO = {
    "parafusadeira": {
        "icone": "🔋",
        "nome": "PARAFUSADEIRA",
        "marcas": {
            "BOSCH": "https://meli.la/1GtWTR",
            "MAKITA": "https://meli.la/1MjEzBC",
            "DEWALT": "https://meli.la/1Lj62wM",
            "BLACK+DECKER": "https://meli.la/2cg9Ew4",
            "STANLEY": "https://meli.la/2YoHTgT",
            "MONDIAL": "https://meli.la/2yH2xvM",
            "PHILCO": "https://meli.la/29EsFhi",
            "VONDER": "https://meli.la/1NwzU1H",
        }
    },
    "serra_marmore": {
        "icone": "🔧",
        "nome": "SERRA MÁRMORE",
        "marcas": {
            "BOSCH": "https://meli.la/16m4wJn",
            "DEWALT": "https://meli.la/1peLUGn",
            "SKIL": "https://meli.la/2kcR4T3",
            "VONDER": "https://meli.la/2Hdyim9",
            "BLACK+DECKER": "https://meli.la/1ptasFd",
            "WESCO": "https://meli.la/1xKyWMe",
            "STANLEY": "https://meli.la/2tANx4w",
            "DWT": "https://meli.la/1ppmtmE",
            "GAMMA": "https://meli.la/1PA6MUR",
        }
    },
    "furadeira": {
        "icone": "⚡",
        "nome": "FURADEIRA",
        "marcas": {
            "BOSCH": "https://meli.la/1rTGEXr",
            "MAKITA": "https://meli.la/1C5PnoK",
            "DEWALT": "https://meli.la/2VeMEBq",
            "BLACK+DECKER": "https://meli.la/24oNzgo",
            "VONDER": "https://meli.la/1KAXyAj",
            "STANLEY": "https://meli.la/1UgDjh9",
            "SKIL": "https://meli.la/1dzZZBC",
            "WAP": "https://meli.la/2pxhPin",
            "WESCO": "https://meli.la/2pD7sRo",
            "MONDIAL": "https://meli.la/1NqpXkj",
        }
    },
    "martelete": {
        "icone": "🔨",
        "nome": "MARTELETE",
        "marcas": {
            "HILTI": "https://meli.la/2qtyLZL",
            "BOSCH": "https://meli.la/1qtahqS",
            "MAKITA": "https://meli.la/2jUiZos",
            "DEWALT": "https://meli.la/1ddicJ8",
            "MILWAUKEE": "https://meli.la/26bQfyA",
            "STANLEY": "https://meli.la/1Ksyh9W",
            "VONDER": "https://meli.la/2TAS8Tr",
            "WESCO": "https://meli.la/2mN7fae",
            "DWT": "https://meli.la/2ZQj5dw",
            "GAMMA": "https://meli.la/1vxe1wi",
        }
    },
    "esmerilhadeira": {
        "icone": "⚙️",
        "nome": "ESMERILHADEIRA",
        "marcas": {
            "MAKITA": "https://meli.la/199YrBZ",
            "BOSCH": "https://meli.la/1x2FruA",
            "DEWALT": "https://meli.la/1LazRn9",
            "MILWAUKEE": "https://meli.la/1nbm7VS",
            "BLACK+DECKER": "https://meli.la/2XW84cb",
            "VONDER": "https://meli.la/1cNSVjo",
            "WAP": "https://meli.la/22RRtDo",
            "STANLEY": "https://meli.la/2Jgiy9E",
            "SKIL": "https://meli.la/2jsbzwK",
            "WESCO": "https://meli.la/2FyXWD9",
        }
    },
    "lixadeira": {
        "icone": "🧰",
        "nome": "LIXADEIRA / POLRIZ",
        "marcas": {
            "MAKITA": "https://meli.la/1RyDQiu",
            "BOSCH": "https://meli.la/2pJTf1t",
            "DEWALT": "https://meli.la/2M1y9GP",
            "SKIL": "https://meli.la/1iS9Wst",
            "BLACK+DECKER": "https://meli.la/1tCG9cc",
            "VONDER": "https://meli.la/2PXxrKT",
            "STANLEY": "https://meli.la/1ZjWBQp",
            "SIGMA TOOLS": "https://meli.la/1UW3jNP",
            "EINHELL": "https://meli.la/2ZUxoFb",
            "HAMMER": "https://meli.la/1yGorSj",
        }
    },
    "solda": {
        "icone": "🔥",
        "nome": "MÁQUINA DE SOLDA",
        "marcas": {
            "ESAB": "https://meli.la/2xSkHub",
            "BOXER": "https://meli.la/18cXM24",
            "VONDER": "https://meli.la/19rHc2y",
            "BELZER": "https://meli.la/1RmfB9X",
            "STANLEY": "https://meli.la/2otoL5c",
            "LYNUS": "https://meli.la/2KQcnqx",
            "TEKNA": "https://meli.la/21ZwQBT",
            "TITANIUM": "https://meli.la/1miUfDe",
            "SUPER TORK": "https://meli.la/2YCDArx",
            "NAGANO": "https://meli.la/2662847",
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
# FUNÇÃO AUXILIAR PARA CRIAR TECLADOS DE MARCAS DINAMICAMENTE
# ============================================================

def criar_teclado_marcas(produto_chave: str) -> InlineKeyboardMarkup:
    marcas = CATALOGO[produto_chave]["marcas"]
    chaves = list(marcas.keys())
    
    botoes = []
    for i in range(0, len(chaves), 2):
        linha = [InlineKeyboardButton(chaves[i], callback_data=f"marca_{produto_chave}_{chaves[i]}")]
        if i + 1 < len(chaves):
            linha.append(InlineKeyboardButton(chaves[i+1], callback_data=f"marca_{produto_chave}_{chaves[i+1]}"))
        botoes.append(linha)
    
    botoes.append([InlineKeyboardButton("◀️ VOLTAR ÀS FERRAMENTAS", callback_data="menu_ferramentas")])
    return InlineKeyboardMarkup(botoes)


# ============================================================
# /START — MENSAGEM DE BOAS-VINDAS
# ============================================================

async def iniciar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    usuario = update.effective_user
    nome = usuario.first_name or "amigo"

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGEM_URL,
        caption=(
            f"👋 OLÁ, {nome.upper()}!\n"
            "SEJA MUITO BEM-VINDO!\n\n"
            "🛠️ EU SOU O MARLIN DAS OFERTAS!\n\n"
            "Seu parceiro de confiança nas melhores "
            "oportunidades do Mercado Livre! 💎\n\n"
            "Aqui você encontra as melhores marcas, "
            "os melhores preços e produtos de qualidade! 💰\n\n"
            "🛍️ FERRAMENTAS\n"
            "🔋 GRANDES MARCAS\n\n"
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

    if texto == "🔴 INÍCIO":
        await iniciar(update, context)

    elif texto == "🔵 FERRAMENTAS":
        # Menu de escolha principal de ferramentas
        await update.message.reply_text(
            "🛠️ FERRAMENTAS\n\n"
            "Escolha o que você está procurando:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔋 PARAFUSADEIRAS", callback_data="lista_parafusadeira")],
                [InlineKeyboardButton("🔧 SERRAS MÁRMORE", callback_data="lista_serra_marmore")],
                [InlineKeyboardButton("⚡ FURADEIRAS", callback_data="lista_furadeira")],
                [InlineKeyboardButton("🔨 MARTELETES", callback_data="lista_martelete")],
                [InlineKeyboardButton("⚙️ ESMERILHADEIRAS", callback_data="lista_esmerilhadeira")],
                [InlineKeyboardButton("🧰 LIXADEIRAS / POLRIZES", callback_data="lista_lixadeira")],
                [InlineKeyboardButton("🔥 MÁQUINAS DE SOLDA", callback_data="lista_solda")],
                [InlineKeyboardButton("◀️ VOLTAR AO INÍCIO", callback_data="menu_inicial")]
            ])
        )

    elif texto == "📋 SOBRE NÓS":
        await update.message.reply_text(
            "🔥 QUEM SOMOS NÓS?\n\n"
            "Somos o MARLIN DAS OFERTAS — conectando você "
            "as melhores promoções do Mercado Livre! 🛍️\n\n"
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

    if dados == "menu_inicial":
        await query.message.delete()
        await iniciar(update, context)

    elif dados == "menu_ferramentas":
        await query.edit_message_text(
            "🛠️ FERRAMENTAS\n\n"
            "Escolha o que você está procurando:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔋 PARAFUSADEIRAS", callback_data="lista_parafusadeira")],
                [InlineKeyboardButton("🔧 SERRAS MÁRMORE", callback_data="lista_serra_marmore")],
                [InlineKeyboardButton("⚡ FURADEIRAS", callback_data="lista_furadeira")],
                [InlineKeyboardButton("🔨 MARTELETES", callback_data="lista_martelete")],
                [InlineKeyboardButton("⚙️ ESMERILHADEIRAS", callback_data="lista_esmerilhadeira")],
                [InlineKeyboardButton("🧰 LIXADEIRAS / POLRIZES", callback_data="lista_lixadeira")],
                [InlineKeyboardButton("🔥 MÁQUINAS DE SOLDA", callback_data="lista_solda")],
                [InlineKeyboardButton("◀️ VOLTAR AO INÍCIO", callback_data="menu_inicial")]
            ])
        )

    elif dados.startswith("lista_"):
        produto_chave = dados.replace("lista_", "")
        info = CATALOGO[produto_chave]

        await query.edit_message_text(
            f"{info['icone']} {info['nome']} — ESCOLHA A MARCA!\n\n"
            "Clique na marca para ver as ofertas disponíveis! 🎯",
            reply_markup=criar_teclado_marcas(produto_chave)
        )

    elif dados.startswith("marca_"):
        partes = dados.split("_", 2)
        produto_chave = partes[1]
        marca = partes[2]

        link = CATALOGO[produto_chave]["marcas"][marca]
        info = CATALOGO[produto_chave]

        await query.edit_message_text(
            f"✅ EXCELENTE ESCOLHA!\n\n"
            f"🔹 PRODUTO: {info['nome']}\n"
            f"🔹 MARCA: {marca}\n\n"
            "🛍️ Acesse agora e confira os melhores preços:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        f"🛍️ VER {marca} NO MERCADO LIVRE",
                        url=link
                    )
                ],
                [
                    InlineKeyboardButton(
                        "◀️ VOLTAR ÀS MARCAS",
                        callback_data=f"lista_{produto_chave}"
                    )
                ]
            ])
        )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("comecar", iniciar))
    app.add_handler(CommandHandler("start", iniciar))
    app.add_handler(CallbackQueryHandler(acao_botao))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_rodape))

    logger.info("=" * 60)
    logger.info("🔥 MARLIN DAS OFERTAS — TUDO FUNCIONANDO!")
    logger.info("=" * 60)

    app.run_polling(drop_pending_updates=True)


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()
