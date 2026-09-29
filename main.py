import os
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (certifique-se de ter o GROQ_API_KEY no seu .env ou substitua abaixo)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️ ERRO: A chave GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
    exit()

# Inicializa o cliente da Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# Instrução de Sistema: Define a personalidade e o comportamento conversacional da IA
system_instruction = (
    "Tu és o assistente de vendas e especialista em produtos do **MERCADO LIVRE**. "
    "O teu objetivo principal é conversar de forma natural e amigável com o cliente, fazer perguntas inteligentes "
    "para descobrir exatamente o que ele procura (como faixa de preço, marca desejada, finalidade do produto) "
    "e ajudá-lo a encontrar a melhor opção antes de sugerir links de compra. "
    "REGRA OBRIGATÓRIA 1: Escreve INTEIRAMENTE EM LETRAS MAIÚSCULAS (CAPSLOCK). "
    "REGRA OBRIGATÓRIA 2: Sê dinâmico, usa emojis comerciais, sê prestativo e nunca encerre a conversa de forma seca; faça sempre uma pergunta para continuar o diálogo."
)

def testar_chat():
    print("=" * 60)
    print("🤖 TESTE DE CONVERSA COM A IA DO MERCADO LIVRE")
    print("Digite 'sair' para encerrar o teste.")
    print("=" * 60)

    # Histórico para manter o contexto da conversa (lembrar o que foi dito antes)
    mensagens_historico = [
        {"role": "system", "content": system_instruction}
    ]

    while True:
        try:
            user_input = input("\n👤 Você (Cliente): ")
            if user_input.strip().lower() == 'sair':
                print("Encerrando teste...")
                break

            if not user_input.strip():
                continue

            # Adiciona a mensagem do utilizador ao histórico
            mensagens_historico.append({"role": "user", "content": user_input})

            # Envia para a Groq mantendo o histórico da conversa
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensagens_historico,
                temperature=0.7,
                max_tokens=1024,
            )

            ai_response = completion.choices[0].message.content

            # Mostra a resposta da IA
            print(f"\n🤖 IA (Marlin das Ofertas): {ai_response}")

            # Adiciona a resposta da IA ao histórico para ela lembrar na próxima frase
            mensagens_historico.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            print(f"\n❌ Erro na comunicação com a API: {e}")

if __name__ == "__main__":
    testar_chat()
