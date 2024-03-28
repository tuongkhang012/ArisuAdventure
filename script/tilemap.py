import pygame, json

# (0,-1): T
# (-1,0): L
# (1,0): R
# (0,1): B
AUTOTILE_MAP = {
    # R, B
    tuple(sorted([(0, 1), (1, 0)])): 0,
    # L, R, B
    tuple(sorted([(-1, 0), (1, 0), (0, 1)])): 1,
    # L, B
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    # T, R, B
    tuple(sorted([(0, -1), (1, 0), (0, 1)])): 3,
    # L, R, T, B
    tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)])): 4,
    # T, L, B
    tuple(sorted([(0, -1), (-1, 0), (0, 1)])): 5,
    # T, R
    tuple(sorted([(0, -1), (1, 0)])): 6,
    # L, T, R
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 7,
    # L, T
    tuple(sorted([(-1, 0), (0, -1)])): 8,
    # R
    tuple(sorted([(1, 0)])): 9,
    # L, R
    tuple(sorted([(-1, 0), (1, 0)])): 10,
    # L
    tuple(sorted([(-1, 0)])): 11,
    # B
    tuple(sorted([(0, 1)])): 12,
    # T, B
    tuple(sorted([(0, -1), (0, 1)])): 13,
    # T
    tuple(sorted([(0, -1)])): 14,
    # None
    tuple(sorted([])): 15

}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
NEIGHBOR_OFFSETS_PLAYER = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2),
                           (0, 2), (1, 2)]
AUTOTILE_TYPES = {'chamber'}
PHYSICS_TILES = {'chamber', 'stairs'}


class Tilemap:
    def __init__(self, gameManager, tile_size=32):
        self.gameManager = gameManager
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    # BINDING OBJECT WITH PARTICLES
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile)
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

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
                rects.append((pygame.Rect(tile['pos'][0] * self.tile_size,
                                          tile['pos'][1] * self.tile_size,
                                          self.tile_size, self.tile_size), tile['behaviour']))
        return rects

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ";" + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ";" + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.gameManager.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.gameManager.assets[tile['type']][tile['variant']],
                              (tile['pos'][0] * self.tile_size - offset[0],
                               tile['pos'][1] * self.tile_size - offset[1]))
