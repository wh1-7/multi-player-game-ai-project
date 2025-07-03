import random
from agents.base_agent import BaseAgent
 
class RandomBot(BaseAgent):
    def get_action(self, observation, env):
        valid_actions = env.get_valid_actions()
        return random.choice(valid_actions) 
    def update_stats(self , result:str , flag:int):
        if not hasattr(self, 'stats'): 
            self.stats = {'wins': 0, 'losses': 0, 'draws': 0}
        if result == 'win':
            self.stats['wins'] += 1
        elif result == 'lose':
            self.stats['losses'] += 1
        elif result == 'draw':
            self.stats['draws'] += 1
        
        print(f"{self.name} 统计更新: {self.stats}")  