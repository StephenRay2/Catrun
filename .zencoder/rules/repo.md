---
description: Repository Information Overview
alwaysApply: true
---

# Catrun Game Information

## Summary
Catrun is a 2D game developed with Pygame where the player controls a character named Corynn in an open world environment. The game features various biomes, harvestable resources, and interactive mobs like cats and squirrels. Players can collect items, manage inventory, and interact with the environment.

## Structure
- **assets/**: Contains all game resources
  - **music/**: Game music files
  - **sounds/**: Sound effects
  - **sprites/**: Visual assets organized by category (biomes, buttons, items, mobs, player, tiles)
- **main.py**: Entry point and game loop
- **mobs.py**: Classes for player and mobile entities (cats, squirrels)
- **world.py**: Environment objects and resource management
- **inventory.py**: Item and inventory system
- **buttons.py**: UI button implementation

## Language & Runtime
**Language**: Python
**Version**: Python 3.12.0
**Framework**: Pygame 2.6.1

## Dependencies
**Main Dependencies**:
- pygame 2.6.1
- pygame-ce 2.5.1
- Standard Python libraries (sys, time, random, math)

## Build & Installation
No formal build process is required. The game can be run directly with Python:

```bash
python3 main.py
```

## Main Components

### Player System
- Player class with stats (health, stamina, hunger, warmth)
- Movement and animation system
- Inventory management
- Resource harvesting capabilities

### World Generation
- Multiple biome types with different backgrounds
- Procedurally placed resources (rocks, trees, berry bushes)
- Collision detection system
- Resource harvesting and regrowth mechanics

### Mob System
- Base Mob class with common behaviors
- Cat class with different cat types and taming mechanics
- Squirrel class with movement patterns
- AI-controlled movement and animation

### Inventory System
- Item types with properties (stack size, weight)
- Inventory slots and management
- Visual inventory interface
- Resource collection and storage

### UI Components
- Button class for interactive UI elements
- Hover and click detection
- Visual feedback for user interaction

## Game Assets
- Character sprites with multiple animation frames
- Various biome background textures
- Resource sprites (trees, rocks, berry bushes)
- Item icons for inventory
- Multiple cat and squirrel sprites
- Music and sound effects