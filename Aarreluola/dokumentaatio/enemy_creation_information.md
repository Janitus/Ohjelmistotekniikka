# To create a new pickup, you need the following three:

- name
- image.png
- info.txt
	- pickup information within the info.txt

# Steps

1. Go to assets/enemies/ directory
2. Create a new directory with your enemy's name, assets/pickups/myenemyname/
3. In this directory, insert any image.png you wish.
4. Create info.txt
5. Fill the info.txt with any or multiple of the following
	- width:int
	- height:int
	- speed:float
	- melee_damage:int
	- melee_knock:int
	- health:int
	- max_health:int
	- gravity:float
	- avoid_falls:bool (it will default to false if not written as 'true'.) This attribute means that the enemy will turn around if it's about to fall off the edge.

If you want your enemies to appear in the game, you then insert objects in the tiled editor named spawn_mymyenemyname, and the game will load them upon startup.

Tip: I do not recommend width and height larger than 32, although they may be functional I do not have the necessary code to make them "as expected"