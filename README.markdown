Modern Art Game Simulator
=========================

This runs a simulation of the board game Modern Art; AIs compete in the simulated game.

Running
-------

	make run

This will run the simulator for one game with the current players, logging game events, and picking a winner.

If necessary, this will try to download and install the [protobuf](https://code.google.com/p/protobuf/) compiler before running the game.

Example output:

	modernart $ make run
	python main.py
	Gathering the players.
	Instantiating 3 players.
	...
	Starting round number 1.
	Starting a new auction.
	Naive 0 puts Fixed Lite Metal up for auction.
	Naive 0 fixes the price at 14.
	Naive 1 passes.
	Naive 2 passes.
	Naive 0 has to buy the painting back.
	Naive 0 pays 14 for Fixed Lite Metal.
	Naive 0 pays 14 and has 86 left.
	The bank takes 14.
	Starting a new auction.
	Naive 1 puts Double Yoko, Sealed Yoko up for auction.
	Naive 2 passes.
	Naive 0 bids 42.
	Naive 1 bids 33.
	Naive 0 wins with a bid of 42.
	Naive 0 pays 42 for Double Yoko, Sealed Yoko.
	Naive 0 pays 42 and has 44 left.
	Naive 1 gets paid 42 and now has 142.
	...
	Naive 0 puts Once-Around Yoko up for auction.
	Round ends with 5 from Yoko.
	Christin P. is worth 20 this round.
	Karl Gitter is worth 10 this round.
	Krypto is worth 30 this round.
	Naive 0 gets paid 10 for: Fixed Lite Metal, Double Yoko, Sealed Yoko, Double Lite Metal, Open Lite Metal, Double Karl Gitter
	Naive 1 gets paid 0 for: Fixed Yoko, Once-Around Lite Metal
	Naive 2 gets paid 90 for: Double Christin P., Fixed Christin P., Double Karl Gitter, Once-Around Karl Gitter, Sealed Krypto, Double Yoko
	Starting round number 2.
	...
	Naive 0 finishes with 156
	Naive 1 finishes with 231
	Naive 2 finishes with 103
	Naive 1 is the winner!

Adding Players
--------------

Players are drawn from any Python module which is placed in players/ and defines a class called Player. This can be a Python source file or a bytecode (pyc) file.

Version History and Roadmap
---------------------------

* Next: Communication with the Player needs expansion, so the Player can make better decisions. Roughly, all the logging messages from GameMaster should be communicated to all the Players.
* v0.1: The simulator runs a valid game, with a very limited Player interface.

Contributing
------------

If you make a Player, you can check in the source if you want to share it, or check in a bytecode if you want to let people compete with it but not see its secrets, or you can wait for a more formal tournament.

Improvements to the GM/Player API are especially welcome.

Code Overview
-------------

There are only a few files, but the starting points are:

* game_master.GameMaster knows all the game's rules, runs the game, and manages Player interaction.
* The players module takes care of loading Players and interacting with them defensively.
* players.base.Player is a naive reference Player, which follows game rules but attempts no informed decision making.

Background
----------

* [game rules](http://www.gamecabinet.com/sumoRulesBank/ModernArt.html)
* [rough design doc](https://docs.google.com/document/d/16GLui4uT4IijqQOH5ZBtPu2az3gX72HdD3pAE-Jgjng/edit)
