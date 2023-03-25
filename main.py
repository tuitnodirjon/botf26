from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, \
    ConversationHandler
from functions import start, get_region, get_region_inline, get_district, get_district_inline, update_contact_info, \
    get_location


def main() -> None:
    updater = Updater("6034803951:AAEb4XeEm-Jb0DdNIZqnWEc-I4p0ZeIRRXs")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("start", start),
            ],
            states={
                "region": [
                    # MessageHandler(Filters.text, get_region),
                    CallbackQueryHandler(get_region_inline)

                ],
                "district": [
                    MessageHandler(Filters.text, get_district),
                    CallbackQueryHandler(get_district_inline)
                ],
                "phone": [
                    MessageHandler(Filters.contact, update_contact_info)
                ],
                "location": [
                    MessageHandler(Filters.location, get_location)
                ]

            },
            fallbacks=[
                CommandHandler("start", start)
            ]

        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
