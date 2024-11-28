# pygame-local-multiplayer

**Description**

A prove-of-concept game/program for learning how to implement local multiplayer without a server and internet. Each device runs a client/sender thread, which broadcasts player inputs to the local network to be processed, and a server/listener thread/main program, which processes the broadcast player inputs, runs the game functionality and displays the game to a pygame window. These 
programs run on all devices, and the inputs are broadcast to the local network and then received to be processed independently by each player.

**Used language**

Python

**Used modules**

socket, threading, pygame
