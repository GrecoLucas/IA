# Niveis que serão usados no jogo
# 0 espaço vazio
# 1 blocos normais (madeira)
# 2 blocos verdes (objetivos a coletar)
# 3 blocos vermelhos (pontos extras)

LEVEL = [
("1",  # Nível 1 - Coletar 5 pedras verdes
 5, # Número de pedras verdes a coletar
 0, # Número de pedras vermelhas
 ["I", "L", "J", "Z", "S", "O", "T_INVERTIDO"],
 [[0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 1, 1, 1, 1, 2, 0],
  [0, 1, 0, 0, 0, 0, 1, 0],
  [0, 1, 0, 2, 2, 0, 1, 0],
  [0, 1, 0, 2, 2, 0, 1, 0],
  [0, 1, 0, 0, 0, 0, 1, 0],
  [0, 2, 1, 1, 1, 1, 2, 0],
  [0, 0, 0, 0, 0, 0, 0, 0]]),

# Adicione mais níveis conforme necessário
# ("2",
#  [[...]])
]
