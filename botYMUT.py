import logging
import time
import shutil
from typing import Dict
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application,CallbackContext,CommandHandler,ConversationHandler,MessageHandler,filters,)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
LOGIN,PASSWORD,ARTIST,TRACKNAME,TRACK,PHOTO = range(6)

reply_keyboard1 = [["/upload"],["/find"],["/logout"]]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)
reply_keyboard2 = [["/cancel"]]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
reply_keyboard = [["/start"],["/cancel"],["/logout"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def cancel(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_text("Вход отменен",reply_markup=markup,)
    return ConversationHandler.END

async def cancel1(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    userid=update.effective_chat.id
    user_data = context.user_data
    user_data.clear()
    namefilemp3way="D:/bot_v2/" +str(userid)+".mp3"
    namefilejpg="D:/bot_v2/"+str(userid)+".jpg"
    namefilejpg="D:/bot_v2/"+str(userid)+".jpg"
    try:
        os.remove(namefilemp3way)
        os.remove(namefilejpg)
        os.remove("C:/Users/Professional/Downloads/tagmp3_"+namefilemp3)
        await update.message.reply_text("Загрузка отменена",reply_markup=markup1,)
        return ConversationHandler.END
    except:
        try:
            os.remove(namefilemp3way)
            os.remove(namefilejpg)
            await update.message.reply_text("Загрузка отменена",reply_markup=markup1,)
            return ConversationHandler.END
        except:
            try:
                os.remove(namefilemp3way)
                await update.message.reply_text("Загрузка отменена",reply_markup=markup1,)
                return ConversationHandler.END
            except:
                await update.message.reply_text("Загрузка отменена",reply_markup=markup1,)
                return ConversationHandler.END

async def cancel2(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Загрузка отменена",reply_markup=markup1,)
    return ConversationHandler.END

async def logout(update: Update, context: CallbackContext.DEFAULT_TYPE):
    userid=update.effective_chat.id
    try:
        try:
            os.remove(str(userid)+".txt")
            shutil.rmtree('D:/Profiles/Profile 1332248807')
            await update.message.reply_text("Выход из аккаунта выполнен",reply_markup=markup,)
            return ConversationHandler.END
        except:
            os.remove(str(userid)+".txt")
            await update.message.reply_text("Выход из аккаунта выполнен",reply_markup=markup,)
            return ConversationHandler.END
    except:
        await update.message.reply_text("Выход из аккаунта не выполнен повтори попытку",reply_markup=markup,)
        return ConversationHandler.END
        

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    userid=update.effective_chat.id
    try:
        os.remove(str(userid)+".txt")
        await update.message.reply_text("Привет это Бот загрузки mp3 на Яндекс Музыку (Для корректной работы бота надо включить авторизацию через Яндекс Ключ https://yandex.ru/support/id/authorization/twofa-on.html) , для продолжения отправь логин без @yandex.ru",reply_markup=markup2,)
        return LOGIN
    except:
        await update.message.reply_text("Привет это Бот загрузки mp3 на Яндекс Музыку (Для корректной работы бота надо включить авторизацию через Яндекс Ключ https://yandex.ru/support/id/authorization/twofa-on.html) , для продолжения отправь логин без @yandex.ru",reply_markup=markup2,)
        return LOGIN

async def login(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["Login"] = text
    await update.message.reply_text("Отправь одноразовый пароль из Яндекс Ключ",reply_markup=markup2,)
    return PASSWORD

async def password(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    pas=update.message.text
    userid=update.effective_chat.id
    log = facts_to_str(user_data)
    user_data.clear()
    log=' '.join(log.split())
    log=log.replace('Login - ', '')
    my_file = open(str(userid)+".txt", "w")
    my_file.write(log)
    my_file.close()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir=D:\Profiles')
        options.add_argument('--profile-directory=Profile '+str(userid))
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://music.yandex.ru/users/'+log+'/playlists/3')
        main_page = driver.current_window_handle
        time.sleep(1)
        driver.refresh()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Войти"))).click()
        time.sleep(2)
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle
                break

        driver.switch_to.window(login_page)
        try:
            driver.find_element(by=By.XPATH, value="//div[@class='AuthLoginInputToggle-type']/button").click()
            time.sleep(2)
            try:
                driver.find_element_by_id('passp-field-login').send_keys(log)
                login_button = driver.find_element_by_id('passp:sign-in').click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Или войдите по одноразовому паролю"))).click()
                time.sleep(2)
                driver.find_element_by_id('passp-field-passwd').send_keys(pas)
                password_button = driver.find_element_by_id('passp:sign-in').click()
                time.sleep(5)
                driver.switch_to.window(main_page)
                driver.close()
                await update.message.reply_text("Вход выполнен",reply_markup=markup1,)
                return ConversationHandler.END
            except:
                driver.find_element(by=By.XPATH, value="//div[@class='AuthLoginInputToggle-type']/button").click()
                time.sleep(2)
                driver.find_element_by_id('passp-field-login').send_keys(log)
                login_button = driver.find_element_by_id('passp:sign-in').click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Или войдите по одноразовому паролю"))).click()
                time.sleep(2)
                driver.find_element_by_id('passp-field-passwd').send_keys(pas)
                password_button = driver.find_element_by_id('passp:sign-in').click()
                time.sleep(5)
                driver.switch_to.window(main_page)
                driver.close()
                await update.message.reply_text("Вход выполнен",reply_markup=markup1,)
                return ConversationHandler.END
                
        except:
            driver.find_element_by_id('passp-field-login').send_keys(log)
            login_button = driver.find_element_by_id('passp:sign-in').click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Или войдите по одноразовому паролю"))).click()
            time.sleep(2)
            driver.find_element_by_id('passp-field-passwd').send_keys(pas)
            password_button = driver.find_element_by_id('passp:sign-in').click()
            time.sleep(5)
            driver.switch_to.window(main_page)
            driver.close()
            await update.message.reply_text("Вход выполнен",reply_markup=markup1,)
            return ConversationHandler.END
    except:
        await update.message.reply_text("Вход не выполнен повтор попытку",reply_markup=markup,)
        return ConversationHandler.END

async def upload(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Отправь имя артиста",reply_markup=markup2,)
    return ARTIST

async def artist(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        text=text.replace(' ', '[]')
        context.user_data["Артист"] = text
        await update.message.reply_text("Напиши название трека")
        return TRACKNAME
    except:
        await update.message.reply_text("Ошибка, отправь корректно имя артиста")
        return ARTIST

async def trackname(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        text=text.replace(' ', '[]')
        context.user_data["Название трека"] = text
        await update.message.reply_text("Отправь обложку")
        return PHOTO
    except:
        await update.message.reply_text("Ошибка, отправь корректно название трека")
        return TRACKNAME


async def photo(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    userid=update.effective_chat.id
    await photo_file.download(str(userid)+".jpg")
    await update.message.reply_text("Отправь трек")
    return TRACK

async def audio(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    userid=update.effective_chat.id
    title=''
    artist=''
    tmp=''
    user_data = context.user_data
    tmp = facts_to_str(user_data)
    user_data.clear()
    tmp=' '.join(tmp.split())
    tmp=tmp.replace('Артист - ', '')
    tmp=tmp.replace('Название трека - ', '')
    arr=tmp.split()
    user_data.clear()
    for i in range(2):
        artist=arr[0]
        title=arr[1]
    artist=artist.replace('[]', ' ')
    title=title.replace('[]', ' ')
    namefilemp3=str(userid)+".mp3"
    namefilemp3way="D:/bot_v2/" +str(userid)+".mp3"
    namefilejpg="D:/bot_v2/"+str(userid)+".jpg"
    user = update.message.from_user
    photo_file = await update.message.audio.get_file()
    await photo_file.download(str(userid)+".mp3")
    log = str(userid)
    my_file = open(log+".txt", "r")
    log = my_file.read()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(r'user-data-dir=D:\Profiles')
        options.add_argument('--profile-directory=Profile '+str(userid))
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://tagmp3.net/ru/')
        time.sleep(5)  
        driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(namefilemp3way)
        time.sleep(30)
        driver.find_element(by=By.XPATH, value="//input[@name='apic_0']").send_keys(namefilejpg)
        driver.find_element(by=By.XPATH, value="//input[@name='tit2_0']").clear()
        driver.find_element(by=By.XPATH, value="//input[@name='tpe1_0']").clear()
        driver.find_element(by=By.XPATH, value="//input[@name='tit2_0']").send_keys(title)
        driver.find_element(by=By.XPATH, value="//input[@name='tpe1_0']").send_keys(artist)
        driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, namefilemp3))).click()
        time.sleep(30)
        driver.get('https://music.yandex.ru/users/'+log+'/playlists/3')
        time.sleep(5)
        driver.find_element(by=By.XPATH, value="//span[@class='ugc-loader__button']/button").click()
        time.sleep(2)
        driver.find_element(by=By.XPATH, value="//div[@class='ugc-loader__actions']/button").click()
        driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys("C:/Users/Professional/Downloads/tagmp3_"+namefilemp3)
        time.sleep(30)
        driver.close()
        try:
            os.remove(namefilemp3way)
            os.remove(namefilejpg)
            shutil.move("C:/Users/Professional/Downloads/tagmp3_"+namefilemp3,'D:/MusicList/')
            os.rename('D:/MusicList/tagmp3_'+namefilemp3,'D:/MusicList/'+artist + ' - ' + title+'.mp3')
            await update.message.reply_text("Трек загружен",reply_markup=markup1,)
            return ConversationHandler.END
        except:
            os.remove(namefilemp3way)
            os.remove(namefilejpg)
            os.remove("C:/Users/Professional/Downloads/tagmp3_"+namefilemp3)
            await update.message.reply_text("Трек загружен",reply_markup=markup1,)
            return ConversationHandler.END
    except:
        os.remove(namefilemp3way)
        os.remove(namefilejpg)
        os.remove("C:/Users/Professional/Downloads/tagmp3_"+namefilemp3)
        await update.message.reply_text("Трек не загружен повтори попытку",reply_markup=markup1,)
        return ConversationHandler.END

async def find(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Отправь имя артиста",reply_markup=markup2,)
    return ARTIST

async def audiolist(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = update.message.text
    tmp=''
    mlist=os.listdir('D:/MusicList')
    for i in range(len(mlist)):
        if mlist[i].find(text)!=-1:
            tmp=tmp+mlist[i]+'\n'
    await update.message.reply_text("Найденные треки в библиотеки бота:"+tmp+"Для продолжения напиши название трека",reply_markup=markup1,)
    return TRACKNAME

async def audioupload(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = update.message.text
    tmp=''
    mlist=os.listdir('D:/MusicList')        
    for i in range(len(mlist)):
        if mlist[i].find(text)!=-1:
            tmp=mlist[i]

    userid=update.effective_chat.id
    log = str(userid)
    my_file = open(log+".txt", "r")
    log = my_file.read()
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=D:\Profiles')
    options.add_argument('--profile-directory=Profile '+str(userid))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)       
    driver.get('https://music.yandex.ru/users/'+log+'/playlists/3')
    time.sleep(5)
    driver.find_element(by=By.XPATH, value="//span[@class='ugc-loader__button']/button").click()
    time.sleep(2)
    driver.find_element(by=By.XPATH, value="//div[@class='ugc-loader__actions']/button").click()
    driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys("D:/MusicList/"+tmp)
    time.sleep(30)
    driver.close()
    await update.message.reply_text("Трек загружен",reply_markup=markup1,)
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("5364426029:AAF4NNq9laHXw6UlMalg0huX5-gjTkeeKh0").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start,block=False)],
        states={
            LOGIN: [CommandHandler("cancel", cancel,block=False),MessageHandler(filters.TEXT,login,block=False)],
            PASSWORD: [CommandHandler("cancel", cancel,block=False),MessageHandler(filters.TEXT,password,block=False)],
        },
        fallbacks=[CommandHandler("cancel", cancel,block=False)],
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("upload", upload,block=False),CommandHandler("logout", logout,block=False)],
        states={
            ARTIST: [CommandHandler("cancel", cancel1,block=False),MessageHandler(filters.TEXT,artist,block=False)],
            TRACKNAME: [CommandHandler("cancel", cancel1,block=False),MessageHandler(filters.TEXT, trackname,block=False)],
            PHOTO: [CommandHandler("cancel", cancel1,block=False),MessageHandler(filters.PHOTO, photo,block=False)],
            TRACK: [CommandHandler("cancel", cancel1,block=False),MessageHandler(filters.AUDIO, audio,block=False)],
            },
        fallbacks=[CommandHandler("cancel", cancel1,block=False)],
    )
    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler("find", find,block=False),CommandHandler("logout", logout,block=False)],
        states={
            ARTIST: [CommandHandler("cancel", cancel2,block=False),MessageHandler(filters.TEXT,audiolist,block=False)],
            TRACKNAME: [CommandHandler("cancel", cancel2,block=False),MessageHandler(filters.TEXT, audioupload,block=False)],
            },
        fallbacks=[CommandHandler("cancel", cancel2,block=False)],
    )
    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)
    application.run_polling()

if __name__ == "__main__":
    main()

