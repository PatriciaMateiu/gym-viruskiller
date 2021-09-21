from gym.envs.registration import register
 
register(id='VirusKiller-v0', 
    entry_point='gym_viruskiller.envs:VirusKillerEnv', 
)