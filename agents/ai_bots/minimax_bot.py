from agents.base_agent import BaseAgent
import copy

class MinimaxBot(BaseAgent):
    def __init__(self, name="MinimaxBot", player_id=1, max_depth=2):
        super().__init__(name, player_id)
        self.max_depth = max_depth

    def get_action(self, observation, env):
        valid_actions = env.get_valid_actions()
        if not valid_actions:
            return None
            
        best_score = float('-inf')
        best_action = valid_actions[0]
        
        for action in valid_actions:
            # 克隆游戏状态
            game_copy = env.game.clone()
            # 执行动作
            game_copy.step(action)
            # 计算分数
            score = self.minimax(game_copy, self.max_depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action

    def minimax(self, game, depth, maximizing):
        if depth == 0 or game.is_terminal():
            winner = game.get_winner()
            if winner == self.player_id:
                return 1
            elif winner is not None:
                return -1
            else:
                return 0
        
        valid_actions = game.get_valid_actions()
        if not valid_actions:
            return 0
            
        if maximizing:
            max_score = float('-inf')
            for action in valid_actions:
                game_copy = game.clone()
                game_copy.step(action)
                score = self.minimax(game_copy, depth - 1, False)
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for action in valid_actions:
                game_copy = game.clone()
                game_copy.step(action)
                score = self.minimax(game_copy, depth - 1, True)
                min_score = min(min_score, score)
            return min_score 