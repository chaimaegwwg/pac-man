#this is readme for u u can write any thing u want wla heta u question
u missions is :
--> parsing:
- parse comments 
# the problem is they said at this part :
        --V.2 Configuration file
The config file uses JSON. In addition to the standard JSON format, you must handle
comments. Lines starting with # are comments and must be ignored. You may also
support additional comment styles (e.g., C or C++).

# -----> but the json file doesn't support comments like # // etc. ask Noaman or someone else about if we must use exactly a json file or just .txt file is ok.

--> render the menu of pac-man u can check subject for more details and the menu of the last



###       infos:

# -----> load() vs loads()

This is an important Python distinction:

json.load(file)

➡️ Reads JSON from a file

json.loads(string)

➡️ Reads JSON from a string


# --> clock utility 
-----> Without clock.tick(60)
The loop runs as fast as possible, potentially consuming more CPU.

------> With clock.tick(60)
The loop is limited to about 60 iterations per second, or one iteration every 16.7 ms.


# about get_rect() method

First, images/pygame.Surfaces don't have a position, so you have to store the blit position in the rect. When you call the get_rect method of a pygame.Surface, Pygame creates a new rect with the size of the image and the x, y coordinates (0, 0). To give the rect other coords during the instantiation you can pass an argument to get_rect, mostly center or topleft is used. To move the rect later, you can change any of these attributes of the rect:

