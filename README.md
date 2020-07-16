#rain_checker
Rain Updater for Olisto connectors

This checker will periodicly check for the expected rain for a configured location (netherlands) using the buienradar api.
Using Lon / Lat you can configure you get a 2 hour forcast of rain. 000 means no rain  255 means heavy rain

This value can be converted to mm/h by:
 mm/h = 10^((value -109)/32)
f.e.
77 = 0.1 mm/uur
200 = 700 mm/uur

drizzle = 0.1 mm/h (motregen)
KNMI definition of rain: drops of water with a min. diamter of approx. 0,5 - 0.6 mm rain (which will make sound when hitting objects)
When talking about sufficient (real rain) we generally mean a 1 - 2 mm of water per hour.
So when talking about "real" we take a general min. of 77 of rainscore

Heavy thunder will give 30 - 80mm of rain. Its does happen to have over 100 mm of rain in 2 / 3 hours for very heavy thunderstorms.
Tropical rains can give 1000 mm/h (very exceptional in western europe)

test_data = "
077|09:35
150|09:40
000|09:45
000|09:50
000|09:55
000|10:00
000|10:05
000|10:10
000|10:15
000|10:20
000|10:25
000|10:30
000|10:35
000|10:40
000|10:45
000|10:50
000|10:55
000|11:00
000|11:05
000|11:10
000|11:15
000|11:20
000|11:25
000|11:30
000|11:35
"

get rain data:
http://gps.buienradar.nl/getrr.php?lat=51&lon=3')

Information about the API:
https://www.buienradar.nl/overbuienradar/gratis-weerdata

Remark:
Currently you are allowed to use the buienradar api for personal use. If you are creating commercial project using this buienradar API you will have to contact buienradar (RTL Netherlands) to get permission.
