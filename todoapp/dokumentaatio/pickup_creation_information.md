# To create a new pickup, you need the following three:

- name
- image.png
- info.txt
	- pickup information within the info.txt

# Steps

1. Go to assets/pickups/ directory
2. Create a new directory with your pickup's name, assets/pickups/mypickupname/
3. In this directory, insert any image.png you wish.
4. Create info.txt
5. Fill the info.txt with any or multiple of the following
	- money:amount
	- health:amount
	- life:amount
	- ammo:amount
	- key:name, the name of the key is important! For instance key:red, the "red" will be the string the game looks for when you're approaching a door with "red" as requirement!

If you want your pickups to appear in the game, you then insert objects in the tiled editor named pickup_mypickupname, and
the game will load them upon startup.