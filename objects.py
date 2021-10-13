from settings import *
import pygame as pg
vec=pg.Vector2
import pyautogui
from os import path

def change_size_with_the_same_quality(surf,var):
        changed_surf=pg.transform.scale(surf,(var[0],var[1]))
        return changed_surf

class Point(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.pos=vec(pos)
        self.image=pg.Surface((5,5))
        self.image.fill(YELLOW)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos
        self.drawing=True
        self.diff_x=0
        self.diff_y=0
        self.new_rect=self.image.get_rect()
        self.new_rect.center=self.rect.center
        self.coord_to_check=vec(0,0)
    def __repr__(self):
        return f"{self.pos}"
    def update(self):
        self.coord_to_check=vec(self.rect.center)-vec(self.game.surf_rect.topleft)
        self.coord_to_check2=vec(self.game.pointer.rect.center)-vec(self.game.surf_rect.topleft)


        if self.rect.colliderect(self.game.apply_rect(self.game.pointer.rect)):
            self.drawing=True
        else:
            self.drawing=False



class Input:
    def __init__(self,game,pos):
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomleft=pos
        self.text=''
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        self.yr=self.game.draw_text('f(x)=',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-10)
        self.game.draw_text(self.text,self.game.font,20,BLACK,self.rect.left+45,self.rect.y+self.rect.height/2-10)
    def update(self):
        self.rect.bottomleft=self.pos
    def get_coords(self,pos):
        self.pos=pos

class ColorInput:
    def __init__(self,game,pos):
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomleft=pos
        self.text=''
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        self.yr=self.game.draw_text('RGB=',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-10)
        self.game.draw_text(self.text,self.game.font,20,BLACK,self.rect.left+60,self.rect.y+self.rect.height/2-10)
    def update(self):
        self.rect.bottomleft=self.pos
    def get_coords(self,pos):
        self.pos=pos

class Legend:
    def __init__(self,game,pos,dict):
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//3))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomright=pos
        self.dict=dict
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        pg.draw.rect(self.game.screen,BLACK,self.rect,3)
        if self.dict:
            height=0
            for key,val in self.dict.items():
                height+=20
                self.game.draw_text("-"+"  "+key,self.game.font,20,BLACK,self.rect.left+45,self.rect.y+height)
                pg.draw.rect(self.game.screen,eval(val),pg.Rect(self.rect.left+20,self.rect.y+height+10,10,10))
    def update(self):
        self.rect.bottomright=self.pos

    def get_coords(self,pos):
        self.pos=pos

class ScrollBarBar:
    def __init__(self, game, pos, width,road_width):
        self.game=game
        self.img=pg.Surface((width,25))
        self.img.fill(LIGHTGREY)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.topleft=self.pos
        self.clicked=False
        self.dif=0
        self.interactable=True
        self.road_width=road_width
    def update(self):
        if self.interactable:
            self.rect.width=self.game.screen.get_width()*(32/self.game.tilesize)
            self.img=pg.transform.scale(self.img,(int(self.rect.width),25))
            if self.clicked:
                self.rect.x=pg.mouse.get_pos()[0]+self.dif
                self.pos=self.rect.topleft
            else:
                self.dif=self.rect.x-pg.mouse.get_pos()[0]
            if self.rect.left<0:
                self.rect.left=0
                self.pos=self.rect
            elif self.rect.right>self.road_width-1:
                self.rect.right=self.road_width-1
                self.pos=self.rect


class ScrollBarBarRight:
    def __init__(self, game, pos, height,road_height):
        self.game=game
        self.img=pg.Surface((25,height))
        self.img.fill(LIGHTGREY)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.topright=self.pos
        self.clicked=False
        self.dif=0
        self.interactable=True
        self.road_height=road_height
    def update(self):
        if self.interactable:
            self.rect.height=self.game.screen.get_height()*(32/self.game.tilesize)
            self.img=pg.transform.scale(self.img,(25,int(self.rect.height)))
            if self.clicked:
                self.rect.y=pg.mouse.get_pos()[1]+self.dif
                self.pos=self.rect.topright
            else:
                self.dif=self.rect.y-pg.mouse.get_pos()[1]
            if self.rect.top<0:
                self.rect.top=0
                self.pos=self.rect
            elif self.rect.bottom>self.road_height-1:
                self.rect.bottom=self.road_height-1
                self.pos=self.rect



class ScrollBarBottom:
    def __init__(self,game,pos):
        self.game=game
        self.pos=pos
        self.img=pg.Surface((self.game.screen.get_width(),25))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.rect.bottomleft=self.pos
        self.bar=ScrollBarBar(self.game,(self.game.surf_rect.x,self.rect.top),self.game.screen.get_width()*(32/self.game.tilesize),self.rect.width)
        # self.road=pg.Rect((pos),self.game.screen.get_width(),self.game.screen.height()-pos[2])
        #
        # self.bar=pg.Rect(-self.game.surf_rect.x)
    def draw(self):
        if self.bar.interactable:
            self.game.screen.blit(self.img,self.rect)
            self.game.screen.blit(self.bar.img,self.bar.rect)
    def update(self,width,pos):
        if self.bar.interactable:
            # self.img=pg.transform.scale(self.img,(width,25))
            # self.rect=self.img.get_rect()
            self.rect.bottomleft=pos
            self.bar.rect.bottom=self.rect.bottom
            self.bar.pos=self.bar.rect.topright



class ScrollBarRight:
    def __init__(self,game,pos):
        self.game=game
        self.pos=pos
        self.img=pg.Surface((25,self.game.screen.get_height()))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.rect.bottomright=self.pos
        self.bar=ScrollBarBarRight(self.game,(self.rect.right,self.game.surf_rect.y),self.game.screen.get_height()*(32/self.game.tilesize),self.rect.height)
    def draw(self):
        if self.bar.interactable:
            self.game.screen.blit(self.img,self.rect)
            self.game.screen.blit(self.bar.img,self.bar.rect)
    def update(self,height,pos):
        if self.bar.interactable:
            # self.img=pg.transform.scale(self.img,(25,height))
            # self.rect=self.img.get_rect()
            self.rect.topright=pos
            self.bar.rect.right=self.rect.right
            self.bar.pos=self.bar.rect.topright

class ToFollowMouse:
    def __init__(self,game):
        self.img=pg.Surface((5,5))
        self.img.fill(WHITE)
        self.game=game
        self.rect=self.img.get_rect()
        self.rect.center=pg.mouse.get_pos()
        self.drawing=False
        self.pseudo_rect=self.img.get_rect()
        self.coords_to_check=vec(0,0)
    def update(self):
        #self.rect.center=vec(pg.mouse.get_pos())-self.game.surf_rect.topleft

        self.rect.center=vec(pg.mouse.get_pos())#-vec(self.game.surf_rect.topleft)

        #self.coords_to_check=(vec(self.rect.center)-vec(self.game.surf_rect.topleft))
    def draw(self):
        if self.drawing:
            self.game.screen.blit(self.img,self.rect)






class ButtonToTheCalculator:
    def __init__(self,game):
        self.game=game
        self.img=self.game.calc_button_img
        self.rect=self.img.get_rect()
        self.clicked=False
        self.collide_with_mouse=False
    def update(self):
        self.rect.topleft=self.game.screen_rect.topleft
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.img=self.game.calc_button_img2
        else:
            self.clicked=False
            self.img=self.game.calc_button_img
    def draw(self):
        self.game.screen.blit(self.img,self.rect)


class CalculatorScreen:
    def __init__(self,game):
        self.image_or=pg.Surface((20,20))
        self.image=pg.Surface((20,20))
        self.image.fill(WHITE)
        self.image_or.fill(WHITE)
        self.rect=self.image.get_rect()
        self.game=game
        self.text=''
        # self.surface_for_text=pg.Surface((self.rect.width/2,self.rect.height))
        # self.surface_for_text
        # self.surf_rect=self.surface_for_text.get_rect()
        self.text_rect=self.rect
        self.dict_of_previous_rows={}
        self.last_command=''
        self.last_command_backup=''
        self.complete_command=''
        self.number_of_row=0
        self.result=False
        self.max_number_of_ch=0
    def isoperator(self,ch):
        list=["+","-","*","/","%","**"]
        isoper=False
        for char in list:
            if ch==char:
                isoper=True
        return isoper

    # def recursive_result_distribution(self,number):
    #     if self.text_rect.left<self.rect.left:
    #         pass

    def update(self):
        if len(self.text)>0:
            self.max_number_of_ch=round((self.rect.width-self.game.screen_rect.height*0.09)/(self.text_rect.width/len(self.text)))

        self.rect.width=int(self.game.screen_rect.width*0.8)
        self.rect.height=int(self.game.screen_rect.height/9)
        self.image=pg.transform.scale(self.image_or,(self.rect.width,self.rect.height))
        self.rect=self.image.get_rect()
        self.rect.top=self.game.screen_rect.top+self.game.screen_rect.height*0.09
        self.rect.left=self.game.screen_rect.left+self.game.screen_rect.width*0.1

        # self.surface_for_text=pg.transform.scale(self.surface_for_text,(self.rect.width//2,self.rect.height))
        # self.surf_rect=self.surface_for_text.get_rect()
        # self.surf_rect.topleft=self.rect.topleft

        if self.last_command!=self.last_command_backup and self.number_of_row!=len(list(self.dict_of_previous_rows.keys()))-1:
            self.number_of_row=len(list(self.dict_of_previous_rows.keys()))-1
            self.text=self.dict_of_previous_rows[len(list(self.dict_of_previous_rows.keys()))-1]+self.last_command

        self.last_command_backup=self.last_command

        self.complete_command="".join([l for s in self.dict_of_previous_rows.values() for l in s])
        if len(self.text)>0:
            print(self.max_number_of_ch)
        if not self.result:
            print(self.dict_of_previous_rows)
            if self.text_rect.left<self.rect.left and self.text!='':
                # if self.number_of_rows%2==0 and self.number_of_rows!=0:
                #     self.dict_of_previous_rows[self.number_of_rows]=([self.last_command+self.text])
                # elif self.number_of_rows==0:
                #     self.dict_of_previous_rows[self.number_of_rows]=([self.text])
                # else:
                #     self.dict_of_previous_rows[self.number_of_rows]=([self.text[1:]])
                self.dict_of_previous_rows[self.number_of_row]=self.text
                self.dict_of_previous_rows[self.number_of_row]=self.dict_of_previous_rows[self.number_of_row][:-1]
                self.text=self.last_command

                self.number_of_row+=1
            self.dict_of_previous_rows[self.number_of_row]=self.text
        else:
            if self.number_of_row==0:
                for index in range(0, len(self.text), self.max_number_of_ch):
                    self.number_of_row=index//self.max_number_of_ch
                    self.dict_of_previous_rows[self.number_of_row]=(self.text[index : index + self.max_number_of_ch])
            self.text=self.dict_of_previous_rows[self.number_of_row]


            print(self.dict_of_previous_rows)
            print(self.number_of_row)




    def draw(self):
        # self.image.blit(self.surface_for_text,self.surf_rect)
        self.game.screen.blit(self.image,self.rect)
        pg.draw.rect(self.game.screen,BLACK,self.rect,3)
        if self.text=='' and len(list(self.dict_of_previous_rows.keys()))<=1:
            self.text_rect=self.game.draw_text('0',self.game.font,self.rect.height//2,BLACK,self.rect.width,self.rect.top+self.rect.height//4)


        else:
            self.text_rect=self.game.draw_text(self.text,self.game.font,self.rect.height//2,BLACK,self.rect.width,self.rect.top+self.rect.height//4,align='ne')



class OnCalcButton:
    def __init__(self,game,pos):
        self.pos=vec(pos)
        self.game=game
        self.img_or=game.calc_on_button_img
        self.img=game.calc_on_button_img
        self.img_or2=game.calc_on_button_img2
        self.img_or3=game.calc_on_button_img_orange
        self.img_or4=game.calc_on_button_img_orange1
        self.rect=self.img.get_rect()
        self.rect.topleft=self.pos
        self.previous_ratio_x=0
        self.previous_ratio_y=0
        self.grapher_button=self.game.grapher_button_img
        self.grapher_button_or=self.game.grapher_button_img
        self.value=''
        self.clicked=False
    def update(self):
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            self.clicked=False

        if self.game.prev_size_for_a_ratio and self.game.new_size_for_a_ratio:
            ratio_x=self.game.prev_size_for_a_ratio[0]/self.game.new_size_for_a_ratio[0]
            ratio_y=self.game.prev_size_for_a_ratio[1]/self.game.new_size_for_a_ratio[1]
            if ratio_x>0 and self.previous_ratio_x!=ratio_x:
                self.pos.x/=ratio_x
                self.previous_ratio_x=ratio_x
            if ratio_y>0 and self.previous_ratio_y!=ratio_y:
                self.pos.y/=ratio_y
                self.previous_ratio_y=ratio_y
        if self.value!='=':
            if not self.rect.collidepoint(pg.mouse.get_pos()):
                self.img=change_size_with_the_same_quality(self.img_or,(self.game.screen_rect.width//8,self.game.screen_rect.height//13))
            else:
                self.img=change_size_with_the_same_quality(self.img_or2,(self.game.screen_rect.width//8,self.game.screen_rect.height//13))
        else:
            if not self.rect.collidepoint(pg.mouse.get_pos()):
                self.img=change_size_with_the_same_quality(self.img_or3,(self.game.screen_rect.width//8,self.game.screen_rect.height//13))
            else:
                self.img=change_size_with_the_same_quality(self.img_or4,(self.game.screen_rect.width//8,self.game.screen_rect.height//13))


        self.rect=self.img.get_rect()

        self.rect.topleft=self.pos
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        if self.value!='g':
            if self.value!='sqrt' and self.value!='cos' and self.value!='deg':
                self.game.draw_text(self.value,self.game.font,self.rect.height//2,BLACK,self.rect.x+self.rect.width//4,self.rect.y+self.rect.height//4 )


            else:
                self.game.draw_text(self.value,self.game.font,self.rect.height//2,BLACK,self.rect.x+self.rect.width//4-5,self.rect.y+self.rect.height//4 )
        elif self.value=='g':
            self.grapher_button=pg.transform.scale(self.grapher_button_or,(self.rect.width,self.rect.height))
            self.game.screen.blit(self.grapher_button,self.rect.topleft)








