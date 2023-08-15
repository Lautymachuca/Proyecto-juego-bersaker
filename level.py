import pygame 
from tile import tile
from settings import tile_size, screen_width
from player import Player

class level:
    def __init__(self,level_data,surface):
        # configuracion del nivel
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self,layout): 
    
        self.tiles =pygame.sprite.Group() 
        self.player =pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                    
                if cell == 'X':
                    tiles = tile((x ,y),tile_size)
                    self.tiles.add(tiles)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player((x ,y))
                    self.player.add(player_sprite)
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x


        if player_x < screen_width / 2 and direction_x < 0 :
            self.world_shift = 8 
            player.speed = 0  
        elif player_x > screen_width - (screen_width / 2) and direction_x > 0 :
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite

        player.rect.x += player.direction.x * player.speed  

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = player.rect.left
        
    def vertical_movement_colision(self):
        player = self.player.sprite
        player.apply_gravity()
            
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = player.rect.bottom
                    player.direction.y = 0
    
    def run(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.scroll_x()
        self.tiles.draw(self.display_surface)
        # player 
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_colision()
        self.player.draw(self.display_surface)
