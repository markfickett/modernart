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
	Naive 1 puts Once-Around Krypto up for auction.
	Naive 0 bids 9.
	Mark #26 bids 10.
	Naive 1 bids 16.
	Naive 1 pays 16 for Once-Around Krypto.
	Naive 1 pays 16 and has 84 left.
	The bank takes 16.
	...
	Starting a new auction.
	Naive 0 puts Double Krypto up for auction.
	Mark #26 adds a card: Open Krypto
	Simultaneously, Naive 1 passes.
	Simultaneously, Naive 0 bids 4.
	Simultaneously, Mark #26 passes.
	Naive 0 increases the bid to 4.
	...
	Simultaneously, Naive 1 passes.
	Simultaneously, Naive 0 passes.
	Simultaneously, Mark #26 passes.
	Naive 1 wins with a bid of 40.
	Naive 1 pays 40 for Double Krypto, Open Krypto.
	Naive 1 pays 40 and has 70 left.
	Naive 0 gets paid 20 and now has 28.
	Mark #26 gets paid 20 and now has 169.
	...
	Starting a new auction.
	Naive 1 puts Double Christin P. up for auction.
	Naive 0 adds a card: Sealed Christin P.
	Round ends with 5 from Christin P..
	...
	Mark #26 finishes with 427
	Naive 1 finishes with 284
	Naive 0 finishes with 97
	Mark #26 is the winner!

Adding Players
--------------

Players are drawn from any Python module which is placed in players/ and defines a class called Player. This can be a Python source file or a bytecode (pyc) file.

To add your player, create players/<yourname>.py, subclass players.base.Player, and edit away! To compete, check players/<yourname>.pyc in to master. (Checking only the bytecode into master lets others play against your player without seeing its source; you can of course check the source into master if you like.)

Version History and Roadmap
---------------------------

* v0.2: Send events to Players, allowing more complex analysis and decisions.
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
