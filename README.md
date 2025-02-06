# Carlos Ruiz García-Casarrubios - Proyecto de Búsqueda en Sokoban

Este proyecto implementa un sistema de búsqueda para resolver niveles del juego Sokoban. Utiliza diferentes estrategias de búsqueda, como BFS (Búsqueda en Anchura), DFS (Búsqueda en Profundidad), UC (Costo Uniforme), A* y GREEDY, para encontrar soluciones óptimas o subóptimas a los niveles del juego.

## Estructura del Proyecto

El proyecto está organizado en los siguientes archivos principales:

- **sokoban.py**: Contiene la clase `Sokoban`, que es la clase principal del proyecto. Esta clase se encarga de gestionar el nivel del juego, incluyendo la inicialización del nivel, la generación de sucesores, la ejecución de diferentes acciones (T1, T2S, T2T, T3), y la implementación del algoritmo de búsqueda.
- **visited_states.py**: Contiene la clase `VisitedStates`, que se utiliza para rastrear los estados visitados durante el proceso de búsqueda.
- **frontier.py**: Implementa la clase `Frontier`, que gestiona una cola de prioridad para los nodos en el proceso de búsqueda.
- **node.py**: Define la clase `Node`, que representa un nodo en el árbol de búsqueda, con atributos como el ID del nodo, el ID del estado, el costo, la heurística, y más.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado:

- **Python 3.8 o superior**.

## Instalación

1. Asegúrate de tener Python instalado. Puedes verificar la instalación ejecutando:

   ```bash
   python --version
