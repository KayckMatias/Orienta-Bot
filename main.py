import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ["API_TOKEN"]

estagioBot = telebot.TeleBot(token=chave_api)

#Teclado Start
keyboardStart = InlineKeyboardMarkup()
button_start = InlineKeyboardButton("Start", callback_data="start")
keyboardStart.add(button_start)

#Teclado Sim / Não
keyboardSN = InlineKeyboardMarkup()
buttonSim = InlineKeyboardButton("Sim", callback_data="Sim")
buttonNao = InlineKeyboardButton("Não", callback_data="Nao")
keyboardSN.add(buttonSim, buttonNao)

@estagioBot.callback_query_handler(func= lambda call: call.data == "Sim" or call.data == "Nao")
def responseSN(callback):
    if (callback.data == "Sim"):
        command_duvidas(callback.message)

    elif (callback.data == "Nao"):
        estagioBot.reply_to(callback.message, "Obrigado por utilizar, Nos ajude dando um feedback")


#Resposta padrão do bot caso não seja um comando
@estagioBot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    estagioBot.reply_to(message, 'Para utilizar o bot, comece com o botão start abaixo', reply_markup=keyboardStart)

@estagioBot.callback_query_handler(func= lambda call: call.data == "start")
def callback_start(callback):
    handle_start(callback.message)

#Teclado inicial
keyboardInicio = InlineKeyboardMarkup()
button_sobre = InlineKeyboardButton('Sobre', callback_data="sobre")
button_duvidas = InlineKeyboardButton('Duvidas', callback_data="duvidas")
keyboardInicio.add(button_sobre, button_duvidas)

@estagioBot.message_handler(commands=['start'])
def handle_start(message):
    texto = "Olá, seja bem vindo! \nEsse é o Orienta Bot. para prosseguir, escolha uma das opções"
    estagioBot.reply_to(message, texto, reply_markup=keyboardInicio)


@estagioBot.message_handler(commands=['sobre'])
def command_sobre(message):
    estagioBot.reply_to(message, "Explicação do projeto")
    estagioBot.reply_to(message, "Deseja ver alguma das dúvidas respondidas?", reply_markup=keyboardSN)

@estagioBot.callback_query_handler(func= lambda call: call.data == "sobre")
def callback_sobre(callback):
    command_sobre(callback.message)


keyboardDuvidas = InlineKeyboardMarkup()
empresa = InlineKeyboardButton("Empresa", callback_data="empresa")
checkEstagiario = InlineKeyboardButton("Checklist Estagiário", callback_data="checklistEstagio")
sice = InlineKeyboardButton("Sice", callback_data="sice")
dicasRelatorio = InlineKeyboardButton("Dicas Relatorio", callback_data="dicasRelatorio")
mediacao = InlineKeyboardButton("Mediação", callback_data= "mediacao")
bolsaEstagio = InlineKeyboardButton("Bolsa Estagio", callback_data="bolsaEstagio")
keyboardDuvidas.row(empresa, checkEstagiario).row(sice, dicasRelatorio).row(mediacao, bolsaEstagio)

@estagioBot.message_handler(commands=["duvidas"])
def command_duvidas(message):
    
    texto = "Essas são as dúvidas respondidas, escolha alguma para poder ver as respostas"
    estagioBot.reply_to(message, texto, reply_markup=keyboardDuvidas)

@estagioBot.callback_query_handler(func= lambda call: call.data == "duvidas")
def callback_duvidas(callback):
    command_duvidas(callback.message)
        

estagioBot.polling()