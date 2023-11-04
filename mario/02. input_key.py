import retro
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()
print(ram[0x03AD])

for i in range(20):
    # B, NULL, SELECT, START, U, D, L, R, A
    env.step(np.array([0, 0, 0, 0, 0, 0, 0, 1, 0]))

ram = env.get_ram()
print(ram[0x03AD])
