"""
MCTS Bot
使用蒙特卡洛树搜索算法
"""

import time
import random
import math
from typing import Dict, List, Tuple, Any, Optional
from agents.base_agent import BaseAgent
import config
import copy


class MCTSNode:
    """MCTS节点"""
    
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions = self._get_untried_actions()
    
    def _get_untried_actions(self):
        """获取未尝试的动作"""
        if hasattr(self.state, 'get_valid_actions'):
            return self.state.get_valid_actions()
        return []
    
    def is_fully_expanded(self):
        """检查是否完全展开"""
        return len(self.untried_actions) == 0
    
    def is_terminal(self):
        """检查是否为终止节点"""
        if hasattr(self.state, 'is_terminal'):
            return self.state.is_terminal()
        return False
    
    def get_winner(self):
        """获取获胜者"""
        if hasattr(self.state, 'get_winner'):
            return self.state.get_winner()
        return None
    
    def clone_state(self):
        """克隆状态"""
        if hasattr(self.state, 'clone'):
            return self.state.clone()
        return self.state


class MCTSBot(BaseAgent):
    """MCTS Bot"""
    
    def __init__(self, name: str = "MCTSBot", player_id: int = 1, 
                 simulation_count: int = 100):
        super().__init__(name, player_id)
        self.simulation_count = simulation_count
        
        # 从配置获取参数
        ai_config = config.AI_CONFIGS.get('mcts', {})
        self.simulation_count = ai_config.get('simulation_count', simulation_count)
        self.timeout = ai_config.get('timeout', 10)
    
    def get_action(self, observation: Any, env: Any) -> Any:
        """
        使用MCTS选择动作
        
        Args:
            observation: 当前观察
            env: 环境对象
            
        Returns:
            选择的动作
        """
        start_time = time.time()
        
        # 获取有效动作
        valid_actions = env.get_valid_actions()
        
        if not valid_actions:
            return None
        
        best_action = valid_actions[0]
        best_score = -float('inf')
        
        simulations_per_action = max(1, self.simulation_count // len(valid_actions))
        
        for action in valid_actions:
            score = 0
            for _ in range(simulations_per_action):
                score += self.simulate(env.game.clone(), action)
            avg_score = score / simulations_per_action
            
            if avg_score > best_score:
                best_score = avg_score
                best_action = action
        
        # 更新统计
        move_time = time.time() - start_time
        self.total_moves += 1
        self.total_time += move_time
        
        return best_action
    
    def simulate(self, game, first_action):
        # 执行第一个动作
        game.step(first_action)
        
        # 随机模拟到游戏结束
        while not game.is_terminal():
            valid_actions = game.get_valid_actions()
            if not valid_actions:
                break
            action = random.choice(valid_actions)
            game.step(action)
        
        # 返回结果评分
        winner = game.get_winner()
        if winner == self.player_id:
            return 1
        elif winner is not None:
            return -1
        else:
            return 0
    
    def reset(self):
        """重置MCTS Bot"""
        super().reset()
    
    def get_info(self) -> Dict[str, Any]:
        """获取MCTS Bot信息"""
        info = super().get_info()
        info.update({
            'type': 'MCTS',
            'description': '使用蒙特卡洛树搜索的Bot',
            'strategy': f'MCTS with {self.simulation_count} simulations',
            'timeout': self.timeout
        })
        return info 