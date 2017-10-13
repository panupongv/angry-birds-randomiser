import pygame
import sys
import random

class RandomApp:
    def __init__(self):
        pygame.init()

        self.screen_width = 960
        self.screen_height = 600
        
        self.window = pygame.display.set_mode([960, 600])
        pygame.display.set_caption("Sport Day 2017")
        self.clock = pygame.time.Clock()

        self.birds = [pygame.image.load("red.png"), pygame.image.load("black.png"),
                      pygame.image.load("blue.png"), pygame.image.load("green.png"),
                      pygame.image.load("blank.png")]
        self.quick_image = [pygame.image.load("notquick.png"), pygame.image.load("quick.png")]
        self.background = pygame.image.load("zbg.png")

        self.font = pygame.font.Font("font.ttf", 40)

        self.name = ""
        self.quick_mode = False
        self.in_queue = False
        
        self.delay = 0
        self.current_delay = 0
        self.result = 0
        self.randomed = 0

        self.bird_index = 4

        self.name_list = [[], [], [], []]

        self.center_x = self.screen_width / 2
        self.center_y = self.screen_height / 2
        self.bird_x = self.screen_width * 2 / 3
        self.text_x = self.screen_width / 5
        self.text_y = self.center_y - 30
        self.BIRD_NUM = 4
        self.MAX_DELAY = 18

    def run(self):
        while True:
            self.keyboard_input()
            self.draw_components()
            self.decrement()
            self.clock.tick(60)

    def draw_components(self):
        self.window.blit(self.background, [0, 0])
        current_bird = self.birds[self.bird_index]
        self.window.blit(current_bird,
                         [self.bird_x - (current_bird.get_rect().width/2),
                          self.center_y - (current_bird.get_rect().height/2)])
        rendered = self.font.render(self.name, True, [0, 0, 0])
        self.window.blit(rendered, [self.text_x - (rendered.get_rect().width / 2),
                                    self.text_y])
        self.window.blit(self.quick_image[self.quick_mode], [0, 0])
        pygame.display.update()

    def keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.write_file()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.name != "":
                        self.start_random()
                else:
                    self.process_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.in_queue:
                    continue
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x < self.quick_image[0].get_rect().width \
                   and mouse_y < self.quick_image[0].get_rect().height:
                    self.quick_mode = not self.quick_mode

    def start_random(self):
        if self.in_queue:
            return
        if self.randomed == 2:
            randomed_index = self.min_index()
            self.randomed = 0
        else:
            randomed_index = random.randrange(self.BIRD_NUM)
        if self.quick_mode:
            self.bird_index = randomed_index
            self.add_name()
        else:        
            self.result = randomed_index
            self.delay = 1
            self.current_delay = self.delay
            self.in_queue = True

    def decrement(self):
        if not self.in_queue:
            return
        if self.current_delay <= 0:
            if self.delay < self.MAX_DELAY:
                self.delay *= 1.1
            self.bird_index += 1
            self.bird_index %= self.BIRD_NUM
            self.current_delay = self.delay
        if self.delay >= self.MAX_DELAY and self.bird_index == self.result:
            self.add_name()
            self.in_queue = False
            

        self.current_delay -= 1

    def process_key(self, key):
        if self.in_queue:
            return
        if key == 8:
            self.name = self.name[:-1]
        elif chr(key).isalpha():
            self.name += chr(key)

    def add_name(self):
        self.name_list[self.bird_index].append(self.name)
        self.name = ""
        self.randomed += 1

    def max_index(self):
        max_ind = 0
        max_len = len(self.name_list[0])
        for i in range(1, self.BIRD_NUM):
            if len(self.name_list[i]) > max_len:
                max_len = len(self.name_list[i])
                max_ind = i
        return max_ind

    def min_index(self):
        min_ind = 0
        min_len = len(self.name_list[0])
        for i in range(1, self.BIRD_NUM):
            if len(self.name_list[i]) < min_len:
                min_len = len(self.name_list[i])
                min_ind = i
        return min_ind

    def write_file(self):
        out_file = open("name_list.txt", mode = "w")
        max_len = len(self.name_list[self.max_index()])
        out_file.write(format("RED|", ">10s") + format("BLACK|", ">10s") \
                       + format("BLUE|", ">10s") + format("GREEN|", ">10s") + "\n")
        out_file.write("-" * 40 + "\n")
        for i in range(max_len):
            for j in range(self.BIRD_NUM):
                if i >= len(self.name_list[j]):
                    out_file.write(" " * 9)
                    out_file.write("|")
                else:
                    out_file.write(format(self.name_list[j][i]  + "|", ">10s"))
            out_file.write("\n")
        out_file.close()
    
RandomApp().run()
