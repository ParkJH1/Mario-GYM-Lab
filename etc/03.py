import retro

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()
print(ram)
print(type(ram))
print(ram.shape)

print(ram[0x001D])
print(ram[29])

print(int(0x500))
print(int(0x69f))
print(int(0x69f) - int(0x500) + 1)

print(13 * 16)