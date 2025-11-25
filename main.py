import telebot
import random
import os
from clasificator import classification
# Замени '#' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("#")

birds = {"голубь": "Голубей следует кормить смесью злаков, таких как перловка, пшеница, просо, ячмень, горох и семена, а также зеленью и овощами. Нельзя давать им хлеб, соленые, жареные и молочные продукты. Для поддержания здоровья в рацион можно добавлять яичную скорлупу и безмолочные детские каши.",
         "синица": "Синиц следует кормить несолёными и нежареными семечками подсолнечника, тыквы, а также несолёным салом, орехами, крупами (пшено, овёс) и кусочками свежих яблок или моркови. Важно избегать жареных и соленых продуктов, хлеба, а также цитрусовых и соленого сала, которые могут навредить птицам.",
         "воробей": "Воробьев можно кормить смесью из зерновых культур: просо, овес, семечки подсолнуха и семена тыквы, а также сухим белым хлебом. Важно использовать нерафинированные зерна (неочищенное просо предпочтительнее, чем пшено), а для птенцов требуется специально приготовленная мешанка из вареного яйца, вареного пшена, мелко нарезанного вареного мяса, тертой моркови и дафний."}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=['hello', 'hi'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    if not message.photo:
        return(bot.send_message(message.chat.id, "Изображение не было загружено!"))
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open (file_name, "wb") as f:
        f.write(downloaded_file)
    result = classification("./Models/birds.h5", "./Models/birds.txt", file_name)
    name = result[0].replace("\n", "")
    procent = int(result[1]*100)
    bot.reply_to(message, f"На изображении {name}, с вероятностю {procent}%. {birds[name.lower()]}")
    os.remove(f"./{file_name}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text !="орел" and message.text !="решка":

        bot.reply_to(message, message.text)
    else:
        monetka= random.choice(["орел", "решка"])
        if message.text == monetka:
            bot.reply_to(message, "Вы угадали!")
        else:
            bot.reply_to(message, "Вы не угадали!")
bot.polling()
