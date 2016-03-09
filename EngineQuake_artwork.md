# Engine Quake2d #

_**ARTWORK** - помечено что нужно нарисовать. будет вид сверху, 2д, скорее всего с масштабированием, так что стиль должен быть мультяшный, контрастный, похожий на оригинал_

# Карта состоит из комнат. Комната - прямоугольник случайного размера, в углах которого могут быть порталы. Порталы связывают комнаты, в любой комнате от одного до 4 порталов, портальные пути постоянны и не всегда двух сторонни. У комнаты есть id
# Портал - до прохода по нему не ясно куда он ведет _**ARTWORK**_
# Цель игроков - в убийстве других игроков. за каждое убийство начисляется фраг, игра идет до н фрагов
# У игрока _**ARTWORK**_ есть:
  * жизни _**ARTWORK**_
  * броня _**ARTWORK**_
  * оружие _**ARTWORK**_
  * количество фрагов _**ARTWORK**_
# На полу комнат появляются с периодичным (постоянным для карты) временем в одном и том же месте (для карты) _**ARTWORK**_ всего - маленькие иконки
  * Аптечки _**ARTWORK**_ иконка, будет лежать на полу
    * http://quake.wikia.com/wiki/Megahealth +100
    * http://quake.wikia.com/wiki/Regeneration восстанавливает 60 сек или до 200
    * http://quake.wikia.com/wiki/Stimpack восстанавливает жизнь до конца
    * http://quake.wikia.com/wiki/Medikit - желтый +25, золотой +50
  * Броня _**ARTWORK**_ иконка, будет лежать на полу и в статусе игроков поднявших отображаться
    * http://quake.wikia.com/wiki/Armor_Shard +5
    * http://quake.wikia.com/wiki/Heavy_Armor +100
    * http://quake.wikia.com/wiki/Light_Armor +50, поглощает 2/3
  * Оружие _**ARTWORK**_ объект который будет "в руках игроков рисоваться", а также лежать на полу
    * http://quake.wikia.com/wiki/Gauntlet Gauntlet - на полу не лежит, но нарисовать надо 50
    * http://quake.wikia.com/wiki/Machine_Gun_%28Q3%29 Machine Gun 7 макс 200
    * http://quake.wikia.com/wiki/Shotgun_%28Q3%29 Shotgun 10/дробина, 10 дробин, все попали - 1110, макс - 200
    * http://quake.wikia.com/wiki/Lightning_Gun_%28Q3%29 Lightning Gun 8 макс 200
    * http://quake.wikia.com/wiki/Plasma_Gun Plasma Gun
    * http://quake.wikia.com/wiki/Railgun Railgun 100 макс 200
    * http://quake.wikia.com/wiki/BFG10k_%28Q3%29 BFG10k 100/взрыв макс 200
    * http://quake.wikia.com/wiki/Grenade_Launcher_%28Q3%29 Grenade Launcher 100/взрыв макс 200
    * http://quake.wikia.com/wiki/Rocket_Launcher_%28Q3%29 Rocket Launcher 100/взрыв макс 200
  * Боеприпас _**ARTWORK**_ - это лучше всего наверное срисовать с символического изображения оружия в квейке. будет лежать на полу + будет символизировать оружие в значках игроков
    * http://quake.wikia.com/wiki/Bullet Bullet 50 Machine Gun
    * http://quake.wikia.com/wiki/Cell Cell 30 Plasma Gun
    * http://quake.wikia.com/wiki/Grenade Grenade 5 Grenade Launcher
    * http://quake.wikia.com/wiki/Rocket Rocket 5 Rocket Launcher
    * http://quake.wikia.com/wiki/Shell Shell 10 Shotgun
    * http://quake.wikia.com/wiki/Slug Slug 10 Railgun
    * Lightning белый Lightning Gun
    * Gauntlet - такого боеприпаса нет, но нужен _**ARTWORK**_
  * Усилители|разные штучки: _**ARTWORK**_
    * http://quake.wikia.com/wiki/Quad_Damage - усилитель
    * http://quake.wikia.com/wiki/Pentagram_of_Protection - неуязвимость
    * http://quake.wikia.com/wiki/Battle_Suit - частичная неуязвимость

# Игрок управляет роботом, у которого есть 2 независимых друг от друга направления - куда смотрит пушка и куда смотрят ноги (шасси). Пушка крутится довольно медленно, шасси-очень быстро, каждый фрейм можно задавать желаемое значение направлений пушки и шасси, и они будут туда поворачиваться. _**ARTWORK**_ надо отдельно нарисовать шасси, отдельно "башню"... вообще надо подумать, кем будут наши роботы - роботами, людьми или еще чем? главное чтоб красиво и без проблем анимировать по минимуму

# Комманды |переменные пользовательского бота
  * aim, dir, aim\_real, dir\_real - цель пушки (желаемая, можно установить и будет в ту сторону крутиться медленно), направление шасси (желаемое), текущая (реальная) цель пушки, текущее направление шасси. в градусах от севера
  * setAimToObj - установить цель на обьект
  * setAimToCoord - установить цель на координату
  * setAim - установить цель в градусах от севера
  * setDirToObj - установить направление шасси на обьект и т.д.
  * setDirToCoord
  * setDir
  * isAimed - ...
  * isDired - если dir == 