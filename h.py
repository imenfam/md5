from aiogram import Bot, Dispatcher, executor, types
import asyncio

TOKEN = '6432913128:AAG-nbG21jo1GezcJGnJCdoKXTh3BO4QEwk'
admin_id = 5577523506

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer('Привет, админ! Добро пожаловать!')
    else:
        await message.answer(f'Привет,  {message.from_user.first_name} ! Если у вас есть вопрос/жалоба - напишите мне!\nпрежде чем отправлять фото/видео материалы, незабудьте прикрепить к нему текст, администрация будет на много быстрее и эффективнее работать с материалом и приписывайте номенурацию #1, #2, #3, вам будет удобнее понимать, по какой жалобе был дан ответ, спасибо!')


@dp.message_handler()
async def process_message(message: types.Message):
    if message.reply_to_message:
        if message.from_user.id == admin_id:
            user_id = message.reply_to_message.forward_from.id
            reply_text = ''
            if message.text:
                reply_text = message.text
            elif message.photo or message.document or message.video:
                reply_text = 'Ваше медиа отправлено администрации'    
            await bot.send_message(user_id, f'👤 • Ответ администрации: {reply_text}')
            await message.reply('Ваш ответ был отправлен пользователю ☑')
        else:
            await bot.forward_message(admin_id, message.chat.id, message.message_id)
            await message.reply('☑ Ваше обращение было отправлено администрации, ожидайте ответ')
    elif not message.text.startswith('/start'):
        if message.from_user.id == admin_id:
            await message.reply('Вы забыли ответить на сообщение пользователя')
        else:
            await bot.forward_message(admin_id, message.chat.id, message.message_id)
            await message.reply('☑ Ваше обращение было отправлено администрации, ожидайте ответ')



@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo(message: types.Message):
    await bot.forward_message(admin_id, message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, ' ☑ Спасибо, ваше фото передано администрации', reply_to_message_id=message.message_id)

@dp.message_handler(content_types=[types.ContentType.VIDEO])
async def handle_video(message: types.Message):
    await bot.forward_message(admin_id, message.chat.id, message.message_id)
    await message.answer(' ☑ Спасибо, ваше видео передано администрации', reply_to_message_id=message.message_id)

@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def handle_document(message: types.Message):
    await bot.forward_message(admin_id, message.chat.id, message.message_id)
    await message.answer(' ☑ Спасибо, ваш документ передан администрации', reply_to_message_id=message.message_id)


async def on_startup(dp):
    await bot.set_webhook()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()
