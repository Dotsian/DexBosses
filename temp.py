import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum


class BattleState(Enum):
    NEUTRAL = ""
    ATTACKING = "attack"
    DEFENDING = "defend"


@dataclass
class BattleBall:
    country: str
    player: str
    
    max_health: int
    damage: int
    
    state: BattleState = BattleState.NEUTRAL
    resistance: int = 1
    damage_taken: int = 0
    
    @property
    def info(self) -> str:
        return f"{self.player}'s {self.country}"
    
    @property
    def health(self) -> int:
        return math.ceil(self.max_health - self.damage_taken)
        
    @property
    def dead(self) -> bool:
        return self.health <= 0
    

@dataclass
class Boss:
    max_health: int
    damage: int
    
    state: BattleState = BattleState.NEUTRAL
    
    resistance: int = 1
    damage_taken: int = 0
    
    @property
    def health(self) -> int:
        return math.ceil(self.max_health - self.damage_taken)
        
        
@dataclass
class BattleInstance:
    boss: Boss | None = None
    balls: list = field(default_factory=list)
    turns: int = 0


def start_battle(battle: BattleInstance):
    targeting_ball = random.choice(battle.balls)
    
    battle.boss.state = random.choice(
        [BattleState.ATTACKING, BattleState.DEFENDING]
    )
    
    yield f"The boss is getting ready to {battle.boss.state.value}"
    
    battle.boss.resistance = (
        2 if battle.boss.state == BattleState.DEFENDING else 1
    )

    answer = input("> Attack or Defend: ")
    
    match answer:
        case "attack":
            absolute = random.randint(1, targeting_ball.damage)
            damage = round(absolute / battle.boss.resistance)
            
            battle.boss.damage_taken += damage
            
            yield (
                f"You dealt {damage} damage to the boss "
                f"({battle.boss.health}/{battle.boss.max_health})"
            )
        
        case "defend":
            yield "You increased your resistance by two"
            
            targeting_ball.resistance += 2
            
    if battle.boss.health <= 0:
        yield f"{targeting_ball.info} has defeated the boss!"
        return
            
    time.sleep(0.5)
            
    if battle.boss.state == BattleState.ATTACKING:
        absolute = random.randint(1, battle.boss.damage)
        damage = round(absolute / targeting_ball.resistance)
        
        targeting_ball.damage_taken += damage
        targeting_ball.resistance = 1
        
        yield (
            f"The boss has dealt {damage} damage to "
            f"{targeting_ball.info} "
            f"({targeting_ball.health}/{targeting_ball.max_health})"
        )
        
        if targeting_ball.dead:
            yield f"{targeting_ball.info} died"
        
    for item in start_battle(battle):
        print(item)
    
if __name__ == "__main__":
    battle = BattleInstance(
        Boss(150000, 500),
        [
            BattleBall("Testing", "test", 5000, 500),
        ],
    )
    
    for item in start_battle(battle):
        print(item)
