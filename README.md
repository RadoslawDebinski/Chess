# Chess

#  Description

The purpose of the project was to create a chess game with a dedicated logic engine, with the possibility to play by mouse and keyboard (chess algebraic notation in a separate translation module). Moreover, according to assumptions, the game should contain mechanisms of:
* **Possibility to play with a bot** controlled by a dedicated **convolutional neural network** model;
* **Multiplayer mode** with communication by **IPv6**;
* **Game saving in SQLite** database and XML file;
* **Millisecond analog clocks** for each player;
* **Saving game status** in JSON file;
* **Animated history playback** gave from the file (controlled by the engine);
* **Marking possible moves** while holding a piece.

The application was written in Python 3.10.9, using the Qt Framework, in the PyCharm 2023.1.1 (Professional Edition) environment.

# User interfece

Interface is splitted to two main parts:
  * Input user interface with:
      * Text box with adequate mask for IPv6 (multiplayer mode);
      * Port Text box (multiplayer mode);
      * Grid layout to choose game mode;
      * Combo boxes to choice game to load or game settings;
      * Button to apply all of the configurations.
      
      ![2023-05-19_18h59_43](https://github.com/RadoslawDebinski/Chess/assets/83645103/b4d0bc84-7cd1-4631-9635-eb73b8e0ea55) ![2023-05-19_19h10_58](https://github.com/RadoslawDebinski/Chess/assets/83645103/8cb92648-a927-4b14-9b19-ed106ebb9153)

      Fig. 1. Inup user interface clear and with example data

  * The game user interface contains:
      * Board section with pieces, labels, and the possibility to change color style;
      * Check / Mate buttons to inform about game status;
      * A text box for inserting moves in chess algebraic notation. Move confirmation could be preceded by “Submit text move button” or pressing Enter in the text box;
      * Light and dark clocks for each player;
      * Continue button to submit proceed move and change clock;
      * Start, Reset and Save Buttons to control the game
      * Additional window to choose pawn promotion. 
      
      ![2023-05-19_19h06_43](https://github.com/RadoslawDebinski/Chess/assets/83645103/4a683acf-8395-41d4-8ee0-ae58a0adb39f)
      
      Fig. 2. The game user interface with pawn promotion window in the center
      
      ![2023-05-19_19h07_00](https://github.com/RadoslawDebinski/Chess/assets/83645103/cf67a6f7-a1cf-4f24-ae13-0784c03521da)
      
      Fig. 3. The game user interface with second color style
      
# Code
The structure of the project files is as follows:
* _**main.py**_ - simple UI with a selection of game mode;
* _**server.py**_ - example of IPv6 server for multiplayer connection;
* _**configs folder**_ - holding JSON files with saved games configurations;
* _**saves folder**_ - holding DB and XML files with games histories;
* _**core folder**_ - all main elements of the the chess game;
  * _**chessBoard.py**_ - a class that creates all pieces objects due to current board set configuration; 
  * _**chessClock.py**_ - a module that creates and updates analog clocks for each player;
  * _**chessEngine.py**_ - chess logic engine. It takes as input the current board set and games status and gives new ones as output. All chess rules were implemented among others:
    * en passant;
    * promotion;
    * castling;
  * _**chessPiece.py**_ - this class creates a single chess piece and proceeds with its movement on board. Calculations for holding and releasing a piece are included;
  * _**gameStaus.py**_ - a class which contains all useful information for all game modes like single, multi, playback etc.;
* _**gameModes**_ folder - other useful classes specified in chosen game mode;
  * _**controllerAI.py**_ - a class which translates current board set to inputs for neural network and proceeds its movement;
  * _**playBackGame.py**_ - module which retraces all moves from gives DB or XML file;
  * _**saveGame.py**_ - a class which creates files mentioned in configs and saves;
  * _**stockEngine.py**_ - implementation of communication wich stockfish engine due to teaching AI model;
* _**interaction**_ folder - all modules somehow connected with UI;
  * _**boardCommunication.py**_ - set of functions which proceed user communication windows;
  * _**chessGraphics.py**_ - binary file created from .qrc which contains all used graphics;
  * _**loadGame.py**_ - a main class which proceeds:
    * communication with the player by load.ui interface;
    * history playback triggering;
    * communication by IPv6 protocol;
    * data transfer of text messages;
    * and more minor functionalities;
  * _**loadui.ui**_, _**start.ui**_ - user interfaces;
  * _**textEngine.py**_ - a translator from chess algebraic notation to chess board coordinates;
* _**modelsAI**_ folder - files that are necessary for AI game mode creation not for the game as such;
  * _**convolutional.py**_ - convolutional neural network teaching model;
  * _**dataCreation.py**_ - creation of dataset with inputs and outputs for teaching;
  * _**evolutionary.py**_ - skeleton for future usage of evolutionary algorithm supported bot;

# Discussion

To sum up the implementation of the above project, the application implements all the initial assumptions. The undoubted advantages of our solution include:
* **Intuitive interface**, the application is legible and does not contain any redundant elements which could confuse the user;
* A significant amount of **game modes** single, multi and AI enforced;
* **Changeable graphic layout** for board and pieces;
* **Immersive analog clocks**;
* **Saving and playback** of game status which makes it less binding and more flexible for daily usage;
* **Chess algebraic notation** for those who want to learn serious chess tournaments slang;

On the other hand, there are also flaws in the application and eliminating them would be the first step in the further development of the project. Future upgrades that have not yet been undertaken may include:
* **Interface improvements** to enhance its aesthetics;
* **Adding a dark background** for the entire application, it's standard in today's software to make the background of the UI have at least a light and dark version;
* **Implementation of difficulty levels** by the usage of different AI models like for example evolutionary algorithm mentioned in evolutionary.py. Usage of different models should cause the creation of bots with different playstyles not only various skill levels

Thus, the product already has a number of useful functionalities and is fully usable, but there is still a lot of room for future development.

