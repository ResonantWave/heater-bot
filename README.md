# Heat bot
Control your house heating from a Telegram bot

### Current features
 * Manually turn on or off the heating
 * Get whether the heater is on or off
 * Keep the heat on for a specified amount of time (eg, 2 hours from now)

### Prerequisites
 * A heating system with a simple on/off switch, or a battery powered timer.
 * A NodeMCU with a relay connected to the heater switch or timer.
 * A Raspberry Pi (any model), that will host the Telegram bot.
 * A cup of coffee or any hot beverage to enjoy while you're setting everything up
 
### Code
#### Raspberry Pi
This project requires some libraries, `requests` and `pyTelegramBotAPI`. 
You can set everything up by running `pip install -r requirements.txt`

You will need a Bot API key, obtainable via @BotFather on Telegram. Put it on [heatBot.py](heat_telegrambot/heatBot.py)

Also, you will need to put your user ID on the `allowed_numbers` list. To find your ID, start the bot and send `/start`. 

Setting the NodeMCU IP Address is also a necessary step. Change it in `base_url`.
 
#### NodeMCU
Using the [Arduino IDE](https://www.arduino.cc/en/Main/Software), flash the sketch in the [heat_nodemcu](heat_nodemcu) folder.
Don't forget to set your WiFi's SSID and password before flashing. By default port 82 will be used.
There's also a commented block for setting a static IP Address

### Other
 1. Can I use the Raspberry Pi directly as the heater controller instead of using the NodeMCU?
      Yes, of course. Open an issue if you want more details on this.

### Planned features
 - [ ] Interval heating (eg, turn on heater 2 hours from now, turn off heater 6 hours from now)
 - [ ] Recurrent heating schedule

### Contributors
 *  [@ResonantWave](https://github.com/ResonantWave)

### Contributing
* The code is licensed under the [GPL V3](LICENSE)
* Feel free to contribute to the code
