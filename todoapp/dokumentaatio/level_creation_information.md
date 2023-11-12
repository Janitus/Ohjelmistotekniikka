# Tiled Editor configs

Use Tiled Editor to create maps.

The configurations:

Tile size: 32x32 pixels

Tileset: assets/images/tileset.png

# Quickstart

To create a functioning from start to finish map, you need to create the following things

	1. Environment layer (This is where players can walk and collide on)

	2. At least one object layer

	3. ..where you place a point object with the name "spawn_player"

	4. ..where you place a rectangular zone with the name "zone", with a custom string property named "exit"

	5. include the map in a campaign, by placing it in the same directory, and writing this level's name inside the order.txt

# Map information

Lighting:

	You can set the lighting by Map -> Map Properties -> Find Custom Properties -> Add a color property -> Name it "darkness" -> Select color. Default is (128, 128, 128)

# Tile Layers:

Functional:

	- MANDATORY: "Environment" Layer. This is where collision map is created, and if a tile is not empty, everything will collide with this layer.

	- MANDATORY: At least one Object Layer. You can name it whatever. Multiple object layers is recommended for ease of editing.

	- "Ladder" Layer. A tile in this layer indicates that the spot is climbable.

Cosmetic:

	- You can name these layers as you see fit. Anything placed in these layers are purely cosmetic and serve only to be rendered. Note that the order of the layers dictates the rendering order, so you can place these below or above the functional layers as you see fit.
	
# Object Layers:

To insert objects in tiled, you must use either Insert point (I) or Insert rectangle (R) and place them into the map. You also need at least one layer for objects to do this.

Spawns - Insert Point (I)

	Rename the object as "spawn_" + substring according to your needs:
		"player" - For player spawn
		"myenemyname" - For the enemy based on their name

Light - Insert Point (I).

	Rename the object as "light"
	Give it two custom properties.
		integer property with name radius, and a numerical value for it.
		color property with the name color, and use tiled to set the color.

Zone - Insert Rectangle (R)

	All zones are "triggers", meaning that they can be used to trigger certain actions. Those actions only trigger when all conditions are met simultaneously.
	By default, all zones are given the following trigger: detect whether the player is in the zone, and if they are in, the condition is true.

	Rename the object as "zone"
	Set a condition. Available conditions:
		string property with the name "key". The value of the key can be set as any string the user likes, for example, "red". This means that when a player has a "red" key, this condition will be true. An example: string property "key", value "red"

	To trigger actions you have two options

	1. Embedded actions
		Embedded actions are directly created within zones. These can be done by clicking the zone, and setting a custom property.
		"exit" (as string property) - For entering the next level
	
	2. External actions
		Create a custom property (as object property), with the name "action" + any optional substring. Then select any other object as your property value. To create actions as objects, read more under "Actions"

Actions - Insert point (I)

	Rename the object as "action"
	Create a string property. The property name dictate the action type. Those names are:
		destroy - It will destroy a tile from the "Environment" layer when triggered.
		
# Save information
	
The levels are saved as .tmx. You can name your levels any name.