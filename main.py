import pygame as pg
import sys

import requests

sys.path.append('data')
import sys
from data.settings import *
from data.objects import *
from math import *
from os import path
from mpmath import *
from random import randint
import pyperclip
from os import path





class Game:
    def __init__(self):
        #os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (300,200)
        pg.init()
        self.screen_width=1024
        self.screen_height=768
        self.tilesize=32
        self.number_of_tiles_width=self.screen_width/self.tilesize
        self.number_of_tiles_height=self.screen_height/self.tilesize
        self.monitor_size=[pg.display.Info().current_w,pg.display.Info().current_h]
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height),pg.RESIZABLE)
        self.screen_calc = pg.display.set_mode((self.screen_width, self.screen_height),pg.RESIZABLE)
        self.surf=pg.Surface((self.screen_width,self.screen_height))
        self.surf_rect=self.surf.get_rect()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.graph_color_dict={}
        self.dict_of_points={}
        self.function_input=False
        self.color_input_text=False
        self.captured_text=''
        self.input=Input(self,(0,self.screen_height))
        self.color_input=ColorInput(self,(self.input.rect.width+self.input.rect.width//4,self.screen_height))
        self.draw_points=False
        self.draw_legend=False
        self.legend=Legend(self,(self.screen_width,self.screen_height),self.graph_color_dict)
        self.full_screen=False
        self.scrollbar_bottom=ScrollBarBottom(self,(0,self.screen_height+25))
        self.scrollbar_right=ScrollBarRight(self,(self.screen_width+25,self.screen_height))
        self.widgets=[self.input,self.color_input,self.legend]
        self.draw_scroll_bar=False
        self.number1=self.surf_rect.width
        self.number2=self.surf_rect.height
        self.pointer=ToFollowMouse(self)
        self.screen_rect=self.screen.get_rect()
        self.point_to_ckeck=vec(0,0)
        self.calc_button=ButtonToTheCalculator(self)
        self.culc_screen=CalculatorScreen(self)
        self.list_of_calc_buttons=[]
        self.prev_size_for_a_ratio=[]
        self.new_size_for_a_ratio=[]
        self.list_of_button_values=['g','rad','sin','cos','tan','^','lg','deg','(',')','sqrt','C','<','%','/','x!','7','8','9','*','1/x','4','5',"6",'-','pi','1','2','3','+',',','e','0','.','=']
        self.dict_of_buttons={}
        self.screen_rect_calc=self.screen_calc.get_rect()
        self.previous_size_calc=[0,0]
        self.previous_size_graph=[0,0]
        self.rad_deg_input=Degree_Radians_Input(self,(self.color_input.rect.width*2+self.color_input.rect.width//2,self.screen_height))
        self.draw_rad_deg_input=False
        self.button_qe=ButtonToTheQE(self)
        self.qe_template=Template(self)
        self.run_qe=False
        self.grapher_button=Grapher_button(self)
        self.previous_size_qe=[self.qe_template.rect.width,self.qe_template.rect.height]
        self.field_1=FieldFollower(self,(self.qe_template.rect.width*0.25,self.qe_template.rect.height//2))
        self.field_1.active=True
        self.field_2=FieldFollower(self,(self.qe_template.rect.width*0.45,self.qe_template.rect.height//2))
        self.field_3=FieldFollower(self,(self.qe_template.rect.width*0.65,self.qe_template.rect.height//2))
        self.dict_of_fields={self.field_1:self.field_1.active,self.field_2:self.field_2.active,self.field_3:self.field_3.active}
        self.prev_size_for_a_ratio_qe=[]
        self.new_size_for_a_ratio_qe=[self.qe_template.rect.width,self.qe_template.rect.height]
        self.rect_of_xpt=self.field_1.rect
        self.rect_of_x=self.field_2.rect
        self.result_eq=[]
        self.previous_e=[]
        self.rect_of_zero=self.qe_template.rect
        self.scrollbar_qe=ScrollBarBottomQE(self,(0,self.qe_template.rect.bottom))
        self.rect_eq=self.qe_template.rect
        self.rect_x1=self.qe_template.rect
        self.rect_x2=self.qe_template.rect
        self.list_of_rects_to_check=[self.rect_x1,self.rect_x2,self.rect_eq,self.rect_of_zero]

    def apply_rect(self, rect):
        return rect.move([i*-1 for i in self.surf_rect.topleft])

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect


    def draw_text_surf(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.surf.blit(text_surface, text_rect)
        return text_rect


    def draw_text_surf_change(self, text, font_name, size, color, x, y,surf, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)
        return text_rect

    def load_data(self):
        self.game_folder = path.join('data')
        self.font=path.join(self.game_folder, 'ARIALI 1.TTF')
        self.calc_font=path.join(self.game_folder, 'New Athletic M54.ttf')
        self.calc_button_img=pg.image.load(path.join(self.game_folder, 'calculator_button.png')).convert_alpha()
        self.calc_button_img2=pg.image.load(path.join(self.game_folder, 'calculator_button2.png')).convert_alpha()
        self.calc_background=pg.image.load(path.join(self.game_folder, 'calculatorbackbround.png')).convert_alpha()
        self.calc_screen_image=pg.image.load(path.join(self.game_folder, 'calculator_screen.png')).convert_alpha()
        self.calc_on_button_img=pg.image.load(path.join(self.game_folder, 'button_on_calc.png')).convert_alpha()
        self.calc_on_button_img2=pg.image.load(path.join(self.game_folder, 'button_on_calc1.png')).convert_alpha()
        self.calc_on_button_img_orange=pg.image.load(path.join(self.game_folder, 'button_on_calc_orange.png')).convert_alpha()
        self.calc_on_button_img_orange1=pg.image.load(path.join(self.game_folder, 'button_on_calc_orange1.png')).convert_alpha()
        self.grapher_button_img=pg.image.load(path.join(self.game_folder, 'grapher_button.png')).convert_alpha()
        self.grapher_button_img1=pg.image.load(path.join(self.game_folder, 'grapher_button1.png')).convert_alpha()
        self.grapher_button_img2=pg.image.load(path.join(self.game_folder, 'grapher_button2.png')).convert_alpha()
        self.qe_button_img=pg.image.load(path.join(self.game_folder, 'quadratic_equation_button.png')).convert_alpha()
        self.qe_button_img1=pg.image.load(path.join(self.game_folder, 'quadratic_equation_button1.png')).convert_alpha()




    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.run_calc=False
        self.run_graph=True
        while self.playing:
            if self.run_graph:
                #self.dt = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()
            elif self.run_calc:
                self.events_calc()
                self.update_calc()
                self.draw_calc()
            elif self.run_qe:
                self.events_qe()
                self.update_qe()
                self.draw_qe()

    def quit(self):
        pg.quit()
        sys.exit()



    def renew_graphs(self):
        tiles_width=self.surf_rect.width//self.tilesize
        tiles_height=self.surf_rect.height//self.tilesize
        if self.dict_of_points:
            for fn in self.dict_of_points.keys():
                    for point in self.dict_of_points[fn]:
                        point.kill()
                    list_of_points=[]
                    if 'log' in fn or 'sqrt' in fn :
                        starting_point=1
                    elif 'tan' in fn:
                        starting_point=-tiles_width*self.tilesize
                    elif 'exp' in fn:
                        starting_point=-tiles_width//2*self.tilesize
                    # elif 'asin' in fn or 'acos' in fn:
                    #     starting_point=-1

                    else:
                        starting_point=-tiles_width*self.tilesize
                    for x in range(starting_point,tiles_width*self.tilesize):
                            if  'cos' in fn or  'sin' in fn or   'tan' in fn or  'cot' in fn:
                                if self.rad_deg_input.text=='' or self.rad_deg_input.text=='d':
                                    x=x*pi/180
                            if 'asin' in fn  or 'acos' in fn:
                                if x>=1:
                                    x=1
                                elif x<=-1:
                                    x=-1
                            try:
                                list_of_points.append(Point(self,(x*self.tilesize+tiles_width//2*self.tilesize,-eval(fn)*self.tilesize+tiles_height//2*self.tilesize)))
                            except ZeroDivisionError:
                                if x!=0:
                                    list_of_points.append(Point(self,(x*self.tilesize+tiles_width//2*self.tilesize,-eval(fn)*self.tilesize+tiles_height//2*self.tilesize)))


                    self.dict_of_points[fn]=list_of_points



    def create_a_graph(self):
        tiles_width=self.surf_rect.width//self.tilesize
        tiles_height=self.surf_rect.height//self.tilesize
        if self.dict_of_points:
            for fn in self.dict_of_points.keys():
                if not self.dict_of_points[fn]:
                    list_of_points=[]
                    if 'log' in fn or 'sqrt' in fn :
                        starting_point=1
                    elif 'tan' in fn:
                        starting_point=-tiles_width*self.tilesize
                    elif 'exp' in fn:
                        starting_point=-tiles_width//2*self.tilesize
                    # elif 'asin' in fn or 'acos' in fn:
                    #     starting_point=-1

                    else:
                        starting_point=-tiles_width*self.tilesize
                    for x in range(starting_point,tiles_width*self.tilesize):
                            if  'cos' in fn or  'sin' in fn or   'tan' in fn or  'cot' in fn:
                                if self.rad_deg_input.text=='' or self.rad_deg_input.text=='d':
                                    x=x*pi/180
                            if 'asin' in fn  or 'acos' in fn:
                                if x>=1:
                                    x=1
                                elif x<=-1:
                                    x=-1
                            try:
                                list_of_points.append(Point(self,(x*self.tilesize+tiles_width//2*self.tilesize,-eval(fn)*self.tilesize+tiles_height//2*self.tilesize)))
                            except ZeroDivisionError:
                                if x!=0:
                                    list_of_points.append(Point(self,(x*self.tilesize+tiles_width//2*self.tilesize,-eval(fn)*self.tilesize+tiles_height//2*self.tilesize)))


                    self.dict_of_points[fn]=list_of_points


    def change_size_with_the_same_quality(self,surf,var):
        changed_surf=pg.transform.scale(surf,(var[0],var[1]))
        return changed_surf

    def qe_logic(self):
        y=float(self.field_2.text)
        x=float(self.field_1.text)
        z=float(self.field_3.text)
        discri = y * y - 4 * x * z
        sqrtval = sqrt(abs(discri))
        if x!=0:
            if discri > 0:
                return [" real and different roots ",str((-y + sqrtval)/(2 * x)),str((-y - sqrtval)/(2 * x))]
            elif discri == 0:
                return [" real and same roots",str(-y / (2 * x))]
            else:
                return ["Complex Roots",str(- y / (2 * x))+" + i*"+str(sqrtval/(2 * x)),str(- y / (2 * x))+" - i*"+str(sqrtval/(2 * x))]
        else:
            return ['invalid equation']

    def sorting(self,r):
        return r.right

    def update_qe(self):
        all_not_False=False
        for v in self.dict_of_fields.values():
            if v:
                all_not_False=True
        if not all_not_False:
            self.dict_of_fields[self.field_1]=True
        self.screen_rect=self.screen.get_rect()
        self.qe_template.update()
        self.field_3.update()
        self.field_2.update()
        self.field_1.update()

        self.field_2.pos.y=self.rect_of_xpt.top
        self.field_2.pos.x=self.rect_of_xpt.right+10

        self.field_3.pos.y=self.rect_of_x.top
        self.field_3.pos.x=self.rect_of_x.right+10
        self.grapher_button.update()
        #if self.rect_of_zero.right>self.qe_template.rect.right:

        self.list_of_rects_to_check=[self.rect_x1,self.rect_x2,self.rect_eq,self.rect_of_zero]
        self.list_of_rects_to_check.sort(reverse=True,key=self.sorting)
        #print([r.right for r in self.list_of_rects_to_check])

        # all_in=True
        # for r in self.list_of_rects_to_check:
        #     if r.right>self.screen_rect.right:
        #         all_in=False
        # if not all_in:
        #     self.qe_template.rect.width+=self.list_of_rects_to_check[0].right-self.qe_template.rect.right
        # else:
        #     self.qe_template.rect=self.screen_rect
        self.qe_template.rect.width+=self.list_of_rects_to_check[0].right-self.qe_template.rect.right

        if self.rect_eq.right>self.qe_template.rect.right:
            pass
        if self.qe_template.rect.right>self.screen_rect.right:
            self.scrollbar_qe.bar.interactable=True
        else:
            self.scrollbar_qe.bar.interactable=False

        self.scrollbar_qe.update()
        self.scrollbar_qe.bar.update()
        self.qe_template.rect.left=-self.scrollbar_qe.bar.rect.left/(self.screen_rect.width/self.qe_template.rect.width)

    def update_calc(self):


        if not self.list_of_calc_buttons:

            self.screen = pg.display.set_mode((400, 600),pg.RESIZABLE)
            self.screen_rect=self.screen.get_rect()
            self.prev_size_for_a_ratio=[self.screen_rect.width,self.screen_rect.height]
            increment=0
            for i in range(7):
                increment+=self.screen_rect.height/10
                for point in range(43,int(self.screen_rect.width*0.8),self.screen_rect.width//6):
                    self.list_of_calc_buttons.append(OnCalcButton(self,(point,self.culc_screen.rect.height*3+increment+10)))
            for num,button in enumerate(self.list_of_calc_buttons):
                button.value=self.list_of_button_values[num]
            for value in self.list_of_button_values:
                self.dict_of_buttons[value]=None
            for key,value in self.dict_of_buttons.items():
                for button in self.list_of_calc_buttons:
                    if button.value==key:
                        self.dict_of_buttons[key]=button
        else:
            for button in self.list_of_calc_buttons:
                button.update()



        self.calc_background_new=self.change_size_with_the_same_quality(self.calc_background,(self.screen_rect.width,self.screen_rect.height))
        self.culc_screen.update()




    def update(self):


        self.screen_rect=self.screen.get_rect()
        # update portion of the game loop
        self.calc_button.update()
        self.button_qe.update()
        if self.surf_rect.right<self.screen_rect.right:
            self.surf_rect.left=self.screen_rect.left

        self.pointer.update()

        self.number1=-self.surf_rect.width//2
        self.number2=-self.surf_rect.height//2

        self.create_a_graph()


        self.scrollbar_bottom.bar.update()
        self.scrollbar_right.bar.update()
        for widget in self.widgets:
            widget.update()

        self.surf=pg.transform.scale(self.surf,(self.surf_rect.width,self.surf_rect.height))


        # self.point_to_ckeck=vec(self.pointer.rect.center)-vec(self.surf_rect.topleft)
        # self.point_to_ckeck.x=self.point_to_ckeck.x+self.surf_rect.x-self.screen_rect.x
        # self.point_to_ckeck.y=self.point_to_ckeck.y+self.surf_rect.y-self.screen_rect.y
        if self.tilesize!=32:

            # moving the graph

            if self.surf_rect.right>self.screen_width:
                self.surf_rect.right=self.screen_width
                self.surf_rect.left=-self.scrollbar_bottom.bar.rect.x/(32/self.tilesize)
                # for fn,val in self.dict_of_points.items():
                #     for value in val:
                #         value.rect.left=value.rect.left-self.scrollbar_bottom.bar.rect.x/(32/self.tilesize)
                self.scrollbar_bottom.bar.interactable=True
            else:
                self.scrollbar_bottom.bar.interactable=False
            if self.surf_rect.bottom>self.screen_height:
                self.surf_rect.bottom=self.screen_height
                self.surf_rect.top=-self.scrollbar_right.bar.rect.y/(32/self.tilesize)
                # for fn,val in self.dict_of_points.items():
                #     for value in val:
                #         value.rect.top=value.rect.top-self.scrollbar_bottom.bar.rect.x/(32/self.tilesize)
                self.scrollbar_right.bar.interactable=True
            else:
                self.scrollbar_right.bar.interactable=False

            self.input.get_coords((0,self.screen_height-25))
            self.color_input.get_coords((self.input.rect.width+self.input.rect.width//4,self.screen_height-25))
            self.legend.get_coords((self.screen_width-25,self.screen_height-25))

            #self.screen = pg.display.set_mode((self.screen_width+25,self.screen_height+25),pg.RESIZABLE,)
            self.draw_scroll_bar=True
            self.scrollbar_right.update(self.screen_height,(self.screen_width,0))
            self.scrollbar_bottom.update(self.screen_width,(0,self.screen_height))




        else:

            self.input.get_coords((0,self.screen_height))
            self.color_input.get_coords((self.input.rect.width+self.input.rect.width//4,self.screen_height))
            self.legend.get_coords((self.screen_width,self.screen_height))
            #self.screen = pg.display.set_mode((self.screen_width,self.screen_height),pg.RESIZABLE,)
            self.draw_scroll_bar=False
        self.all_sprites.update()



    def draw_grid(self):
        for x in range(0, self.surf_rect.width, self.tilesize):
            pg.draw.line(self.surf, LIGHTGREY, (x, 0), (x, self.surf_rect.height))
        for y in range(0, self.surf_rect.height, self.tilesize):
            pg.draw.line(self.surf, LIGHTGREY, (0, y), (self.surf_rect.width, y))
        tiles_width=self.surf_rect.width//self.tilesize
        tiles_height=self.surf_rect.height//self.tilesize
        pg.draw.line(self.surf,CYAN,(tiles_width//2*self.tilesize,0),(tiles_width//2*self.tilesize,self.surf_rect.height),2)
        pg.draw.line(self.surf,CYAN,(0,tiles_height//2*self.tilesize),(self.surf_rect.width,tiles_height//2*self.tilesize),2)
        # enumeration of the graph: lines, numbers
        for i in range(0,self.surf_rect.width,self.tilesize):
            pg.draw.line(self.surf,CYAN,(i,tiles_height//2*self.tilesize-self.tilesize//4),(i,tiles_height//2*self.tilesize+self.tilesize//4),2)
        for i in range(0,self.surf_rect.height,self.tilesize):
            pg.draw.line(self.surf,CYAN,(tiles_width//2*self.tilesize-self.tilesize//4,i),(tiles_width//2*self.tilesize+self.tilesize//4,i),2)
        self.number1-=self.tilesize
        self.number2-=self.tilesize
        for i in range(0,self.surf_rect.width,self.tilesize):
            self.number1=self.number1+self.tilesize
            self.draw_text_surf(str(self.number1//self.tilesize),self.font,14,WHITE,i+3,self.surf_rect.height//2+self.tilesize//4)
        for i in range(0,self.surf_rect.height,self.tilesize):
            self.number2=self.number2+self.tilesize
            if self.number2!=0:
                self.draw_text_surf(str(-self.number2//self.tilesize),self.font,14,WHITE,self.surf_rect.width//2+self.tilesize//4,i+3)


    def draw_calc(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.calc_background_new,(0,0))
        self.culc_screen.draw()
        for button in self.list_of_calc_buttons:
            button.draw()
        pg.display.flip()

    def draw_qe(self):

        self.qe_template.img.fill(DARKGREY)
        self.field_1.draw()
        xpt=self.draw_text_surf_change('*x**2+',self.font,int(self.qe_template.rect.height*0.1),CYAN,self.field_1.rect.right+10,self.field_1.rect.top,self.qe_template.img)
        self.rect_of_xpt=xpt
        self.field_2.draw()
        x=self.draw_text_surf_change('*x+',self.font,int(self.qe_template.rect.height*0.1),CYAN,self.field_2.rect.right+10,self.field_2.rect.top,self.qe_template.img)
        self.rect_of_x=x
        self.field_3.draw()
        self.rect_of_zero=self.draw_text_surf_change('=0',self.font,int(self.qe_template.rect.height*0.1),CYAN,self.field_3.rect.right+10,self.field_3.rect.top,self.qe_template.img)
        if len(self.result_eq)>0:
            rect=self.draw_text_surf_change(self.result_eq[0],self.font,int(self.qe_template.rect.height*0.07),CYAN,self.field_1.rect.left,self.field_1.rect.bottom+self.field_1.rect.height-6,self.qe_template.img)
            if len(self.previous_e)>0:
                for n,p in enumerate(self.previous_e):
                    if self.previous_e[n][0]!='-' and self.previous_e[n][0]!='+' and n!=0:
                        self.previous_e[n]="+"+self.previous_e[n]
                self.rect_eq=self.draw_text_surf_change(self.previous_e[0]+"*x**2"+self.previous_e[1]+"*x"+self.previous_e[2]+'=0:',self.font,int(self.qe_template.rect.height*0.07),CYAN,rect.left,rect.top-rect.height,self.qe_template.img)
            if self.result_eq[0]!='invalid equation':
                self.rect_x1=self.draw_text_surf_change('x1='+self.result_eq[1],self.font,int(self.qe_template.rect.height*0.07),CYAN,rect.left,rect.bottom,self.qe_template.img)
                self.rect_x2=self.draw_text_surf_change('x2='+self.result_eq[2],self.font,int(self.qe_template.rect.height*0.07),CYAN,rect.left,rect.bottom+rect.height,self.qe_template.img)
        self.qe_template.draw()
        self.grapher_button.draw()
        self.scrollbar_qe.draw()
        pg.display.flip()

    def draw(self):
        self.screen.fill(BLACK)
        self.surf.fill(BGCOLOR)
        self.draw_grid()
        if self.dict_of_points:
            for fn in self.dict_of_points.keys():
                for n,s_p in enumerate(self.dict_of_points[fn]):
                    if n<len(self.dict_of_points[fn])-1: #and n%3!=0:
                        pg.draw.line(self.surf,eval(self.graph_color_dict[fn]),self.dict_of_points[fn][n].rect.center,self.dict_of_points[fn][n+1].rect.center,1)
        if self.draw_points:
            self.all_sprites.draw(self.surf)
        self.screen.blit(self.surf,self.surf_rect)
        if self.function_input:
            self.input.draw()
        if self.color_input_text:
            self.color_input.draw()
        if self.draw_legend:
            self.legend.draw()
        if self.draw_scroll_bar:
            self.scrollbar_bottom.draw()
            self.scrollbar_right.draw()
        if self.draw_rad_deg_input:
            self.rad_deg_input.draw()

        self.pointer.draw()
        list_of_coords=[]
        for fn,val in self.dict_of_points.items():
            for sprite in val:
                if sprite.drawing:

                    self.screen.blit(sprite.image,self.pointer.rect.topleft)
                    list_of_coords.append((sprite.rect.centerx-self.number_of_tiles_width/2*self.tilesize,sprite.rect.centery-self.number_of_tiles_height/2*self.tilesize))
        if len(list_of_coords)>0:
            point=list(list_of_coords[-1])
            coords=[round(i/self.tilesize,2) for i in point]
            coords[1]*=-1
            self.draw_text(str(coords),self.font,20,WHITE,self.pointer.rect.x+10,self.pointer.rect.y-10)

        self.calc_button.draw()
        self.button_qe.draw()
        pg.display.flip()

    def recur_factorial(self,n):
        if n == 1:
           return n
        elif n < 1 or type(n)==float:
           return ("Error")
        else:
           return n*self.recur_factorial(n-1)

    def events_qe(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.grapher_button.rect,pg.mouse.get_pos()):
                    print(self.previous_size_graph)
                    self.screen = pg.display.set_mode((self.previous_size_graph[0], self.previous_size_graph[1]),pg.RESIZABLE)
                    if not self.run_graph:
                        self.previous_size_qe=[self.screen_rect.width,self.screen_rect.height]
                    self.run_graph=True
                    self.run_qe=False
            if  event.type==pg.VIDEORESIZE:
                if self.new_size_for_a_ratio_qe:
                    self.prev_size_for_a_ratio_qe=self.new_size_for_a_ratio_qe
                self.screen = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)

                self.new_size_for_a_ratio_qe=(event.w, event.h)
                self.screen_rect=self.screen.get_rect()
            for f in list(self.dict_of_fields.keys()):
                if event.type == pg.KEYDOWN:
                    if self.dict_of_fields[f] :
                        if event.key==pg.K_BACKSPACE:
                                f.text=f.text[:-1]
                        elif event.key!=pg.K_RETURN:
                            if event.unicode.isnumeric() or event.unicode=='.' or event.unicode=='-':
                                f.text+=event.unicode
                        if event.key==pg.K_RETURN and f.text!='':
                            self.dict_of_fields[f]=False
                            index=list(self.dict_of_fields.keys()).index(f)
                            if index<2:
                                self.dict_of_fields[list(self.dict_of_fields.keys())[index+1]]=True
                            else:
                                self.result_eq=self.qe_logic()
                                self.previous_e=[self.field_1.text,self.field_2.text,self.field_3.text]
                                self.field_1.text=''
                                self.field_2.text=''
                                self.field_3.text=''
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1:
                if pg.Rect.collidepoint(self.scrollbar_qe.bar.rect,pg.mouse.get_pos()):
                    self.scrollbar_qe.bar.clicked=True
            elif event.type==pg.MOUSEBUTTONUP and event.button == 1 and self.scrollbar_qe.bar.clicked :
                    self.scrollbar_qe.bar.clicked=False
            # if event.type == pg.KEYDOWN:
            #     if  event.key==pg.K_c:
            #         self.previous_e=[]
            #         self.result_eq=[]
            #         self.rect_eq=self.qe_template.rect
            #         self.rect_x2=self.qe_template.rect
            #         self.rect_x1=self.qe_template.rect
            #         self.rect_of_zero=self.qe_template.rect







    def events_calc(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

                #print(f"{self.prev_size_for_a_ratio},{self.new_size_for_a_ratio}")
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['g'].rect,pg.mouse.get_pos()):
                self.dict_of_buttons['g'].clicked=True
                if self.dict_of_buttons['g'].clicked:
                    self.screen = pg.display.set_mode((self.previous_size_graph[0], self.previous_size_graph[1]),pg.RESIZABLE)
                    if not self.run_graph:
                        self.previous_size_calc=[self.screen_rect.width,self.screen_rect.height]
                    self.run_graph=True
                    self.run_calc=False
                    #self.list_of_calc_buttons.clear()

                    self.screen_rect=self.screen.get_rect()
                    #pg.display.iconify()
            # if event.type==pg.MOUSEBUTTONUP and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['g'].rect,pg.mouse.get_pos()):
            #       self.dict_of_buttons['g'].clicked=False
            if  event.type==pg.VIDEORESIZE:
                if self.new_size_for_a_ratio:
                    self.prev_size_for_a_ratio=self.new_size_for_a_ratio
                self.screen = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)

                self.new_size_for_a_ratio=(event.w, event.h)
                self.screen_rect=self.screen.get_rect()

            # buttons` action
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and self.culc_screen.text=='Error':
                self.culc_screen.text=''


            if len(self.culc_screen.text)>1 and event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['<'].rect,pg.mouse.get_pos()):
                self.culc_screen.last_command='<'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.result=False
                self.culc_screen.text=self.culc_screen.dict_of_previous_rows[0]
                self.culc_screen.text=self.culc_screen.text[:-1]
            elif len(self.culc_screen.text)==1 and event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['<'].rect,pg.mouse.get_pos()):
                self.culc_screen.last_command='<'
                if len(list(self.culc_screen.dict_of_previous_rows.keys()))>=2:
                    del self.culc_screen.dict_of_previous_rows[self.culc_screen.number_of_row]
                    self.culc_screen.number_of_row+=1
                    self.culc_screen.text=self.culc_screen.dict_of_previous_rows[self.culc_screen.number_of_row]
                self.culc_screen.dict_of_previous_rows={k-1:v for k,v in self.culc_screen.dict_of_previous_rows.items()}
                self.culc_screen.number_of_row-=1

            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['C'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.text=''
                self.culc_screen.complete_command=''
                self.culc_screen.dict_of_previous_rows.clear()
                self.culc_screen.number_of_row=0
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['1'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='1'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='1'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['2'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='2'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='2'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['3'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='3'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='3'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['4'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='4'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='4'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['5'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='5'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='5'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['6'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='6'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='6'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['7'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='7'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='7'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['8'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='8'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='8'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['9'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='9'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='9'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['0'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='0'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='0'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['.'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='.'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='.'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['('].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='('
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons[')'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command=')'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+=')'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['pi'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='pi'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='pi'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['sin'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='sin('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='sin('
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['cos'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='cos('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='cos('
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['tan'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='tan('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='tan('
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['+'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='+'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="+"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['-'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='-'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="-"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['*'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='*'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="*"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['/'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='/'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="/"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['%'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='%'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="%"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['deg'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='degrees('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="degrees("
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['lg'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='log('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="log("
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['sqrt'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='sqrt('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="sqrt("
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['rad'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='radians('
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="radians("
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons[','].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command=','
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+=","
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['^'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='**'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+="**"
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['e'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                self.culc_screen.last_command='exp(1)'
                self.culc_screen.last_commands_list.append(self.culc_screen.last_command)
                self.culc_screen.text+='exp(1)'
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['='].rect,pg.mouse.get_pos()):

                    try:

                        num=0
                        self.culc_screen.text=str(eval(self.culc_screen.complete_command))

                        for l in str(eval(self.culc_screen.complete_command)):
                            if l=="0":
                                num+=1
                        print(num)
                        if num>5:
                            self.culc_screen.text=str(eval(self.culc_screen.complete_command))[:3]

                        self.culc_screen.result=True
                        self.culc_screen.number_of_row=0
                        self.culc_screen.complete_command=''
                        self.culc_screen.dict_of_previous_rows.clear()

                    except SyntaxError:
                        self.culc_screen.text="Error"
                    except NameError:
                        self.culc_screen.text="Error"

            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['x!'].rect,pg.mouse.get_pos()):
                self.culc_screen.result=False
                if self.culc_screen.complete_command!='':
                    frac,whole=modf(float(self.culc_screen.complete_command))
                if self.culc_screen.complete_command=="" or self.culc_screen.complete_command=="0":
                    self.culc_screen.text=str(1)
                elif frac!=0:
                    self.culc_screen.text=str(self.recur_factorial(float(self.culc_screen.text)))
                else:
                    self.culc_screen.text=str(self.recur_factorial(int(self.culc_screen.text)))
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.dict_of_buttons['1/x'].rect,pg.mouse.get_pos()):
                if self.culc_screen.complete_command!='' and self.culc_screen.complete_command!='0':
                    self.culc_screen.result=False
                    self.culc_screen.text=str(1/float(self.culc_screen.complete_command))
                    self.culc_screen.number_of_row=0
                    self.culc_screen.complete_command=''
                    self.culc_screen.dict_of_previous_rows.clear()
                else:
                    self.culc_screen.result=False
                    self.culc_screen.text='Error'
                    self.culc_screen.number_of_row=0
                    self.culc_screen.complete_command=''
                    self.culc_screen.dict_of_previous_rows.clear()
            if event.type==pg.MOUSEWHEEL and pg.Rect.collidepoint(self.culc_screen.rect,pg.mouse.get_pos()):

                if event.y==-1 and len(self.culc_screen.dict_of_previous_rows)>=2:
                    self.culc_screen.result=False
                    self.culc_screen.number_of_row-=1
                    if self.culc_screen.number_of_row>=0 and self.culc_screen.number_of_row<=len(list(self.culc_screen.dict_of_previous_rows.keys()))-1:
                        self.culc_screen.text=self.culc_screen.dict_of_previous_rows[self.culc_screen.number_of_row]
                    elif self.culc_screen.number_of_row<0:
                        self.culc_screen.number_of_row=0
                    elif self.culc_screen.number_of_row>len(list(self.culc_screen.dict_of_previous_rows.keys()))-1:
                        self.culc_screen.number_of_row=len(list(self.culc_screen.dict_of_previous_rows.keys()))-1


                if event.y==1 and len(self.culc_screen.dict_of_previous_rows)>=2:
                    self.culc_screen.result=False
                    self.culc_screen.number_of_row+=1
                    if self.culc_screen.number_of_row>=0 and self.culc_screen.number_of_row<=len(list(self.culc_screen.dict_of_previous_rows.keys()))-1 :
                        self.culc_screen.text=self.culc_screen.dict_of_previous_rows[self.culc_screen.number_of_row]
                    elif self.culc_screen.number_of_row<0:
                        self.culc_screen.number_of_row=0
                    elif self.culc_screen.number_of_row>len(list(self.culc_screen.dict_of_previous_rows.keys()))-1:
                        self.culc_screen.number_of_row=len(list(self.culc_screen.dict_of_previous_rows.keys()))-1








    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.calc_button.rect,pg.mouse.get_pos()):
                self.calc_button.clicked=True
                if self.calc_button.clicked:

                    self.screen = pg.display.set_mode((self.previous_size_calc[0],self.previous_size_calc[1]),pg.RESIZABLE)
                    if not self.run_calc:
                        self.previous_size_graph=[self.screen_rect.width,self.screen_rect.height]
                    self.run_graph=False
                    self.run_calc=True
                    self.screen_rect=self.screen.get_rect()

            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1 and pg.Rect.collidepoint(self.button_qe.rect,pg.mouse.get_pos()):
                self.button_qe.clicked=True
                if self.button_qe.clicked:
                    self.screen = pg.display.set_mode((self.previous_size_qe[0],self.previous_size_qe[1]),pg.RESIZABLE)
                    if not self.run_qe:
                        self.previous_size_graph=[self.screen_rect.width,self.screen_rect.height]
                    self.run_graph=False
                    self.run_calc=False
                    self.run_qe=True
                    self.screen_rect=self.screen.get_rect()

                    #pg.display.iconify()
            # if event.type==pg.MOUSEBUTTONUP and event.button == 1 and pg.Rect.collidepoint(self.calc_button.rect,pg.mouse.get_pos()):
            #         self.calc_button.clicked=False



            if event.type==pg.MOUSEBUTTONDOWN and event.button == 1:
                if pg.Rect.collidepoint(self.scrollbar_bottom.bar.rect,pg.mouse.get_pos()):
                    self.scrollbar_bottom.bar.clicked=True
                if pg.Rect.collidepoint(self.scrollbar_right.bar.rect,pg.mouse.get_pos()):
                    self.scrollbar_right.bar.clicked=True
            elif event.type==pg.MOUSEBUTTONUP and event.button == 1 and self.scrollbar_bottom.bar.clicked or event.type==pg.MOUSEBUTTONUP and event.button == 1 and self.scrollbar_right.bar.clicked:
                    self.scrollbar_bottom.bar.clicked=False
                    self.scrollbar_right.bar.clicked=False
                    self.renew_graphs()

            if event.type == pg.QUIT:
                self.quit()

            if  event.type==pg.VIDEORESIZE :
                if not self.full_screen :
                    self.screen = pg.display.set_mode((event.w, event.h),pg.RESIZABLE)
                    self.screen_width=event.w
                    self.screen_height=event.h
                    self.renew_graphs()



            if event.type == pg.KEYDOWN:



                if event.key==pg.K_UP:
                    if self.tilesize<64:
                        self.tilesize+=2
                        self.surf_rect.width=self.number_of_tiles_width*self.tilesize
                        self.surf_rect.height=self.number_of_tiles_height*self.tilesize
                        self.renew_graphs()
                if event.key==pg.K_DOWN:
                    if self.tilesize>32:
                        self.tilesize-=2

                        self.surf_rect.width=self.number_of_tiles_width*self.tilesize
                        self.surf_rect.height=self.number_of_tiles_height*self.tilesize
                        self.surf_rect.topleft=(0,0)
                        self.renew_graphs()

                # if event.key==pg.K_f:
                #     self.full_screen=not self.full_screen
                #     if self.full_screen:
                #         self.screen = pg.display.set_mode((self.monitor_size),pg.FULLSCREEN)
                #         self.screen_height=self.monitor_size[1]
                #         self.screen_width=self.monitor_size[0]
                #         self.renew_graphs()
                #     else:
                #         self.screen = pg.display.set_mode((self.monitor_size[0]//2,self.monitor_size[1]//2),pg.RESIZABLE,)
                #         self.renew_graphs()
                #         self.full_screen=False

                if event.key==pg.K_l:
                    self.draw_legend=not self.draw_legend
                if event.key == pg.K_v and pg.key.get_mods() & pg.KMOD_CTRL:
                    self.color_input.text=pyperclip.paste()
                if event.key==pg.K_BACKSPACE and self.input.text=='' and not self.draw_rad_deg_input:
                    if len(list(self.dict_of_points.keys()))>0:
                        key=list(self.dict_of_points.keys())[-1]
                        value=list(self.dict_of_points.values())[-1]
                        del self.graph_color_dict[key]
                        del self.dict_of_points[key]
                        for spr in value:
                            spr.kill()
                if event.key==pg.K_TAB:
                    self.dict_of_points.clear()
                    self.graph_color_dict.clear()
                    self.all_sprites.empty()
                if event.key==pg.K_p:
                    self.draw_points=not self.draw_points
                if event.key==pg.K_SPACE and not self.color_input_text:
                    self.function_input=not self.function_input

                if self.function_input:
                    if event.key==pg.K_BACKSPACE and not self.color_input_text:
                        self.input.text=self.input.text[:-1]
                    elif event.key!=pg.K_SPACE and event.key!=pg.K_RETURN and not self.color_input_text:
                        self.input.text+=event.unicode
                    if  event.key==pg.K_RETURN and  self.color_input.text=='' :
                        self.color_input_text= not self.color_input_text
                        if  not self.color_input_text:
                            self.function_input=False
                            self.color_input_text=False
                            try:
                                eval(self.input.text)
                            except SyntaxError:
                                pass

                            except NameError :
                                if 'x' in self.input.text:
                                    good=False
                                    str=self.input.text
                                    srt2=str.split('x')
                                    for el in srt2:
                                        if len(el)>0 and not el[-1].isalpha() :
                                            good=True
                                    if good:
                                        self.dict_of_points[self.input.text]=[]
                                    else:
                                        pass
                                else:
                                    pass

                            else:
                                self.dict_of_points[self.input.text]=[]
                            self.graph_color_dict[self.input.text]=f"({randint(0,255)},{randint(0,255)},{randint(0,255)})"
                            self.input.text=""
                            self.color_input.text=''
                if self.color_input_text:
                    if event.key==pg.K_BACKSPACE :
                        self.color_input.text=self.color_input.text[:-1]
                    elif  event.key!=pg.K_RETURN and event.key!=pg.K_SPACE and event.key!=pg.K_v:
                        self.color_input.text+=event.unicode
                    if  event.key==pg.K_RETURN and self.color_input.text!='' :
                        self.function_input=not self.function_input
                        self.color_input_text=not self.color_input_text
                        try:
                                eval(self.input.text)
                        except SyntaxError:
                                pass

                        except NameError :
                                if 'x' in self.input.text:
                                    good=False
                                    str=self.input.text
                                    srt2=str.split('x')
                                    for el in srt2:
                                        if len(el)>0 and not el[-1].isalpha() :
                                            good=True
                                    if good:
                                        self.dict_of_points[self.input.text]=[]
                                    else:
                                        pass
                                else:
                                    pass

                        else:
                                self.dict_of_points[self.input.text]=[]
                        self.graph_color_dict[self.input.text]=self.color_input.text
                        self.input.text=""
                        self.color_input.text=''

                if   event.key==pg.K_z:
                    self.draw_rad_deg_input=not self.draw_rad_deg_input

                if self.draw_rad_deg_input and event.key!=pg.K_RETURN and not self.function_input and event.key!=pg.K_z:
                    if event.key==pg.K_BACKSPACE :
                        self.rad_deg_input.text=self.rad_deg_input.text[:-1]
                    else:
                        self.rad_deg_input.text+=event.unicode
                        self.renew_graphs()






# create the game object


g = Game()
g.new()
g.run()

