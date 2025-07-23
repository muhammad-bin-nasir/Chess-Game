# 🧠 Minimax Chess in Python

This is a simple yet powerful 2D Chess Game built with **Pygame** in **Python**, featuring:

- Human vs Human mode (on same device)
- Human vs AI mode (using the Minimax algorithm with Alpha-Beta pruning, depth-limited to 4)
- GUI built with Pygame (no command line fiddling)
- Mode selection screen (landing page style)
- Move highlighting, turn-based control, and full legal move validation

## 🔧 Technologies Used

- Python 3.10
- Pygame 2.6.1
- python-chess
- Minimax with alpha-beta pruning

## 🧠 AI Strategy

The AI opponent uses a depth-limited Minimax algorithm with Alpha-Beta pruning (depth = 4). It evaluates board states using a basic material-value function, prioritizing piece captures and positional play.

## 📦 How to Run

1. Clone or download this repo.
2. Ensure Python 3.10+ is installed.
3. Install dependencies:
   ```bash
   pip install pygame python-chess
