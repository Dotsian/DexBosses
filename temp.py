import math
import random
import time
from dataclasses import dataclass
from enum import Enum


class BattleState(Enum):
    NEUTRAL = 0
    ATTACKING = 1
    DEFENDING = 2


@dataclass
class Boss:
    max_health: int
    
    state: BattleState = BattleState.NEUTRAL
    
    damage_taken: int = 0
    
    @property
    def health(self) -> int:
        return math.ceil(self.max_health - self.damage_taken)
        
active_boss = Boss(30)

def loop():
    if random.randint(1, 2) == 1:
        active_boss.state = BattleState.ATTACKING
        print("The boss is getting ready to attack")
    else:
        active_boss.state = BattleState.DEFENDING
        print("The boss is getting ready to defend")
    
    answer = input("Action: ")
    
    match answer:
        case "attack":
            active_boss.damage_taken += 15
            print(
                "You dealt 15 damage to the boss "
                f"({active_boss.health}/{active_boss.max_health})"
            )
            
    if active_boss.health <= 0:
        print("You have defeated the boss!")
        return
            
    time.sleep(1)
            
    if active_boss.state == BattleState.ATTACKING:
        print("The boss has struck you, dealing X damage")
        
    loop()
    
loop()
