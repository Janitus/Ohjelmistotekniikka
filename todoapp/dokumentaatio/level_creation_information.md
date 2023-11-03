Use Tiled Editor to create maps.

The configurations:

Tile size: 32x32 pixels
Tileset: assets/images/tileset.png
Layers:
	- Background - When a layer is supposed to only act as a background, name it as "Background" + .. Can have multiple
	- Environment - When a layer is supposed to act as both walkable and collideable (e.g. wall), name it as "Walkable". Only one required
	- Platform - When a layer is supposed to act only as walkable (But can jump to it from underneath), name it as "Platform". Only one required
	- Over - Similar to background, but the objects will be placed in front of everything. These do not interact with anything! Can have multiple.
	- Objects - See more details below. Name it as "Objects". Only one object layer is required
	
Objects:
	To create an object, create an object layer in the tiled editor. In order to create the following..
	Spawns - Insert Point (I) (and place them into the map). The name of the object will dictate the type of a spawn.
		"Player" - For player spawn
		"Enemy0" - For x enemy..
		.. Fill rest

	Light - Insert Point (I).
		There is only one type of light, Point Light. To create a light, name the object "light" and give it two custom properties.
			radius as integer field, with the integer becoming the radius in-game.
			color as a color field.

	TODO Zones, traps, etc.
	
The levels can be saved as .tmx. Make sure to name your levels as "Level" + number.