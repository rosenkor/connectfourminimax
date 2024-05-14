from .helper_functions import *


def switch_player(player):
     player = "y" if player == "r" else "r"
     return player


def true_mn(player, original_player, state, nodes_examined, depth, max_depth, maximizing = False):
     nodes_examined = nodes_examined + 1
     if UTILITY(state):
          return UTILITY(state), nodes_examined

     if depth == 0:
          return EVALUATION(state, original_player),nodes_examined
     
     
     value = -float('inf') if maximizing else float('inf')


     values_array = [None] * 7

     for c in range(7):
          for r in (range(6)):
               if state[r][c] == '.':
                    if not check_full(state):
                         new_state = simulate_move(state, r, c, player)
                         if maximizing == True:
                              valueA, nodes_examined = true_mn(switch_player(player), original_player, new_state, nodes_examined, depth - 1, max_depth, False)
                         else:
                              valueA, nodes_examined = true_mn(switch_player(player), original_player, new_state ,nodes_examined, depth - 1, max_depth, True)
                         values_array[c] = valueA
                         if maximizing == True:
                              value = max(value, valueA) 
                         else:
                              value = min(value, valueA)
               break

     if depth == max_depth:
          best_move = max(range(7), key=lambda c: values_array[c] if values_array[c] is not None else None)
          return best_move, nodes_examined
     
     return value, nodes_examined
     

def true_ab_pruning(player, original_player, state, nodes_examined, max_depth, depth, alpha, beta, maximizing = True):
     nodes_examined = nodes_examined + 1
     if UTILITY(state):
          return UTILITY(state), nodes_examined

     if depth == 0:
          return EVALUATION(state, original_player),nodes_examined
     
     values_array = []

     value = -float('inf') if maximizing else float('inf')

     for c in range(7):
          for r in (range(6)):
               if state[r][c] == '.':
                    if not check_full(state):
                         new_state = simulate_move(state, r, c, player)
                         if maximizing == True:
                              if alpha < beta:
                                   valueA, nodes_examined = true_ab_pruning(switch_player(player), original_player, new_state, nodes_examined, max_depth, depth -1, alpha, beta, False)
                                   values_array.append(valueA)
                              value = max(value, valueA)
                              if alpha >= beta:
                                   return value, nodes_examined
                              alpha = max(value, alpha)
                         else:
                              if alpha < beta:
                                   valueA, nodes_examined = true_ab_pruning(switch_player(player), original_player, new_state ,nodes_examined, max_depth, depth -1, alpha, beta, True)
                                   values_array.append(valueA)
                              value = min(value, valueA)
                              if alpha >= value:
                                   return value, nodes_examined
                              beta = min(value, beta)
                    break
     if depth == max_depth:
          return values_array.index(value), nodes_examined
     
     return value, nodes_examined
