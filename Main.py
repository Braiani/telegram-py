import telebot
from Database import Database
from dotenv import load_dotenv
from DiarioMS import DiarioMS
import os

def show_messages_info(message):
    for key, value in message.__dict__.items():
        print(f'{key}: {value}')

def connect_db():
    try:
        db = Database('database.db')
        return db
    except Exception as e:
        print(f'Erro ao conectar com o banco de dados: {e}')
        return False

def get_info_from_env():
    try:
        load_dotenv()
        return {
            'CHAVE_API': os.getenv('CHAVE_API', '')
        }
    except Exception as e:
        print(f'Erro ao carregar variáveis de ambiente: {e}')
        return False


def main():
    chave_api = get_info_from_env()['CHAVE_API']
    bot = telebot.TeleBot(chave_api)
    connection = connect_db()
    log_messages = False

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        if log_messages:
            show_messages_info(message)
        bot.reply_to(message, f"Olá {message.from_user.first_name}! Como posso ajudar?")

    @bot.message_handler(commands=['verificar_diario'])
    def check_diary(message):
        if log_messages:
            show_messages_info(message)
        bot.send_message(message.chat.id, 'Vamos verificar o diário do MS dos últimos 60 dias...')
        bot.send_message(message.chat.id, 'Marque essa mensagem com o texto que deseja buscar')

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        if log_messages:
            show_messages_info(message)

        if message.json.get('reply_to_message', False):
            if message.json['reply_to_message']['text'] == 'Marque essa mensagem com o texto que deseja buscar':
                texto_busca = message.text
                diario = DiarioMS(texto_busca)
                bot.reply_to(message, diario.location_text())
                result = diario.get_diarios()
                bot.send_message(message.chat.id, result)
            else:
                bot.reply_to(message, 'Não entendi o que você quer, por favor, tente novamente')
            return
        bot.send_message(message.chat.id, message.text)

    bot.infinity_polling()


if __name__ == '__main__':
    main()