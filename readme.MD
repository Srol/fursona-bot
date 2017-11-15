This was a stupid bot I made for Mastodon in about 45 minutes that ended up being really popular. When someone triggers the bot, it generates a random RGB color, gets a name for that color from [The Color Api](http://www.thecolorapi.com), then matches it with a species taken from the animal, bird, reptile and amphibian lists at [observation.org](http://www.observation.org).

The bot is set up to run on Heroku, although you will need to create a database with one "last_toot" integer table, as well as a scheduler, for it to work properly. 

You also will need to follow the directions for generating Mastodon instance credentials from the [Mastodon.py](https://github.com/halcy/Mastodon.py) library. The bot is configured to run on [BotsIn.Space](http://botsin.space), but any instance that allows bots should work.

