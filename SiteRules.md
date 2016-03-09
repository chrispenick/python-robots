# Определения #

  * **Игрок** - участник проекта
    * **Рейтинг в каждом виде игры** равен самому большому рейтингу среди ботов игрока в данном виде игры
    * **Рейтинг** - общий рейтинг игрока. Высчитывается по формуле: **рейтинг игрока = наибольший рейтинг игрока в виде игры + следующий рейтинг игрока/2 + следующий/4 + следующий/8**...
  * **Движок** (дисциплина, вид игры) - вид игры на сайте (танчики, быки и коровы, etc)
  * **Бот** - программа, написанная игроком. Разделяются по:
    * **Языкам программирования**
    * **Активизированный/деактевизированный** - изначально при добавлении/редактировании бот деактивизирован и не участвует в боях. Чтобы он участвовал, его нужно **активизировать**. У игрока может быть до 5 активизированных бота
    * **Рейтинг бота** - рейтинг, присвоенный боту по результатам его **рейтингового турнира**
    * **Групповой рейтинг бота** - рейтинг, равный групповому рейтингу партии в которой состоял бот последний раз (или сейчас состоит)
    * **Исходник бота** - виден только у активизированных, **устаканеных** ботов, когда владелец зайдет на сайт после устаканивания и пройдут сутки. виден всем игрокам - владельцам ботов, которые на две **категории** выше по **списку рейтинга**
  * **Группы ботов-друзей** (партия) - в групповых боях сражаются только вместе. Для добавления чужого бота в друзья своему игрок-владелец чужого бота должен подтвердить.
    * **Рейтинг партии** - рейтинг, присвоенный партии по результатам **группового рейтингового турнира**
  * **Язык** - ЯП, на котором написан бот, может быть компилируемым или интерпретируемым
  * **Личка** - личная почта
  * **Бой** - сражение ботов
    * **Один на один**
      * **Тестовый бой** с дефолтным ботом - проводится при **активизации** бота. Не влияет на рейтинг, в случае проигрыша - бот не активизируется
      * **Заказной** - игрок предложил другому игроку бой, предложил условия. Другой игрок может согласится или отказаться. Не влияет на рейтинг
      * **Автоматический** - при активизации бот проходит **рейтинговый турнир**
    * **Групповой** - n на n ботов
      * **Заказной** - игроки создают заявку на бой, в которой обговорены условия. На сайте есть список активных заявок. Можно сделать "приватную заявку", приглашать туда ботов. Все участники должны подтвердить желание участвовать, не влияет на рейтинг
      * **Автоматический** - при активизиции всех ботов в **группе друзей-ботов** бот с друзьями участвует в **групповом рейтинговом турнире**
    * **Приоритет** - бои при планировании заносятся в очередь, преимущество отдается заказным и тестовым боям (тестовым боям отдается очень сильное преимущество)
    * **Фэйл** - если движок сообщает что бот вывалился (тормозит, жрет память, отдает некорректные комманды) - его деактивизируют


# Рейтинговые турниры #
Понятия:
  * **Рейтинг** - числовое значение, чем больше - тем лучше. изначально = 0
  * **Список** - список ботов по этой дисциплине, отсортированный по рейтингу
  * **Место** - место в **списке**, чем меньше - тем лучше
  * **Категория** - список ботов делится на n (n=func(количество ботов в списке)) категорий.

Процедура:
  1. Бот **активизируется**. При этом он компилируется и, скомпилированный, сохраняется
  1. Бот заносится в последнюю **категорию**
  1. Бот дерется в категории со всеми по очереди
  1. Если бот победил _0,8 (надо подумать)_ ботов в категории, _его рейтинг становится на единицу больше чем максимальный рейтинг в категории, и он переходит в следующую категорию_
  1. Идем на **пункт 3**
  1. Если за _3 итерации_ _категория не изменилась больше чем на 1_, бот **устаканился** - бои прекращаются, владельцу высылается на личку сообщение о присвоенном рейтинге