#!/usr/bin/env python3
# -*- codificação: utf-8 -*-

importar os
importação de registro

from dotenv import load_dotenv

importação do Telegram (
    Atualizar,
    RespostaKeyboardMarkup,
    Botão de teclado embutido,
    Marcação de teclado embutida,
)

from telegram.ext import (
    Aplicativo,
    Manipulador de Comandos,
    CallbackQueryHandler,
    ManipuladorDeMensagens,
    filtros,
    Tipos de contexto,
)


# ============================================================
# CONFIGURARÃ‡ÃƒO
# ============================================================

carregar_dotenv()

TOKEN = os.getenv("TOKEN")

se não for TOKEN:
    raise SystemExit("â Œ Verifique o TOKEN no .env!")


# ============================================================
# REGISTRO
# ============================================================

registro.configuração básica(
    nível=registro.INFO,
    formato="%(asctime)s | %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# IMAGEM DE BOAS-VINDAS
# ============================================================

IMAGEM_URL = "https://i.ibb.co/JRvr5XjN/file-00000000e2f4820e905136c406931929.png"


# ============================================================
# LOGOTIPO CATÃ
# ============================================================

CATÁLOGO = {
    "parafusadeira": {
        "ícone": "ðŸ”©",
        "nome": "PARAFUSADEIRA",

        "marcas": {
            "BOSCH": "https://meli.la/1GtWTR",
            "MAKITA": "https://meli.la/1MjEzBC",
            "DEWALT": "https://meli.la/1Lj62wM"
            "BLACK+DECKER": "https://meli.la/2cg9Ew4",
            "STANLEY": "https://meli.la/2YoHTgT",
            "MONDIAL": "https://meli.la/2yH2xvM",
            "PHILCO": "https://meli.la/29EsFhi",
            "VONDER": "https://meli.la/1NwzU1H",
        }
    }
}


# ============================================================
# TECLADO FIXO DO RODAPÉ‰
# ============================================================

def teclado_rodape() -> ReplyKeyboardMarkup:

    retornar ReplyKeyboardMarkup(
        [
            ["ðŸ”´ INÍCIO", "ðŸ”µ FERRAMENTAS"],
            ["ðŸ“‹ SOBRE NÃ“S"]
        ],

        redimensionar_teclado=Verdadeiro,
        one_time_keyboard=False,
        é_persistente=Verdadeiro,
        seletivo=Falso
    )


# ============================================================
# MENU DE MARCAS
# ============================================================

def teclado_marcas() -> InlineKeyboardMarkup:

    retornar InlineKeyboardMarkup([

        [
            Botão de teclado embutido(
                "BOSCH",
                callback_data="marca_BOSCH",
                estilo="primário"
            ),

            Botão de teclado embutido(
                "MAKITA",
                callback_data="marca_MAKITA",
                estilo="primário"
            )
        ],

        [
            Botão de teclado embutido(
                "DEWALT",
                callback_data="marca_DEWALT",
                estilo="primário"
            ),

            Botão de teclado embutido(
                "BLACK+DECKER",
                callback_data="marca_BLACK+DECKER",
                estilo="primário"
            )
        ],

        [
            Botão de teclado embutido(
                "STANLEY",
                callback_data="marca_STANLEY",
                estilo="primário"
            ),

            Botão de teclado embutido(
                "MONDIAL",
                callback_data="marca_MONDIAL",
                estilo="primário"
            )
        ],

        [
            Botão de teclado embutido(
                "PHILCO",
                callback_data="marca_PHILCO",
                estilo="primário"
            ),

            Botão de teclado embutido(
                "VONDER",
                callback_data="marca_VONDER",
                estilo="primário"
            )
        ],

        [
            Botão de teclado embutido(
                "â¬…ï¸ VOLTAR",
                callback_data="menu_inicial",
                estilo="perigo"
            )
        ]
    ])


# ============================================================
# /START — MENSAGEM DE BOAS-VINDAS
# ============================================================

async def iniciar(
    Atualização: Atualização,
    contexto: ContextTypes.DEFAULT_TYPE
):

    usuário = atualizar.usuário_efetivo

    nome = usuário.first_name ou "amigo"

    aguarde context.bot.send_photo(

        chat_id=update.effective_chat.id,

        foto=URL_DA_IMAGEM,

        legenda=(

            f"ðŸ OLÃ , {nome.upper()}! "
            "SEJA MUITO BEM-VINDO!\n\n"

            "ðŸ”§ EU SOU O MARLIN DAS OFERTAS!\n\n"

            "Seu parceiro de confiança nas melhores"
            "oportunidades do Mercado Livre! ðŸ'Ž\n\n"

            "Aqui você encontra as melhores marcas",
            "os melhores preços e produtos de qualidade! ðŸ'°\n\n"

            "ðŸ› ï¸ FERRAMENTAS\n"
            "ðŸ”© PARAFUSADEIRAS\n"
            "â GRANDES MARCAS\n\n"

            "ðŸ'‡ Escolha uma opção abaixo e vamos lá!"
        ),

        reply_markup=teclado_rodape()
    )


# ============================================================
# BOTAS DO RODAPÉ
# ============================================================

async def mensagem_rodape(
    Atualização: Atualização,
    contexto: ContextTypes.DEFAULT_TYPE
):

    texto = update.message.text.strip()


    # --------------------------------------------------------
    # INÃ CIO
    # --------------------------------------------------------

    if texto == "ðŸ”´ INÍCIO":

        aguardar início(atualização, contexto)


    # --------------------------------------------------------
    # FERRAMENTAS
    # --------------------------------------------------------

    elif texto == "ðŸ”µ FERRAMENTAS":

        aguarde update.message.reply_text(

            "ðŸ› ï¸ FERRAMENTAS\n\n"
            "Escolha o que você está procurando:",

            reply_markup=InlineKeyboardMarkup([

                [
                    Botão de teclado embutido(
                        "ðŸ”© PARAFUSADEIRAS",
                        callback_data="lista_parafusadeira",
                        estilo="primário"
                    )
                ],

                [
                    Botão de teclado embutido(
                        "â¬…ï¸ VOLTAR AO INÍCIO",
                        callback_data="menu_inicial",
                        estilo="perigo"
                    )
                ]

            ])
        )


    # --------------------------------------------------------
    # SOBRE NÓS
    # --------------------------------------------------------

    elif texto == "ðŸ“‹ SOBRE NÓS":

        aguarde update.message.reply_text(

            "ðŸ”¥ QUEM SOMOS NÓS?\n\n"

            "Somos o MARLIN DAS OFERTAS — conectando você"
            "As melhores promoções do Mercado Livre! ðŸ›'\n\n"

            "âœ… Produtos de qualidade\n"
            "âœ… Marcas confiáveis\n"
            "âœ…Preços direto da fonte\n"
            "âœ…Segurança em cada compra\n\n"

            "Escolha uma opção abaixo e comece a economizar! ðŸ'¸",

            reply_markup=teclado_rodape()
        )


# ============================================================
# AÃ‡Ã•ES DOS BOTÃ•ES INLINE
# ============================================================

def assíncrona acao_botao(
    Atualização: Atualização,
    contexto: ContextTypes.DEFAULT_TYPE
):

    consulta = atualização.callback_query

    aguarde a consulta.resposta()

    dados = consulta.dados


    # --------------------------------------------------------
    # VOLTAR AO MENU INICIAL
    # --------------------------------------------------------

    se dados == "menu_inicial":

        aguardar início(atualização, contexto)


    # --------------------------------------------------------
    # LISTA DE PARAFUSADEIRAS
    # --------------------------------------------------------

    elif dados == "lista_parafusadeira":

        aguarde query.edit_message_text(

            "ðŸ”© PARAFUSADEIRAS — ESCOLHA A MARCA!\n\n"

            "Clique na marca para ver as ofertas disponíveis! ðŸŽ¯",

            reply_markup=teclado_marcas()
        )


    # --------------------------------------------------------
    # MARCA SELECIONADA
    # --------------------------------------------------------

    elif dados.startswith("marca_"):

        marca = dados.replace("marca_", "")

        link = CATALOGO["parafusadeira"]["marcas"][marca]


        aguarde query.edit_message_text(

            f"âœ… EXCELENTE ESCOLHA!\n\n"

            f"ðŸ”¹ PRODUTO: PARAFUSADEIRA\n"
            f"ðŸ”¹ MARCA: {marca}\n\n"

            "ðŸ›' Acesse agora e confira os melhores preços:",

            reply_markup=InlineKeyboardMarkup([

                [
                    Botão de teclado embutido(
                        f"ðŸ›' VER {marca} NO MERCADO LIVRE",
                        url=link,
                        estilo="primário"
                    )
                ],

                [
                    Botão de teclado embutido(
                        "â¬…ï¸ VOLTAR ÀS MARCAS",
                        callback_data="lista_parafusadeira",
                        estilo="perigo"
                    )
                ]

            ])
        )


# ============================================================
# INICIALIZAÇÃOÃ‡ÃƒO
# ============================================================

def main():

    app = Application.builder().token(TOKEN).build()


    # /começar
    app.add_handler(
        ManipuladorDeComandos(
            "começar",
            começar
        )
    )


    # Botãs em linha
    app.add_handler(
        CallbackQueryHandler(
            acao_botao
        )
    )


    # Botãs do rodapé
    app.add_handler(
        ManipuladorDeMensagens(
            filtros.TEXTO e ~filtros.COMANDO,
            mensagem_rodape
        )
    )


    logger.info("=" * 60)

    logger.info(
        "ðŸ MARLIN DAS OFERTAS — BOTÃ•ES AZUIS!"
    )

    logger.info(
        "âœ… Nova imagem de ferramentas definidas"
    )

    logger.info(
        "âœ… Imagem aparece na mensagem de boas-vindas"
    )

    logger.info(
        "âœ… Rodapé persistente"
    )

    logger.info(
        "âœ… Todas as marcas em azul"
    )

    logger.info(
        "âœ… Botões VOLTAR em vermelho"
    )

    logger.info(
        "âœ…Parafusadeiras dentro de Ferramentas"
    )

    logger.info("=" * 60)


    # Inicia o bot
    app.run_polling(
        drop_pending_updates=True
    )


# ============================================================
# EXECUTAR
# ============================================================

se __name__ == "__main__":
    principal()
