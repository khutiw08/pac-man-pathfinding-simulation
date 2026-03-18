# 🎮 Pac-Man Pathfinding Simulation (BFS & A*)

A **grid-based Pac-Man simulation** showcasing real-time pathfinding using **Breadth-First Search (BFS)** and **A\*** algorithms.  
This project highlights the difference between **uninformed search** and **heuristic-based optimization** in navigation.

---

## 🖼️ Demo Preview

<p align="center">
  <img src="https://github.com/user-attachments/assets/73cd5c2e-2ee2-4170-bef5-55e53af28a4f" width="300"/>
  <img src="https://github.com/user-attachments/assets/e82b1f48-e076-47cf-bc90-a3f6f8a5d3b1" width="300"/>
</p>

---

## 🚀 Features

✨ Real-time Pac-Man movement in a grid environment  
✨ Dual pathfinding implementation: **BFS & A\***  
✨ Heuristic optimization using **Manhattan Distance**  
✨ Smooth gameplay with ~**60 FPS** using Pygame  
✨ Dynamic navigation toward nearest targets (pellets)  

---

## 🧠 Algorithms Used

### 🔹 Breadth-First Search (BFS)
- Guarantees **shortest path**
- Explores all nodes uniformly
- Higher computational cost

### 🔹 A* Search
- Uses **heuristic (Manhattan Distance)**
- Reduces unnecessary exploration
- More efficient than BFS in grid navigation

---

## ⚡ Performance Insight

📉 Achieved approximately **60% reduction in node exploration** using A* compared to BFS  

---

## 🛠️ Tech Stack

- **Python**
- **Pygame**
- **Data Structures & Algorithms**
  - BFS (Queue - `deque`)
  - A* (Priority Queue - `heapq`)

---



---

## ▶️ How to Run

```bash
pip install pygame
python game.py
