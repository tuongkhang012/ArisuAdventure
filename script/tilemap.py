import pygame, json

AUTOTILE_MAP = {
    tuple(sorted([(1,0), (0,1)])): 0, #IF HAS NEIGHBOR TO THE RIGHT AND BOTTOM, USE VARIANT=0 TILE
    tuple(sorted([(1,0), (0,1), (-1, 0)])): 1, #IF HAS NEIGHBOR TO THE RIGHT, BOTTOM AND LEFT, USE VARIANT=1 TILE
    tuple(sorted([(-1,0), (0,1)])): 2, #LEFT, BOTTOM
    tuple(sorted([(-1,0), (0,-1), (0,1)])): 3, #LEFT, TOP, BOTTOM
    tuple(sorted([(-1,0), (0,-1)])): 4, #LEFT, TOP
    tuple(sorted([(-1,0), (0,-1), (1,0)])): 5, #LEFT, TOP, RIGHT
    tuple(sorted([(1,0), (0,-1)])): 6, #RIGHT, TOP
    tuple(sorted([(1,0), (0,-1), (0,1)])): 7, #RIGHT, TOP, BOTTOM
    tuple(sorted([(1,0), (-1,0), (0,1), (0,-1)])): 8, #LEFT, RIGHT, TOP, BOTTOM
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
NEIGHBOR_OFFSETS_PLAYER = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
AUTOTILE_TYPES = {'overworld'}
PHYSICS_TILES = {'overworld'}

class Tilemap:
    def __init__(self, gameManager, tile_size=32):
        self.gameManager = gameManager
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

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

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1,0), (-1,0), (0,-1), (0,1)]:
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