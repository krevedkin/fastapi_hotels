INSERT INTO hotels (
  name,
  location,
  services,
  rooms_quantity,
  image_url,
  stars,
  description,
  city,
  address
) VALUES
('Отель "Райский уголок"', 'Москва', '["Спа", "Бассейн", "Ресторан"]', 50, 'http://localhost:8000/static/images/hotels/1.webp', 4, 'Роскошный отель с первоклассными удобствами', 'Москва', 'ул. Тверская, д. 123'),
('Отель "Вид на закат"', 'Санкт-Петербург', '["Бар", "Тренажерный зал", "Обслуживание в номерах"]', 30, 'http://localhost:8000/static/images/hotels/2.webp', 3, 'Наслаждайтесь прекрасными закатами из вашего номера', 'Санкт-Петербург', 'Невский проспект, д. 456'),
('Курорт "Природный уголок"', 'Сочи', '["Доступ к пляжу", "Теннисный корт", "Детский клуб"]', 80, 'http://localhost:8000/static/images/hotels/3.webp', 5, 'Погрузитесь в природную красоту в нашем курорте', 'Сочи', 'Роза Хутор, д. 789'),
('Пансионат "Горный вид"', 'Красная Поляна', '["Горные лыжи", "Сауна", "WiFi"]', 40, 'http://localhost:8000/static/images/hotels/4.webp', 4, 'Захватывающий вид на горы и уютные коттеджи', 'Красная Поляна', 'Горная улица, д. 12'),
('Гостиница "У реки"', 'Казань', '["Бесплатный завтрак", "Прокат велосипедов", "Вид на реку"]', 25, 'http://localhost:8000/static/images/hotels/5.webp', 3, 'Отдыхайте у реки в нашем комфортабельном отеле', 'Казань', 'Набережная, д. 56'),
('Отель "В центре города"', 'Екатеринбург', '["Фитнес-центр", "Бизнес-центр", "Круглосуточная стойка регистрации"]', 60, 'http://localhost:8000/static/images/hotels/6.webp', 4, 'Удобное расположение в центре города', 'Екатеринбург', 'пр. Ленина, д. 789'),
('Гостиница "Прибрежный бриз"', 'Владивосток', '["Вид на море", "Бар у бассейна", "Просторные номера"]', 70, 'http://localhost:8000/static/images/hotels/7.webp', 4, 'Захватывающие виды и свежий морской бриз', 'Владивосток', 'Приморская набережная, д. 101'),
('Курорт "Золотые пески"', 'Анапа', '["Частный пляж", "Водные виды спорта", "Шоу-программы"]', 100, 'http://localhost:8000/static/images/hotels/8.webp', 5, 'Отдыхайте на золотистых пляжах и в чистых водах', 'Анапа', 'Побережье Черного моря, д. 222'),
('Исторический особняк', 'Великий Новгород', '["Экскурсии по историческим местам", "Сад", "Ресторан высокой кухни"]', 15, 'http://localhost:8000/static/images/hotels/9.webp', 3, 'Окунитесь в атмосферу старинных времен', 'Великий Новгород', 'ул. Старая, д. 45'),
('Гостиница "Величественный замок"', 'Псков', '["Замковые экскурсии", "Каминный зал", "Библиотека"]', 20, 'http://localhost:8000/static/images/hotels/10.webp', 5, 'Живите, как короли, в нашем величественном замке', 'Псков', 'Замковый холм, д. 1'),
('Озерный курорт', 'Красноярск', '["Спортзал", "Бильярд", "Детская площадка"]', 70, 'http://localhost:8000/static/images/hotels/11.webp', 4, 'Расслабление у озера с разнообразными активностями', 'Красноярск', 'ул. Озерная, д. 22'),
('Горнолыжный отель', 'Гудаури', '["Прокат лыж", "Бассейн", "Сауна"]', 40, 'http://localhost:8000/static/images/hotels/12.webp', 4, 'Отдых на горнолыжных склонах и комфортные условия', 'Гудаури', 'ул. Горнолыжная, д. 33'),
('Комфортный спа-отель', 'Сочи', '["СПА-центр", "Фитнес", "Бар на крыше"]', 100, 'http://localhost:8000/static/images/hotels/13.webp', 5, 'Спокойствие и релаксация в нашем спа-отеле', 'Сочи', 'ул. Спортивная, д. 44'),
('Отель "Премьер-Люкс"', 'Москва', '["VIP-сервис", "Конференц-зал", "Казино"]', 200, 'http://localhost:8000/static/images/hotels/14.webp', 5, 'Высший класс обслуживания для искушенных гостей', 'Москва', 'Красная площадь, д. 1'),
('Загородный домик', 'Псковская область', '["Баня", "Барбекю", "Рыбалка"]', 10, 'http://localhost:8000/static/images/hotels/15.webp', 3, 'Отдых на природе в уютном загородном доме', 'Псковская область', 'д. Загородное, д. 5'),
('Атмосферный бутик-отель', 'Санкт-Петербург', '["Бутик-магазин", "Кафе", "Терраса"]', 25, 'http://localhost:8000/static/images/hotels/16.webp', 4, 'Уникальное оформление и уютная атмосфера', 'Санкт-Петербург', 'ул. Бутиковая, д. 6'),
('Семейный отдых на море', 'Судак', '["Детский клуб", "Бассейн", "Анимационная программа"]', 80, 'http://localhost:8000/static/images/hotels/17.webp', 4, 'Отличный выбор для семейного отдыха на побережье', 'Судак', 'пгт. Новый Свет, д. 7'),
('Курорт "Зеленый берег"', 'Анапа', '["Спортивные площадки", "Аквапарк", "Широкий песчаный пляж"]', 150, 'http://localhost:8000/static/images/hotels/18.webp', 5, 'Наши берега предлагают много возможностей для активного отдыха', 'Анапа', 'пгт. Витязево, д. 8'),
('Отель "Волшебный лес"', 'Карелия', '["Экскурсии по лесу", "Каминный зал", "Финская сауна"]', 30, 'http://localhost:8000/static/images/hotels/19.webp', 3, 'Погрузитесь в волшебство леса вместе с нами', 'Карелия', 'пос. Чудское, д. 9'),
('Романтический уют', 'Ярославль', '["Камин", "Ресторан романтической кухни", "Спа-процедуры"]', 20, 'http://localhost:8000/static/images/hotels/20.webp', 4, 'Идеальное место для романтического отдыха', 'Ярославль', 'ул. Романтическая, д. 10'),
('Отель "Под звездами"', 'Сочи', '["Бассейн на крыше", "Ресторан с видом на море", "СПА-салон"]', 120, 'http://localhost:8000/static/images/hotels/21.webp', 5, 'Идеальное место для романтического отдыха под звездами', 'Сочи', 'ул. Звездная, д. 11'),
('Гостевой дом "Зеленая поляна"', 'Екатеринбург', '["Сауна", "Бильярд", "Теннисный корт"]', 12, 'http://localhost:8000/static/images/hotels/22.webp', 3, 'Уютный дом с красивыми зелеными полянами', 'Екатеринбург', 'ул. Полянская, д. 12'),
('Оздоровительный курорт "Здоровый берег"', 'Крым', '["СПА-центр", "Лечебные процедуры", "Бассейны с морской водой"]', 200, 'http://localhost:8000/static/images/hotels/23.webp', 5, 'Отдых и оздоровление на берегу Черного моря', 'Крым', 'пгт. Здоровый, д. 13'),
('Отель "Горный воздух"', 'Сочи', '["Лыжные трассы", "Парковая зона", "Кафе с видом на горы"]', 70, 'http://localhost:8000/static/images/hotels/24.webp', 4, 'Погрузитесь в горный воздух и красоты окружающей природы', 'Сочи', 'ул. Горная, д. 14'),
('Пансионат "Тихий залив"', 'Севастополь', '["Частный пляж", "Водные виды спорта", "Ресторан морской кухни"]', 40, 'http://localhost:8000/static/images/hotels/25.webp', 4, 'Отдыхайте в тишине и уединении на берегу моря', 'Севастополь', 'ул. Заливная, д. 15'),
('Усадьба "Золотая роща"', 'Тверская область', '["Пешеходные маршруты", "Русская баня", "Рыбная ловля"]', 18, 'http://localhost:8000/static/images/hotels/26.webp', 3, 'Отдыхайте среди золотистой осенней рощи', 'Тверская область', 'д. Золотая, д. 16'),
('Отель "Рай в горах"', 'Сочи', '["Вид на горы", "Лыжные трассы", "Ресторан с национальной кухней"]', 60, 'http://localhost:8000/static/images/hotels/27.webp', 4, 'Идеальное место для любителей активного отдыха в горах', 'Сочи', 'ул. Райская, д. 17'),
('Гостиница "Морской бриз"', 'Анапа', '["Бассейн с морской водой", "Пляжные вечера", "Детская анимация"]', 80, 'http://localhost:8000/static/images/hotels/28.webp', 4, 'Погрузитесь в атмосферу морского бриза и летних вечеров', 'Анапа', 'ул. Бризовая, д. 18'),
('Отель "Лунное озеро"', 'Байкал', '["Пляж", "Экскурсии по озеру", "Барбекю на природе"]', 25, 'http://localhost:8000/static/images/hotels/29.webp', 3, 'Отдыхайте на берегу Байкала под лунным светом', 'Байкал', 'оз. Лунное, д. 19'),
('Курорт "Солнечный рай"', 'Сочи', '["Бассейны", "Песчаный пляж", "Кафе с живой музыкой"]', 100, 'http://localhost:8000/static/images/hotels/30.webp', 5, 'Расслабление и развлечения в солнечном райском уголке', 'Сочи', 'ул. Солнечная, д. 20'),
('Отель "Панорамный вид"', 'Санкт-Петербург', '["Терраса с видом на город", "СПА-центр", "Бильярд"]', 50, 'http://localhost:8000/static/images/hotels/31.webp', 4, 'Насладитесь потрясающим панорамным видом на Санкт-Петербург', 'Санкт-Петербург', 'пр. Панорамный, д. 21'),
('Курорт "Зеленые холмы"', 'Кавказ', '["Горные прогулки", "Пляж", "Кафе с региональной кухней"]', 80, 'http://localhost:8000/static/images/hotels/32.webp', 5, 'Отдыхайте среди зеленых холмов Кавказа', 'Кавказ', 'ул. Холмистая, д. 22'),
('Оздоровительный курорт "Здоровье и гармония"', 'Сочи', '["Лечебные процедуры", "СПА-салон", "Бассейны с минеральной водой"]', 120, 'http://localhost:8000/static/images/hotels/33.webp', 5, 'Позаботьтесь о своем здоровье и гармонии на нашем курорте', 'Сочи', 'ул. Здоровая, д. 23'),
('Гостиница "Семейное гнездо"', 'Москва', '["Детский клуб", "Бассейн", "Ресторан с детским меню"]', 100, 'http://localhost:8000/static/images/hotels/34.webp', 4, 'Отличное место для семейного отдыха в Москве', 'Москва', 'ул. Семейная, д. 24'),
('Отель "Сказочные дали"', 'Карелия', '["Экскурсии по лесу", "Баня", "Каминный зал"]', 25, 'http://localhost:8000/static/images/hotels/35.webp', 3, 'Погрузитесь в сказочные дали и загадочные леса Карелии', 'Карелия', 'ул. Дальная, д. 25'),
('Курорт "Морская радуга"', 'Сочи', '["Аквапарк", "Пляжные вечера", "Кафе с национальной кухней"]', 200, 'http://localhost:8000/static/images/hotels/36.webp', 5, 'Радужные эмоции и разнообразие активностей на нашем курорте', 'Сочи', 'ул. Морская, д. 26'),
('Отель "Под соснами"', 'Судак', '["Пляж", "Барбекю", "Детская анимация"]', 30, 'http://localhost:8000/static/images/hotels/37.webp', 3, 'Отдыхайте в тени сосен на побережье Крыма', 'Судак', 'ул. Сосновая, д. 27'),
('Пансионат "Здоровый край"', 'Алтай', '["Экскурсии по горам", "Пляж", "Ресторан с региональной кухней"]', 40, 'http://localhost:8000/static/images/hotels/38.webp', 4, 'Отдыхайте в здоровом краю среди красот Алтая', 'Алтай', 'ул. Здоровый, д. 28'),
('Отель "Солнечные поля"', 'Ростов-на-Дону', '["Теннисные корты", "Бассейн", "Ресторан с региональной кухней"]', 70, 'http://localhost:8000/static/images/hotels/39.webp', 4, 'Насладитесь солнечными полями и комфортом нашего отеля', 'Ростов-на-Дону', 'ул. Полевая, д. 29'),
('Гостиница "Тихий берег"', 'Анапа', '["Пляж", "Водные виды спорта", "Бар у бассейна"]', 50, 'http://localhost:8000/static/images/hotels/40.webp', 3, 'Отдыхайте на тихом берегу Черного моря', 'Анапа', 'ул. Тихая, д. 30'),
('Отель "Альпийская роза"', 'Альпы', '["Горные прогулки", "Бассейн с видом на горы", "Ресторан альпийской кухни"]', 100, 'http://localhost:8000/static/images/hotels/41.webp', 4, 'Откройте для себя красоту альпийских гор в нашем отеле', 'Альпы', 'ул. Альпийская, д. 31'),
('Курорт "Морское счастье"', 'Севастополь', '["Частный пляж", "Бассейн с морской водой", "Ресторан с видом на море"]', 150, 'http://localhost:8000/static/images/hotels/42.webp', 5, 'Отдыхайте на нашем курорте и наслаждайтесь морским счастьем', 'Севастополь', 'ул. Морская, д. 32');