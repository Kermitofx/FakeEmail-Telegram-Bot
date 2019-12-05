import telebot
import redis
r = redis.Redis('localhost')
from tempmail import TempMail
token = '951045807:AAGo-mPp7NhjcYT05t3IXwUU9SyVABA1nNI' #put your token here
bot = telebot.TeleBot(token)
user = bot.get_me().username
@bot.message_handler(commands=['start'])
def start(m):
  # start text
  text = 'ðŸ“§Oi.\nBem-vindo {}.\nCommands: \n/newemail: Para fazer um novo e-mail.\n/emails: Para ler novos e-mails.\nDeveloped by @Fraviin'.format(user)
  bot.send_message(m.chat.id, text)
@bot.message_handler(commands=['newemail'])
def newmail(m):
        #initialize Temp-Male and making a new Email.
        tm = TempMail()
        email = tm.get_email_address()
        r.set('email:{}:mail'.format(str(m.from_user.id)), email)
        bot.send_message(m.chat.id, 'ðŸ“§Seu novo e-mail: '+email)
@bot.message_handler(commands=['emails'])
def mails(m):
    try :
        #initialize Temp-Male and read recieved Mails.
        mail = r.get('email:{}:mail'.format(str(m.from_user.id)))
        if not mail:
                bot.send_message(m.from_user.id, 'ðŸ“§Faça um e-mail primeiro.\nUsar /newemail')
                return
        parts = mail.split('@')
        tm = TempMail(login=parts[0], domain='@'+parts[1])
        mails = tm.get_mailbox()
        if not mails :
                bot.send_message(m.from_user.id, 'ðŸ“­Não há e-mail...')
        else:
            if 'error' in mails :
                bot.send_message(m.from_user.id, 'ðŸ“­Não há e-mail...')
            else:
                print mails
                for i in mails:
                        bot.send_message(m.from_user.id, 'ðŸ“¬E-mail de: '+i['mail_from']+'\n\nAssunto: '+i['mail_subject']+'\n\nTexto: ' +i['mail_text'])
    except:
        bot.send_message(m.from_user.id, 'ðŸ“­Não há e-mail...')

bot.polling()
