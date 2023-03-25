from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from geopy.geocoders import Nominatim
import database
from buttons.inline import get_regions_button_inline, get_districts_button_inline
from buttons.keyboard import get_district_button, get_region_button, phone_button, location_button


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if not database.check_user_in_table(user.id):
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        telegram_id = user.id
        database.insert_user_to_table(first_name, last_name, username, telegram_id)
    user_data = database.get_user_data_with_telegram_id(user.id)
    if not user_data[0][5]:
        update.message.reply_text("Telefon raqamingizni yuborishingiz kerak", reply_markup=phone_button())
        return "phone"
    elif not user_data[0][6] or not user_data[0][7]:
        update.message.reply_text("Yashash joyingizni yuboring", reply_markup=location_button())
        return "location"
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"<b>Assalomu alaykum xush kelibsiz</b> {user.full_name}. Quyidagi viloyatlardan birini tanlang",
        reply_markup=get_regions_button_inline(),
        parse_mode="HTML"
    )

    update.message.reply_html("""<pre language='python'>
    user = update.effective_user
    if not database.check_user_in_table(user.id):
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        telegram_id = user.id
        database.insert_user_to_table(first_name, last_name, username, telegram_id)
        </pre>
    """)
    return "region"


def get_region(update: Update, context: CallbackContext):
    text = update.message.text
    region = database.get_region_by_title(text)

    if region:
        region_id = region[0][0]
        districts = database.districts_by_region_id(int(region_id))
        if districts:
            update.message.reply_text("""Quyidagi tumanlardan birini tanlang """,
                                      reply_markup=ReplyKeyboardMarkup(get_district_button(districts),
                                                                       resize_keyboard=True))
            return "district"
        else:
            update.message.reply_text("""Siz tanlagan viloyatda hali tumanlar mavjud emas""")
            return "region"
    else:
        update.message.reply_text("""Siz ko'rsatilgan viloyatlardan birini tanlang""")
        return "region"


def update_contact_info(update: Update, context: CallbackContext):
    contact = update.message.contact
    database.update_profile_contact(contact.user_id, contact.phone_number)
    update.message.reply_text("Iltimos yashash joyingizni yuboring", reply_markup=location_button())
    return "location"


def get_region_inline(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    data = query.data
    region = database.get_region_by_id(int(data))
    if region:
        context.user_data['region_name'] = region[0][1]
        query.message.edit_text(f"Siz tanlagan viloyat {region[0][1]}\nQuyidagi tumanlardan birini tanlang",
                                reply_markup=get_districts_button_inline(int(region[0][0])))
        return "district"
    else:
        query.answer("Siz tanlagan viloyat topilmadi ko'rsatilgan viloyatlardan birini tanlang🙃")
    return "region"


def get_district(update: Update, context: CallbackContext):
    district_title = update.message.text
    if district_title == "Ortga":
        update.message.reply_text("""Viloyatlardan birini tanlang """,
                                  reply_markup=ReplyKeyboardMarkup(get_region_button()))
        return "region"
    district = database.get_district_by_title(district_title)
    if district:
        district = district[0]
    else:
        update.message.reply_text("""Iltimos faqat ko'rsatilgan tumanlardan birini tanlang""", parse_mode='HTML')
        return "district"
    message = f"""<i>Tuman idsi:</i> <b>{district[0]}</b>
Viloyat idsi: {district[1]}
Tuman nomi: {district[2]}"""
    update.message.reply_html(message)


def get_district_inline(update: Update, context: CallbackContext):
    query = update.callback_query

    data = query.data
    if data == 'back':
        query.message.edit_text(text="Quyidagi viloyatlardan birini tanlang", reply_markup=get_regions_button_inline())
        return "region"
    district = database.get_district_by_id(int(data))
    if district:
        text = f"""<i>Viloyat Nomi:</i> {context.user_data['region_name']}
Tuman nomi: {district[0][2]}
Tuman idsi {district[0][0]}"""
        query.edit_message_text(text=text, reply_markup=get_districts_button_inline(int(district[0][1])), parse_mode="HTML")


def all_message_function(update: Update, context: CallbackContext):
    print(context.bot, update)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='/start bosing'
    )


def command_forward(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Iltimos xabarni forward qilmang")


def get_location(update: Update, context: CallbackContext):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    geolocator = Nominatim(user_agent="botf26")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    message = f"Sizning manzilingiz: {location}\n" \
              f"Manzilingiz muaffaqiyatli qabul qilindi. Botdan foydalanishingiz mumkin"
    update.message.reply_text(message, reply_markup=get_regions_button_inline())
    database.update_profile_location(update.effective_user.id, latitude, longitude)
    return 'region'
