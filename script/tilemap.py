import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
NEIGHBOR_OFFSETS_PLAYER = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
PHYSICS_TILES = {'overworld'}

class Tilemap:
    def __init__(self, gameManager, tile_size=32):
        self.gameManager = gameManager
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3+i) + ";8"] = {'type': 'overworld', 'variant': 1, 'pos': (3+i, 8)}
            self.tilemap["13;" + str(2+i)] = {'type': 'overworld', 'variant': 10, 'pos': (13, 2+i)}

    # Check for colliding tiles around a position
    def tiles_around(self, pos, player=False):
        tiles = []
        # From pixel coordinates to grid coordinates
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        if player:
            offsets = NEIGHBOR_OFFSETS_PLAYER
        else:
            offsets = NEIGHBOR_OFFSETS

        for offset in offsets:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])

            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos, player=False):
        rects = []
        for tile in self.tiles_around(pos, player):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size,
                                         tile['pos'][1] * self.tile_size,
                                         self.tile_size, self.tile_size))
        return rects


    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.gameManager.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.gameManager.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))