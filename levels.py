# Niveis que serão usados no jogo
# 0 espaço vazio
# 1 blocos normais (madeira)
# 2 blocos verdes (objetivos a coletar)
# 3 blocos vermelhos (pontos extras)

LEVEL = [
(0,
 2,
 0,
 ["L","J","I","J"],
 [[0, 1, 0, 0, 0, 0, 0, 1],
  [0, 1, 0, 0, 0, 0, 0, 1],
  [0, 2, 0, 0, 0, 0, 0, 2],
  [0, 1, 0, 0, 0, 0, 0, 1],
  [0, 1, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0]]),

(1,  # Nível 1 - Coletar 5 pedras verdes
 5, # Número de pedras verdes a coletar
 0, # Número de pedras vermelhas
 ["left_down_corner", "right_down_corner", "left_up_corner", "right_up_corner", "I","I_H", "L", "J", "L", "J", "I", "T_INVERTIDO"],
 [[0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 1, 1, 1, 1, 2, 0],
  [0, 1, 0, 0, 0, 0, 1, 0],
  [0, 1, 0, 2, 2, 0, 1, 0],
  [0, 1, 0, 2, 2, 0, 1, 0],
  [0, 1, 0, 0, 0, 0, 1, 0],
  [0, 2, 1, 1, 1, 1, 2, 0],
  [0, 0, 0, 0, 0, 0, 0, 0]]),

  ( 2,  # Nível 2 - Coletar 5 pedras verdes
    5,
    2,
    ["left_down_corner", "right_down_corner", "left_up_corner", "right_up_corner", "I","I_H", "L", "J", "L", "J", "I", "T_INVERTIDO"],
    [[2, 2, 0, 0, 0, 0, 1, 1],
     [2, 0, 0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 3, 3, 0, 0, 0],
     [0, 0, 0, 3, 3, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 2],
     [1, 1, 0, 0, 0, 0, 2, 2],])

]
