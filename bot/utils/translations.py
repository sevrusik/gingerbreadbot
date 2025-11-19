"""
Мультиязычная поддержка для бота
Поддерживаемые языки: русский (ru), английский (en), украинский (uk)
"""

TRANSLATIONS = {
    # Выбор языка
    "choose_language": {
        "ru": "🌍 **Хотите переключить язык?**\n\nНаши пряники понимают и по-русски, по-украински, и по-английски —\nвыберите, как вам уютнее 🍪",
        "en": "🌍 **Want to switch the language?**\n\nOur gingerbreads speak Russian, Ukrainian, and English —\nchoose the one that feels most cozy for you 🍪",
        "uk": "🌍 **Хочете перемкнути мову?**\n\nНаші пряники розуміють і українську, і російську, і англійську —\nоберіть, як вам затишніше 🍪"
    },
    "language_selected": {
        "ru": "✅ Язык изменен на русский",
        "en": "✅ Language changed to English",
        "uk": "✅ Мову змінено на українську"
    },

    # Главное меню
    "welcome": {
        "ru": "🍪 Добро пожаловать в пряничную мастерскую!\n\nЯ помогу вам заказать расписные пряники от мастера {master_name}.\n\n👩‍🍳 Разогреваем печку и готовим место для нового набора!\nВыберите тему, упаковку и добавьте пожелания —\nмы замесим тесто и начнём творить сладкую историю 💛",
        "en": "🍪 Welcome to the gingerbread workshop!\n\nI'll help you order hand-decorated gingerbread cookies from master {master_name}.\n\n👩‍🍳 We're warming up the oven and getting ready for your new set!\nChoose a theme, packaging, and add your wishes —\nwe'll mix the dough and start baking your sweet story 💛",
        "uk": "🍪 Ласкаво просимо до пряникової майстерні!\n\nЯ допоможу вам замовити розписані пряники від майстра {master_name}.\n\n👩‍🍳 Розігріваємо пічку й готуємо місце для нового набору!\nОбирайте тему, упаковку та додайте побажання —\nми замісимо тісто й почнемо творити солодку історію 💛"
    },
    "welcome_with_orders": {
        "ru": "🍪 С возвращением!\n\nМы тут разогрели печку и продолжаем творить твой сладкий заказ 🍪\nАромат имбиря уже витает в воздухе — всё идёт по плану!\n\n👇 Нажми на номер заказа, чтобы посмотреть детали",
        "en": "🍪 Welcome back!\n\nWe've warmed up the oven and continue crafting your sweet order 🍪\nThe scent of ginger is already in the air — everything's going according to plan!\n\n👇 Tap the order number to see details",
        "uk": "🍪 З поверненням!\n\nМи тут розігріли пічку й продовжуємо творити твоє солодке замовлення 🍪\nАромат імбиру вже витає в повітрі — все йде за планом!\n\n👇 Натисни на номер замовлення, щоб переглянути деталі"
    },
    "btn_view_and_order": {
        "ru": "🍪 Посмотреть и заказать",
        "en": "🍪 View and order",
        "uk": "🍪 Переглянути і замовити"
    },
    "btn_contacts": {
        "ru": "💌 Контакты",
        "en": "💌 Contacts",
        "uk": "💌 Контакти"
    },
    "btn_my_orders": {
        "ru": "📦 Мои заказы",
        "en": "📦 My orders",
        "uk": "📦 Мої замовлення"
    },
    "btn_change_language": {
        "ru": "🌍 Язык | Language | Мова",
        "en": "🌍 Язык | Language | Мова",
        "uk": "🌍 Язык | Language | Мова"
    },

    # Выбор типа пряников
    "choose_type": {
        "ru": "🍪 **Выберите тип пряников:**\n\nУ нас есть несколько видов пряников на выбор.",
        "en": "🍪 **Choose the type of gingerbread:**\n\nWe have several types to choose from.",
        "uk": "🍪 **Оберіть тип пряників:**\n\nУ нас є кілька видів пряників на вибір."
    },
    "type_classic": {
        "ru": "Классические расписные",
        "en": "Classic decorated",
        "uk": "Класичні розписні"
    },
    "type_classic_desc": {
        "ru": "Ручная роспись с любовью — классика, которую приятно дарить и получать. Подойдёт к любому празднику.",
        "en": "Hand-painted with love — a timeless classic for any celebration. Perfect as a heartfelt gift.",
        "uk": "Ручний розпис з любов'ю — класика, яку приємно дарувати та отримувати. Підходить до будь-якого свята."
    },
    "type_coloring": {
        "ru": "Пряники-раскраски",
        "en": "Coloring cookies",
        "uk": "Пряники-розмальовки"
    },
    "type_coloring_desc": {
        "ru": "Набор из 3 пряников для раскрашивания + палитра с пищевыми красителями + кисточка. Весело и вкусно для детей и взрослых!",
        "en": "Set of 3 cookies for coloring + palette with edible paints + brush. Fun and tasty for both kids and adults!",
        "uk": "Набір з 3 пряників для розмальовування + палітра з харчовими фарбами + пензлик. Смачно та весело для дітей і дорослих!"
    },
    "type_numbers": {
        "ru": "Цифры",
        "en": "Numbers",
        "uk": "Цифри"
    },
    "type_numbers_desc": {
        "ru": "Пряники в форме цифр — для дня рождения, годовщины или важной даты.",
        "en": "Number-shaped cookies — for birthdays, anniversaries, or any special date.",
        "uk": "Пряники у формі цифр — для дня народження, річниці або важливої дати."
    },
    "type_themed": {
        "ru": "Тематические",
        "en": "Themed",
        "uk": "Тематичні"
    },
    "type_themed_desc": {
        "ru": "Пряники по теме праздника или события — от 8 марта до первого зуба.",
        "en": "Holiday- or event-themed cookies — from Women's Day to baby's first tooth.",
        "uk": "Пряники на тему свята або події — від 8 Березня до першого зубчика."
    },
    "type_urgent": {
        "ru": "Срочный заказ",
        "en": "Urgent order",
        "uk": "Терміново"
    },
    "type_urgent_desc": {
        "ru": "Нужны пряники через 3 дня? Мы поможем. Срочное изготовление с удвоенной стоимостью.",
        "en": "Need cookies in 3 days? We've got you — urgent production at double price.",
        "uk": "Потрібні пряники через 3 дні? Ми допоможемо. Термінове виготовлення з подвоєною вартістю."
    },
    "type_topper": {
        "ru": "Топер для торта",
        "en": "Cake topper",
        "uk": "Топер для торта"
    },
    "type_topper_desc": {
        "ru": "Пряничный топпер в торт — эффектно, съедобно и по-настоящему празднично.",
        "en": "Edible cake topper made of gingerbread — festive, eye-catching, and delicious.",
        "uk": "Пряниковий топер у торт — ефектно, смачно й по-справжньому святково."
    },
    "type_newyear": {
        "ru": "Новогодние пряники",
        "en": "New Year cookies",
        "uk": "Новорічні пряники"
    },
    "type_newyear_desc": {
        "ru": "Праздничные новогодние пряники — ёлочки, человечки, мишки и домики. Создадут волшебную атмосферу праздника!",
        "en": "Festive New Year cookies — trees, gingerbread men, bears, and houses. Create the magic of the holidays!",
        "uk": "Святкові новорічні пряники — ялинки, чоловічки, ведмедики та будиночки. Створять чарівну атмосферу свята!"
    },
    "choose_newyear_subtype": {
        "ru": "🎄 **Выберите тип новогодних пряников:**\n\nУ нас есть два варианта на выбор.",
        "en": "🎄 **Choose New Year cookie type:**\n\nWe have two options to choose from.",
        "uk": "🎄 **Оберіть тип новорічних пряників:**\n\nУ нас є два варіанти на вибір."
    },
    "newyear_subtype_selected": {
        "ru": "Выбран тип: **{subtype}** ({price} €) ✨",
        "en": "Type selected: **{subtype}** ({price} €) ✨",
        "uk": "Обрано тип: **{subtype}** ({price} €) ✨"
    },
    "enter_quantity_newyear": {
        "ru": "📦 **Сколько пряников вам нужно?**\n\nУкажите общее количество (от 1 до 100 штук)",
        "en": "📦 **How many cookies do you need?**\n\nEnter total quantity (from 1 to 100 pieces)",
        "uk": "📦 **Скільки пряників вам потрібно?**\n\nВкажіть загальну кількість (від 1 до 100 штук)"
    },
    "enter_newyear_comment": {
        "ru": "💬 **Укажите состав заказа**\n\nОпишите, какие пряники и в каком количестве вам нужны.\n\n**Примеры:**\n• Елка — 2 шт, Человечек — 2 шт\n• Домик (красный) — 4 шт, Мишка — 2 шт\n• Домик (коричневый) — 3 шт",
        "en": "💬 **Specify order composition**\n\nDescribe which cookies and how many you need.\n\n**Examples:**\n• Tree — 2 pcs, Gingerbread man — 2 pcs\n• House (red) — 4 pcs, Bear — 2 pcs\n• House (brown) — 3 pcs",
        "uk": "💬 **Вкажіть склад замовлення**\n\nОпишіть, які пряники і в якій кількості вам потрібні.\n\n**Приклади:**\n• Ялинка — 2 шт, Чоловічок — 2 шт\n• Будиночок (червоний) — 4 шт, Ведмедик — 2 шт\n• Будиночок (коричневий) — 3 шт"
    },
    "choose_coloring_subtype": {
        "ru": "🎨 **Выберите набор пряников-раскрасок:**\n\nУ нас есть три варианта на выбор.",
        "en": "🎨 **Choose coloring cookie set:**\n\nWe have three options to choose from.",
        "uk": "🎨 **Оберіть набір пряників-розмальовок:**\n\nУ нас є три варіанти на вибір."
    },
    "subtype_selected": {
        "ru": "Выбран набор: **{subtype}** ({price} €) ✨",
        "en": "Set selected: **{subtype}** ({price} €) ✨",
        "uk": "Обрано набір: **{subtype}** ({price} €) ✨"
    },
    "enter_quantity_coloring_subtype": {
        "ru": "📦 **Сколько наборов вам нужно?**\n\nУкажите количество наборов (от 1 до 100)",
        "en": "📦 **How many sets do you need?**\n\nEnter number of sets (from 1 to 100)",
        "uk": "📦 **Скільки наборів вам потрібно?**\n\nВкажіть кількість наборів (від 1 до 100)"
    },

    # Тема
    "choose_theme": {
        "ru": "🎨 **Выберите тему или введите свою:**\n\nМожете выбрать одну из популярных тем или описать свою идею.",
        "en": "🎨 **Choose a theme or enter your own:**\n\nYou can choose from popular themes or describe your own idea.",
        "uk": "🎨 **Оберіть тему або введіть свою:**\n\nМожете обрати одну з популярних тем або описати свою ідею."
    },
    "custom_theme": {
        "ru": "✏️ Опишите, какую тему вы хотите.\n\nНапример: \"Единороги и радуга\" или \"Космос и звезды\"",
        "en": "✏️ Describe the theme you want.\n\nFor example: \"Unicorns and rainbow\" or \"Space and stars\"",
        "uk": "✏️ Опишіть, яку тему ви хочете.\n\nНаприклад: \"Єдинороги та веселка\" або \"Космос і зірки\""
    },
    "btn_custom_theme": {
        "ru": "✏️ Своя тема",
        "en": "✏️ Custom theme",
        "uk": "✏️ Своя тема"
    },

    # Количество
    "enter_quantity": {
        "ru": "📦 **Сколько пряников вам нужно?**\n\nМинимальный заказ: 10 штук\nУкажите количество (от 10 до 100 штук)",
        "en": "📦 **How many cookies do you need?**\n\nMinimum order: 10 pieces\nEnter quantity (from 10 to 100 pieces)",
        "uk": "📦 **Скільки пряників вам потрібно?**\n\nМінімальне замовлення: 10 штук\nВкажіть кількість (від 10 до 100 штук)"
    },
    "enter_quantity_coloring": {
        "ru": "📦 **Сколько наборов вам нужно?**\n\n🎨 Один набор включает:\n• 3 пряника для раскрашивания\n• Палитра с пищевыми красителями\n• Кисточка\n\nУкажите количество наборов (от 1 до 100)",
        "en": "📦 **How many sets do you need?**\n\n🎨 One set includes:\n• 3 cookies for coloring\n• Palette with edible paints\n• Brush\n\nEnter number of sets (from 1 to 100)",
        "uk": "📦 **Скільки наборів вам потрібно?**\n\n🎨 Один набір включає:\n• 3 пряники для розмальовування\n• Палітра з харчовими фарбами\n• Пензлик\n\nВкажіть кількість наборів (від 1 до 100)"
    },
    "enter_quantity_topper": {
        "ru": "📦 **Сколько топперов вам нужно?**\n\n🎂 Большой пряник 10×15 см\n\nУкажите количество (от 1 до 100 штук)",
        "en": "📦 **How many toppers do you need?**\n\n🎂 Large cookie 10×15 cm\n\nEnter quantity (from 1 to 100 pieces)",
        "uk": "📦 **Скільки топерів вам потрібно?**\n\n🎂 Великий пряник 10×15 см\n\nВкажіть кількість (від 1 до 100 штук)"
    },
    "invalid_quantity": {
        "ru": "❌ Неверное количество.\n\nПожалуйста, укажите число.",
        "en": "❌ Invalid quantity.\n\nPlease enter a number.",
        "uk": "❌ Невірна кількість.\n\nБудь ласка, вкажіть число."
    },
    "invalid_quantity_min": {
        "ru": "❌ Минимальное количество: {min} штук.\n\nЭто необходимо для рентабельности производства.\nПожалуйста, укажите от {min} до {max} штук.",
        "en": "❌ Minimum quantity: {min} pieces.\n\nThis is required for cost-effective production.\nPlease enter from {min} to {max} pieces.",
        "uk": "❌ Мінімальна кількість: {min} штук.\n\nЦе необхідно для рентабельності виробництва.\nБудь ласка, вкажіть від {min} до {max} штук."
    },
    "invalid_quantity_coloring": {
        "ru": "❌ Укажите количество наборов.\n\n📦 Один набор = 3 пряника + краски + кисточка\n\nПожалуйста, укажите от {min} до {max} наборов.",
        "en": "❌ Enter the number of sets.\n\n📦 One set = 3 cookies + paints + brush\n\nPlease enter from {min} to {max} sets.",
        "uk": "❌ Вкажіть кількість наборів.\n\n📦 Один набір = 3 пряники + фарби + пензлик\n\nБудь ласка, вкажіть від {min} до {max} наборів."
    },
    "invalid_quantity_range": {
        "ru": "❌ Неверное количество.\n\nПожалуйста, укажите от {min} до {max} штук.",
        "en": "❌ Invalid quantity.\n\nPlease enter from {min} to {max} pieces.",
        "uk": "❌ Невірна кількість.\n\nБудь ласка, вкажіть від {min} до {max} штук."
    },

    # Дата
    "enter_date": {
        "ru": "📅 **На какую дату нужны пряники?**\n\nУкажите дату в формате: дд.мм.гггг\nНапример: 25.12.2024\n\n⏰ Минимальный срок изготовления: {min_days} дней",
        "en": "📅 **What date do you need the cookies?**\n\nEnter date in format: dd.mm.yyyy\nFor example: 25.12.2024\n\n⏰ Minimum preparation time: {min_days} days",
        "uk": "📅 **На яку дату потрібні пряники?**\n\nВкажіть дату у форматі: дд.мм.рррр\nНаприклад: 25.12.2024\n\n⏰ Мінімальний термін виготовлення: {min_days} днів"
    },
    "invalid_date": {
        "ru": "❌ Неверный формат даты.\n\nПожалуйста, используйте формат: дд.мм.гггг\nНапример: 25.12.2024",
        "en": "❌ Invalid date format.\n\nPlease use format: dd.mm.yyyy\nFor example: 25.12.2024",
        "uk": "❌ Невірний формат дати.\n\nБудь ласка, використовуйте формат: дд.мм.рррр\nНаприклад: 25.12.2024"
    },
    "date_too_early": {
        "ru": "❌ Слишком ранняя дата.\n\nМинимальный срок изготовления: {min_days} дней.\nПожалуйста, выберите дату не раньше {min_date}",
        "en": "❌ Date too early.\n\nMinimum preparation time: {min_days} days.\nPlease choose a date not earlier than {min_date}",
        "uk": "❌ Занадто рання дата.\n\nМінімальний термін виготовлення: {min_days} днів.\nБудь ласка, оберіть дату не раніше {min_date}"
    },
    "date_not_available": {
        "ru": "❌ К сожалению, на эту дату все слоты заняты.\n\nПожалуйста, выберите другую дату.",
        "en": "❌ Unfortunately, all slots for this date are taken.\n\nPlease choose another date.",
        "uk": "❌ На жаль, на цю дату всі слоти зайняті.\n\nБудь ласка, оберіть іншу дату."
    },

    # Повод
    "enter_occasion": {
        "ru": "💬 **Комментарии к заказу**\n\nНапишите дополнительные пожелания или уточнения.\nНапример: цвет глазури, особые пожелания к дизайну и т.д.",
        "en": "💬 **Order comments**\n\nWrite additional wishes or clarifications.\nFor example: icing color, special design requests, etc.",
        "uk": "💬 **Коментарі до замовлення**\n\nНапишіть додаткові побажання або уточнення.\nНаприклад: колір глазурі, особливі побажання до дизайну тощо."
    },
    "enter_themed_description": {
        "ru": "🎨 **Опишите, какие тематические пряники вам нужны**\n\nНапишите тему или повод для заказа. Мастер уточнит детали при необходимости.\n\nНапример:\n• Свадьба в морском стиле\n• День рождения с единорогами\n• 8 марта с цветами\n• Первый зубик малыша",
        "en": "🎨 **Describe the themed cookies you need**\n\nWrite the theme or occasion for your order. The master will clarify details if needed.\n\nFor example:\n• Beach-themed wedding\n• Birthday with unicorns\n• Women's Day with flowers\n• Baby's first tooth",
        "uk": "🎨 **Опишіть, які тематичні пряники вам потрібні**\n\nНапишіть тему або привід для замовлення. Майстер уточнить деталі за потреби.\n\nНаприклад:\n• Весілля в морському стилі\n• День народження з єдинорогами\n• 8 Березня з квітами\n• Перший зубчик малюка"
    },

    # Телефон
    "enter_phone": {
        "ru": "📱 **Укажите ваш номер телефона**\n\nМожете нажать кнопку \"Отправить номер\" или ввести вручную.\n\nПримеры форматов:\n• +357 95 111 4444\n• 95111444",
        "en": "📱 **Enter your phone number**\n\nYou can press \"Send number\" button or enter manually.\n\nExample formats:\n• +357 95 111 4444\n• 95111444",
        "uk": "📱 **Вкажіть ваш номер телефону**\n\nМожете натиснути кнопку \"Надіслати номер\" або ввести вручну.\n\nПриклади форматів:\n• +357 95 111 4444\n• 95111444"
    },
    "invalid_phone": {
        "ru": "❌ Неверный формат номера.\n\nПожалуйста, введите корректный номер телефона.",
        "en": "❌ Invalid phone format.\n\nPlease enter a valid phone number.",
        "uk": "❌ Невірний формат номера.\n\nБудь ласка, введіть коректний номер телефону."
    },
    "btn_send_phone": {
        "ru": "📱 Отправить номер",
        "en": "📱 Send number",
        "uk": "📱 Надіслати номер"
    },

    # Подтверждение заказа
    "order_confirmation": {
        "ru": "📋 **Проверьте данные заказа:**\n\n🍪 Тип: {type}\n{theme}📦 Количество: {quantity} шт\n📅 Дата: {date}\n💬 Комментарии: {occasion}\n📱 Телефон: {phone}\n\n💰 **Сумма: {total}€**\n\nВсе верно?",
        "en": "📋 **Check order details:**\n\n🍪 Type: {type}\n{theme}📦 Quantity: {quantity} pcs\n📅 Date: {date}\n💬 Comments: {occasion}\n📱 Phone: {phone}\n\n💰 **Total: {total}€**\n\nIs everything correct?",
        "uk": "📋 **Перевірте дані замовлення:**\n\n🍪 Тип: {type}\n{theme}📦 Кількість: {quantity} шт\n📅 Дата: {date}\n💬 Коментарі: {occasion}\n📱 Телефон: {phone}\n\n💰 **Сума: {total}€**\n\nВсе вірно?"
    },
    "btn_confirm": {
        "ru": "✅ Подтвердить",
        "en": "✅ Confirm",
        "uk": "✅ Підтвердити"
    },
    "btn_cancel": {
        "ru": "❌ Отменить",
        "en": "❌ Cancel",
        "uk": "❌ Скасувати"
    },

    # После подтверждения
    "order_accepted": {
        "ru": "✅ **Заказ #{order_number} принят!**\n\nСпасибо за ваш заказ!\n\n⏳ Заказ передан мастеру на рассмотрение.\n📱 Вы получите уведомление, как только мастер подтвердит заказ.\n\n📅 Планируемая дата: {date}\n💰 Сумма: {total}€\n\n📞 Если у вас есть вопросы, свяжитесь с нами через раздел \"Контакты\".",
        "en": "✅ **Order #{order_number} accepted!**\n\nThank you for your order!\n\n⏳ Order sent to master for review.\n📱 You'll receive a notification once the master confirms the order.\n\n📅 Planned date: {date}\n💰 Total: {total}€\n\n📞 If you have questions, contact us through \"Contacts\" section.",
        "uk": "✅ **Замовлення #{order_number} прийнято!**\n\nДякуємо за ваше замовлення!\n\n⏳ Замовлення передано майстру на розгляд.\n📱 Ви отримаєте сповіщення, як тільки майстер підтвердить замовлення.\n\n📅 Планована дата: {date}\n💰 Сума: {total}€\n\n📞 Якщо у вас є питання, зв'яжіться з нами через розділ \"Контакти\"."
    },
    "order_cancelled": {
        "ru": "Заказ отменен. Возвращайтесь когда будете готовы! 😊",
        "en": "Order cancelled. Come back when you're ready! 😊",
        "uk": "Замовлення скасовано. Повертайтесь, коли будете готові! 😊"
    },

    # Контакты
    "contacts": {
        "ru": "💌 **Хотите написать мастеру напрямую?**\n\nМы всегда рядом — в Telegram, Instagram или по телефону.\nРасскажите, что задумали, и мы подскажем, какой набор подойдёт именно вам 🍀\n\n👤 Мастер: {master_name}\n📱 Телефон: {phone}\n📍 Адрес: {address}\n⏰ Время работы: {hours}",
        "en": "💌 **Want to message the baker directly?**\n\nWe're always nearby — on Telegram, Instagram, or by phone.\nTell us your idea, and we'll help you choose the perfect set 🍀\n\n👤 Master: {master_name}\n📱 Phone: {phone}\n📍 Address: {address}\n⏰ Working hours: {hours}",
        "uk": "💌 **Хочете написати майстру напряму?**\n\nМи завжди поруч — у Telegram, Instagram чи телефоном.\nРозкажіть, що задумали, і ми підкажемо, який набір підійде саме вам 🍀\n\n👤 Майстер: {master_name}\n📱 Телефон: {phone}\n📍 Адреса: {address}\n⏰ Години роботи: {hours}"
    },

    # Каталог
    "catalog": {
        "ru": "📖 **Вот наш ароматный каталог**\n\nКаждый набор со своей историей.\n\n⚠️ Аккуратно: корица и мёд могут вызвать лёгкое головокружение 😋\n\n{catalog_items}\n\n💡 Выберите тип в меню заказа!",
        "en": "📖 **Here's our aromatic catalog**\n\nEvery set has its own story.\n\n⚠️ Careful: cinnamon and honey may cause mild happiness overload 😋\n\n{catalog_items}\n\n💡 Choose type in order menu!",
        "uk": "📖 **Ось наш запашний каталог**\n\nКожен набір має власну історію.\n\n⚠️ Обережно: кориця й мед можуть викликати легке запаморочення 😋\n\n{catalog_items}\n\n💡 Оберіть тип у меню замовлення!"
    },

    # Мои заказы
    "my_orders_empty": {
        "ru": "У вас пока нет активных заказов.\n\nХотите сделать первый заказ? 🍪",
        "en": "You don't have any active orders yet.\n\nWould you like to make your first order? 🍪",
        "uk": "У вас поки немає активних замовлень.\n\nХочете зробити перше замовлення? 🍪"
    },
    "my_orders": {
        "ru": "📦 **Ваши активные заказы:**\n\n{orders}",
        "en": "📦 **Your active orders:**\n\n{orders}",
        "uk": "📦 **Ваші активні замовлення:**\n\n{orders}"
    },
    "my_orders_header": {
        "ru": "📦 **Ваши активные заказы:**",
        "en": "📦 **Your active orders:**",
        "uk": "📦 **Ваші активні замовлення:**"
    },

    # Детали заказа
    "order_details": {
        "ru": "📋 **Заказ #{order_number}**\n\n"
              "📊 Статус: {status}\n"
              "🍪 Тип: {type}\n"
              "{theme}"
              "{notes}"
              "{occasion_text}"
              "📦 Количество: {quantity} шт\n"
              "📅 Дата доставки: {date}\n"
              "📱 Телефон: {phone}\n\n"
              "💰 **Сумма: {total}€**\n\n"
              "🕐 Создан: {created}",
        "en": "📋 **Order #{order_number}**\n\n"
              "📊 Status: {status}\n"
              "🍪 Type: {type}\n"
              "{theme}"
              "{notes}"
              "{occasion_text}"
              "📦 Quantity: {quantity} pcs\n"
              "📅 Delivery date: {date}\n"
              "📱 Phone: {phone}\n\n"
              "💰 **Total: {total}€**\n\n"
              "🕐 Created: {created}",
        "uk": "📋 **Замовлення #{order_number}**\n\n"
              "📊 Статус: {status}\n"
              "🍪 Тип: {type}\n"
              "{theme}"
              "{notes}"
              "{occasion_text}"
              "📦 Кількість: {quantity} шт\n"
              "📅 Дата доставки: {date}\n"
              "📱 Телефон: {phone}\n\n"
              "💰 **Сума: {total}€**\n\n"
              "🕐 Створено: {created}"
    },
    "order_not_found": {
        "ru": "❌ Заказ не найден",
        "en": "❌ Order not found",
        "uk": "❌ Замовлення не знайдено"
    },
    "example_not_found": {
        "ru": "❌ Пример не найден",
        "en": "❌ Example not found",
        "uk": "❌ Приклад не знайдено"
    },
    "theme_label": {
        "ru": "Тема",
        "en": "Theme",
        "uk": "Тема"
    },
    "no_occasion": {
        "ru": "Не указан",
        "en": "Not specified",
        "uk": "Не вказано"
    },

    # Статусы заказов
    "status_new": {
        "ru": "🟡 Новый",
        "en": "🟡 New",
        "uk": "🟡 Новий"
    },
    "status_confirmed": {
        "ru": "🟢 Подтвержден",
        "en": "🟢 Confirmed",
        "uk": "🟢 Підтверджено"
    },
    "status_in_progress": {
        "ru": "🔵 В работе",
        "en": "🔵 In progress",
        "uk": "🔵 У роботі"
    },
    "status_ready": {
        "ru": "🟣 Готов",
        "en": "🟣 Ready",
        "uk": "🟣 Готовий"
    },
    "status_completed": {
        "ru": "✅ Выполнен",
        "en": "✅ Completed",
        "uk": "✅ Виконано"
    },
    "status_cancelled": {
        "ru": "❌ Отменен",
        "en": "❌ Cancelled",
        "uk": "❌ Скасовано"
    },

    # Кнопки навигации
    "btn_back": {
        "ru": "⬅️ Назад",
        "en": "⬅️ Back",
        "uk": "⬅️ Назад"
    },
    "btn_back_to_selection": {
        "ru": "◀️ Назад к выбору",
        "en": "◀️ Back to selection",
        "uk": "◀️ Назад до вибору"
    },
    "btn_order_this": {
        "ru": "✅ Заказать",
        "en": "✅ Order",
        "uk": "✅ Замовити"
    },
    "btn_main_menu": {
        "ru": "🏠 Главное меню",
        "en": "🏠 Main menu",
        "uk": "🏠 Головне меню"
    },

    # Админ панель
    "btn_admin_orders": {
        "ru": "📋 Активные заказы",
        "en": "📋 Active orders",
        "uk": "📋 Активні замовлення"
    },
    "btn_admin_calendar": {
        "ru": "📅 Календарь",
        "en": "📅 Calendar",
        "uk": "📅 Календар"
    },
    "btn_admin_stats": {
        "ru": "📊 Статистика",
        "en": "📊 Statistics",
        "uk": "📊 Статистика"
    },
    "btn_admin_broadcast": {
        "ru": "📢 Рассылка",
        "en": "📢 Broadcast",
        "uk": "📢 Розсилка"
    },
    "theme_recorded": {
        "ru": "Тема записана: **{theme}** ✨\n\n",
        "en": "Theme recorded: **{theme}** ✨\n\n",
        "uk": "Тему записано: **{theme}** ✨\n\n"
    },
    "urgent_order_info": {
        "ru": "🚨 **Срочный заказ**\n\n⚠️ Стоимость: **двойная** от базовой цены\n⏰ Минимальный срок подготовки: всего 3 дня (вместо обычных 10)\n\nОпишите, какие пряники вам нужны:",
        "en": "🚨 **Urgent order**\n\n⚠️ Price: **double** the base price\n⏰ Minimum preparation time: only 3 days (instead of usual 10)\n\nDescribe what cookies you need:",
        "uk": "🚨 **Терміново**\n\n⚠️ Вартість: **подвійна** від базової ціни\n⏰ Мінімальний термін підготовки: лише 3 дні (замість звичайних 10)\n\nОпишіть, які пряники вам потрібні:"
    },
    "urgent_enter_date": {
        "ru": "📅 **На какую дату нужны пряники?**\n\n🚨 Срочный заказ - минимальный срок {min_days} дня!\n\nУкажите дату в формате: дд.мм.гггг\nНапример: 10.10.2024",
        "en": "📅 **What date do you need the cookies?**\n\n🚨 Urgent order - minimum {min_days} days!\n\nEnter the date in format: dd.mm.yyyy\nFor example: 10.10.2024",
        "uk": "📅 **На яку дату потрібні пряники?**\n\n🚨 Термінове замовлення - мінімальний термін {min_days} дні!\n\nВкажіть дату у форматі: дд.мм.рррр\nНаприклад: 10.10.2024"
    },
    "date_in_past": {
        "ru": "❌ Дата не может быть в прошлом. Укажите сегодняшнюю дату или позже.",
        "en": "❌ Date cannot be in the past. Enter today's date or later.",
        "uk": "❌ Дата не може бути в минулому. Вкажіть сьогоднішню дату або пізніше."
    },
    "check_order_above": {
        "ru": "⬆️ Проверьте данные заказа выше",
        "en": "⬆️ Check the order details above",
        "uk": "⬆️ Перевірте дані замовлення вище"
    },
    "order_accepted": {
        "ru": "✅ **Заказ #{order_number} принят!**\n\nСпасибо за ваш заказ!\n\n⏳ Заказ передан мастеру на рассмотрение.\n📱 Вы получите уведомление, как только мастер подтвердит заказ.\n\n📅 Планируемая дата: {date}\n💰 Сумма: {total}€\n\n📞 Если у вас есть вопросы, свяжитесь с нами через раздел \"Контакты\".",
        "en": "✅ **Order #{order_number} accepted!**\n\nThank you for your order!\n\n⏳ Order has been sent to the master for review.\n📱 You will receive a notification once the master confirms the order.\n\n📅 Planned date: {date}\n💰 Total: {total}€\n\n📞 If you have any questions, contact us through the \"Contacts\" section.",
        "uk": "✅ **Замовлення #{order_number} прийнято!**\n\nДякуємо за ваше замовлення!\n\n⏳ Замовлення передано майстру на розгляд.\n📱 Ви отримаєте сповіщення, як тільки майстер підтвердить замовлення.\n\n📅 Планована дата: {date}\n💰 Сума: {total}€\n\n📞 Якщо у вас є питання, зв'яжіться з нами через розділ \"Контакти\"."
    },
    "order_confirmed_by_master": {
        "ru": "✅ **Заказ #{order_number} подтверждён!**\n\n🎉 Ваш заказ подтвержден мастером!\n\n📅 Дата получения: {date}\n💰 Сумма: {total}€\n\n📞 Ждем вас по адресу, указанному в разделе \"Контакты\".",
        "en": "✅ **Order #{order_number} confirmed!**\n\n🎉 Your order has been confirmed by the master!\n\n📅 Pickup date: {date}\n💰 Total: {total}€\n\n📞 We are waiting for you at the address specified in the \"Contacts\" section.",
        "uk": "✅ **Замовлення #{order_number} підтверджено!**\n\n🎉 Ваше замовлення підтверджено майстром!\n\n📅 Дата отримання: {date}\n💰 Сума: {total}€\n\n📞 Чекаємо на вас за адресою, вказаною в розділі \"Контакти\"."
    },
    "price_from": {
        "ru": "от",
        "en": "from",
        "uk": "від"
    },
}


def get_text(key: str, lang: str = "ru", **kwargs) -> str:
    """
    Получить текст на выбранном языке

    Args:
        key: Ключ текста
        lang: Код языка (ru, en, uk)
        **kwargs: Параметры для форматирования

    Returns:
        Отформатированный текст на выбранном языке
    """
    if key not in TRANSLATIONS:
        return key

    if lang not in TRANSLATIONS[key]:
        lang = "ru"  # Fallback на русский

    text = TRANSLATIONS[key][lang]

    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text
