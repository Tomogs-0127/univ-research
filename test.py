import numpy as np
import random
import collections
""" methods=[]
def my_last_action(observation):
  times=observation.step
  opp_last_action=observation.lastOpponentAction
  return opp_last_action



def plus(observation):
  my_plus_strategy=(observation.lastOpponentAction+1) % 3
  return my_plus_strategy

def minus(observation):
  my_minus_strategy=(observation.lastOpponentAction-1) % 3
  return my_minus_strategy

def initial_strategy(observation):
  times=observation.step
  if times % 2 ==1:
    return minus(observation)
  else:
    return plus(observation)
 """


def markov_agent(observation, configuration):
  k = 2
  #global table, action_seq
  if observation.step % 250 == 0: # refresh table every 250 steps
      action_seq, table = [], collections.defaultdict(lambda: [1, 1, 1])
  if len(action_seq) <= 2 * k + 1:
      action = int(np.random.randint(3))
      if observation.step > 0:
          action_seq.extend([observation.lastOpponentAction, action])
      else:
          action_seq.append(action)
      return action
  # update table
  key = ''.join([str(a) for a in action_seq[:-1]])
  table[key][observation.lastOpponentAction] += 1
  # update action seq
  action_seq[:-2] = action_seq[2:]
  action_seq[-2] = observation.lastOpponentAction
  # predict opponent next move
  key = ''.join([str(a) for a in action_seq[:-1]])
  if observation.step < 500:
      next_opponent_action_pred = np.argmax(table[key])
  else:
      scores = np.array(table[key])
      next_opponent_action_pred = np.random.choice(3, p=scores/scores.sum()) # add stochasticity for second part of the game
  # make an action
  action = (next_opponent_action_pred + 1) % 3
  # if high probability to lose -> let's surprise our opponent with sudden change of our strategy
  if observation.step > 900:
      action = next_opponent_action_pred
  action_seq[-1] = action
  return int(action)




def copy_opponent_agent(observation, configuration):
  if observation.step > 0:
    try:
      return markov_agent(observation,configuration)
    except:
      return observation.lastOpponentAction
  else:
    return random.randint(0,2)

