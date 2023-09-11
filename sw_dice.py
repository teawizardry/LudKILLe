import numpy as np

# Values
SUCCESS = "Success"
FAILURE = "Failure"
ADVANTAGE = "Advantage"
THREAT = "Threat"
TRIUMP = "Triump"
DESPAIR = "Despair"
BLANK = "Blank"
DARK = "Dark"
LIGHT = "Light"

# Ability
ability =  [[SUCCESS, ADVANTAGE], [ADVANTAGE, SUCCESS], [SUCCESS, SUCCESS], [ADVANTAGE], [SUCCESS], [ADVANTAGE, ADVANTAGE], [BLANK]]

# Proficiency
proficiency = [[ADVANTAGE, ADVANTAGE], [ADVANTAGE], [ADVANTAGE, ADVANTAGE], [TRIUMP], [SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS, SUCCESS], [SUCCESS, ADVANTAGE], [SUCCESS, SUCCESS], [BLANK]]

# Boost
boost = [[ADVANTAGE], [SUCCESS, ADVANTAGE], [ADVANTAGE, ADVANTAGE], [SUCCESS], [BLANK], [BLANK]]

# Difficulty
difficulty = [[THREAT], [FAILURE], [THREAT, FAILURE], [THREAT], [BLANK], [THREAT, THREAT], [FAILURE, FAILURE], [THREAT]]

# Challenge
challenge = [[THREAT, THREAT], [THREAT], [THREAT, THREAT], [THREAT], [THREAT, FAILURE], [FAILURE], [THREAT, FAILURE], [FAILURE], [FAILURE, FAILURE], [DESPAIR], [FAILURE, FAILURE], [BLANK]]

# Setback
setback = [[FAILURE], [FAILURE], [THREAT], [THREAT], [BLANK], [BLANK]]

# Force
force = [[DARK], [DARK], [DARK], [DARK], [DARK], [DARK], [DARK, DARK], [LIGHT], [LIGHT], [LIGHT, LIGHT], [LIGHT, LIGHT], [LIGHT, LIGHT]]

rng = np.random.default_rng()

def sw_roll(dice):
    roll = rng.integers(len(dice))
    return dice[roll]