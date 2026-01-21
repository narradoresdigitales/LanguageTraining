# Spanish Language Training Game

## Overview

This project is a Python-based interactive language training game designed to improve Spanish comprehension and conversational skills through immersive, scenario-based gameplay. The goal is to create a software experience that combines educational content with engaging gameplay mechanics, allowing players to practice language skills in context.

The game places the player in a series of missions where they interact with NPCs, respond to prompts in Spanish, and make decisions that influence the progression of the story. Each mission presents objectives, questions, and feedback to guide the player through realistic language exercises.

**How to Play:**  
1. Start the game and create a character profile with a name and password.  
2. Complete introductory briefings and tutorials.  
3. Advance through missions by reading NPC dialogue, typing responses in Spanish, and making choices when prompted.  
4. Mission outcomes depend on correct usage of keywords and decisions made throughout the scenarios.  
5. The game provides feedback, saves progress, and transitions to new missions automatically.

**Purpose:**  
The primary purpose of this software is to explore the intersection of game development and educational technology. By combining Python programming, Pygame graphics, and interactive text-based scenarios, this project demonstrates how software can be used as a learning tool while reinforcing practical coding skills.

[PYGAME Demo Video](https://youtu.be/b4UElMj7jN0)
[MONGODB Demo Video](forthcoming)

---

## Development Environment

- **Programming Language:** Python 3.11  
- **Game Framework:** Pygame  
- **Code Editor:** Visual Studio Code  
- **Additional Tools:** JSON for dialogue management, GitHub for version control, audio editing software for sound assets

**Libraries Used:**  
- `pygame` – for graphics, input handling, and sound  
- `json` – to store and load mission dialogue and questions  
- `pymongo` for MongoDB connectivity
- `python-dotenv` for managing environment variables
- `hashlib` for password hashing

---

# Cloud Database

This project uses **MongoDB Atlas**, a cloud-hosted NoSQL database service. MongoDB Atlas was chosen for its scalability, ease of setup, and seamless integration with Python applications using the PyMongo driver.

The database consists of two related collections:

- **users**
  - Stores user authentication data.
  - Fields include:
    - `_id` (ObjectId)
    - `username`
    - `password_hash`

- **progress**
  - Stores gameplay progress for each user.
  - Fields include:
    - `user_id` (references a user’s `_id`)
    - `current_mission`
    - `missions_completed` (array of completed mission IDs)

These collections are related through the `user_id` field, allowing each user to have persistent and independent progress tracking.


# Useful Websites

- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)


# Future Work

- Improve password security by adding salting and stronger hashing algorithms.
- Add additional missions and branching mission paths.
- Implement user profile management (password changes, progress reset from UI).
- Add cloud change notifications or real-time sync features.
- Improve error handling and user feedback during login and database operations.

## How to Run the Game

1. Clone this repository:  
   ```bash
   git clone https://github.com/narradoresdigitales/LanguageTraining.git 
   cd language-training-game
