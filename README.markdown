Modern Art Game Simulator
=========================

This runs a simulation of the board game Modern Art; AIs compete in the simulated game.

Background
----------

* [game rules](http://www.gamecabinet.com/sumoRulesBank/ModernArt.html)
* [rough design doc](https://docs.google.com/document/d/16GLui4uT4IijqQOH5ZBtPu2az3gX72HdD3pAE-Jgjng/edit)

Running
-------

	make run

This will run the simulator for one game with the current players, logging game events, and picking a winner.

If necessary, this will try to download and install the [protobuf](https://code.google.com/p/protobuf/) compiler before running the game.

Adding Players
--------------

Players are drawn from any Python module which is placed in players/ and defines a class called Player. This can be a Python source file or a bytecode (pyc) file.

Version History and Roadmap
---------------------------

* Next Communication with the Player needs expansion, so the Player can make better decisions. Roughly, all the logging messages from GameMaster should be communicated to all the Players.
* v0.1 The simulator runs a valid game, with a very limited Player interface.

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
