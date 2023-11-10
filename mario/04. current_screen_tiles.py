import retro
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()

full_screen_tiles = ram[0x0500:0x069F + 1]
full_screen_tile_count = full_screen_tiles.shape[0]

full_screen_page1_tiles = full_screen_tiles[:full_screen_tile_count // 2].reshape((-1, 16))
full_screen_page2_tiles = full_screen_tiles[full_screen_tile_count // 2:].reshape((-1, 16))

full_screen_tiles = np.concatenate((full_screen_page1_tiles, full_screen_page2_tiles), axis=1).astype(np.int)

print(full_screen_tiles)

current_screen_in_level = ram[0x071A]
screen_x_position_in_level = ram[0x071C]
screen_x_position_offset = (256 * current_screen_in_level + screen_x_position_in_level) % 512
sx = screen_x_position_offset // 16

screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, sx:sx + 16]

print(screen_tiles)
