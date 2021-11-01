from settings import *
import pygame as pg
import sympy
from sympy import diff,parse_expr,abc

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
        self.game.draw_text('Functions:',self.game.font,20,BLACK,self.rect.left+45,self.rect.y)
        if self.dict:
            height=0
            for key,val in self.dict.items():
                height+=20
                self.game.draw_text("-"+"  "+key,self.game.font,20,BLACK,self.rect.left+45,self.rect.y+height)
                pg.draw.rect(self.game.screen,eval(val),pg.Rect(self.rect.left+30,self.rect.y+height+10,10,10))
                self.game.draw_text(str(list(self.dict.keys()).index(key))+')',self.game.font,20,BLACK,self.rect.left+10,self.rect.y+height)
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
        self.img=self.game.calc_button_img
        self.rect.topleft=self.game.screen_rect.topleft
        if self.rect.collidepoint(pg.mouse.get_pos()) and 0<pg.mouse.get_pos()[0]<self.game.screen_rect.width and 0<pg.mouse.get_pos()[1]<self.game.screen_rect.height:
            self.img=self.game.calc_button_img2
        else:
            self.clicked=False
            self.img=self.game.calc_button_img
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        pg.draw.rect(self.game.screen,BLACK,self.rect,3)

class ButtonToTheQE:
    def __init__(self,game):
        self.game=game
        self.img=self.game.qe_button_img
        self.rect=self.img.get_rect()
        self.clicked=False
        self.collide_with_mouse=False
    def update(self):
        self.rect.left=self.game.screen_rect.left
        self.rect.top=self.game.screen_rect.top+self.rect.height
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.img=self.game.qe_button_img1
        else:
            self.clicked=False
            self.img=self.game.qe_button_img
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        pg.draw.rect(self.game.screen,BLACK,self.rect,3)


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
        self.last_command=""
        self.last_commands_list=[]
        self.last_command_backup=[]
        self.complete_command=''
        self.number_of_row=0
        self.result=False
        self.max_number_of_ch=0
        self.result_set=False
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
        if len(self.last_commands_list)!=len(self.last_command_backup) and self.number_of_row!=0  :
            self.number_of_row=0
            if self.last_command!='<':
                self.text=self.dict_of_previous_rows[0]+self.last_command
            else:
                self.text=self.dict_of_previous_rows[0]



        if self.last_commands_list!=self.last_command_backup:
            self.last_command_backup.append(self.last_command)

        self.complete_command="".join([l for s in self.dict_of_previous_rows.values() for l in s])
        if not self.result:



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
                self.number_of_row=len(self.dict_of_previous_rows.keys())
                list_of_keys=list(self.dict_of_previous_rows.keys())
                list_of_keys.insert(0,self.number_of_row)
                list_of_values=list(self.dict_of_previous_rows.values())
                list_of_values.append(self.text)
                new_rows=list(zip(list_of_keys,list_of_values))
                new_rows={k:v for k,v in new_rows}
                self.dict_of_previous_rows=new_rows
                self.number_of_row=0
            self.dict_of_previous_rows[self.number_of_row]=self.text
        else:
            if self.number_of_row==0:
                for index in range(0, len(self.text), self.max_number_of_ch):
                    self.number_of_row=index//self.max_number_of_ch
                    self.dict_of_previous_rows[self.number_of_row]=(self.text[index : index + self.max_number_of_ch])
                    list_of_keys=list(self.dict_of_previous_rows.keys())
                    list_of_values=list(self.dict_of_previous_rows.values())
                    list_of_keys.sort(reverse=True)
                    new_rows=list(zip(list_of_keys,list_of_values))
                    new_rows={k:v for k,v in new_rows}
                    self.dict_of_previous_rows=new_rows
                self.text=self.dict_of_previous_rows[self.number_of_row]










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

class Degree_Radians_Input:
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
        self.yr=self.game.draw_text('Radians or Degrees',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-22)
        self.yr=self.game.draw_text('(r or d)=',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-5)
        self.game.draw_text(self.text,self.game.font,20,BLACK,self.rect.left+75,self.rect.y+self.rect.height/2-5)
    def update(self):
        self.rect.bottomleft=self.pos
    def get_coords(self,pos):
        self.pos=pos

class Template:
    def __init__(self,game):
        self.img=pg.Surface((600,300))
        self.img.fill(DARKGREY)
        self.rect=self.img.get_rect()
        self.game=game
    def update(self):
        if self.rect.width<=self.game.screen_rect.width:
            self.rect=self.game.screen_rect
        else:
            self.rect.height=self.game.screen_rect.height
        self.img=pg.transform.scale(self.img,(self.rect.width,self.rect.height))
        self.rect.topleft=self.game.screen_rect.topleft
    def draw(self):
        self.game.screen.blit(self.img,self.rect)

class Grapher_button:
    def __init__(self,game):
        self.game=game
        self.img=self.game.grapher_button_img2
        self.rect=self.img.get_rect()
        self.clicked=False
        self.collide_with_mouse=False
    def update(self):
        self.rect.left=self.game.screen_rect.left
        self.rect.top=self.game.screen_rect.top
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.img=self.game.grapher_button_img1
        else:
            self.clicked=False
            self.img=self.game.grapher_button_img2
    def draw(self):
        self.game.screen.blit(self.img,self.rect)
        pg.draw.rect(self.game.screen,BLACK,self.rect,3)

class FieldFollower:
    def __init__(self,game,pos):
        self.game=game
        self.pos=vec(pos)
        self.image=pg.Surface((self.game.qe_template.rect.width*0.1,self.game.qe_template.rect.height*0.1))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        self.rect.topleft=self.pos
        self.previous_ratio_x=0
        self.previous_ratio_y=0
        self.active=False
        self.text=''
        self.rect_of_text=self.rect
        self.new_coords=False
    def update(self):
        self.image=pg.Surface((self.game.qe_template.rect.width*0.1,self.game.qe_template.rect.height*0.1))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        if not self.new_coords:
            if self.game.prev_size_for_a_ratio_qe and self.game.new_size_for_a_ratio_qe:
                ratio_x=self.game.prev_size_for_a_ratio_qe[0]/self.game.new_size_for_a_ratio_qe[0]
                ratio_y=self.game.prev_size_for_a_ratio_qe[1]/self.game.new_size_for_a_ratio_qe[1]
                if ratio_x>0 and self.previous_ratio_x!=ratio_x:
                    self.pos.x/=ratio_x
                    self.previous_ratio_x=ratio_x
                if ratio_y>0 and self.previous_ratio_y!=ratio_y:
                    self.pos.y/=ratio_y
                    self.previous_ratio_y=ratio_y
        self.rect.topleft=self.pos
        if self.rect.right<self.rect_of_text.right:
            self.rect.width=self.rect_of_text.width
            self.image=pg.Surface((self.rect.width,self.rect.height))
            self.image.fill(WHITE)
    def draw(self):
        self.game.qe_template.img.blit(self.image,self.rect)
        self.rect_of_text=self.game.draw_text_surf_change(self.text,self.game.font,int(self.game.qe_template.rect.height*0.1),BLACK,self.rect.left,self.rect.top,self.game.qe_template.img)




class ScrollBarBarQE:
    def __init__(self, game, pos, width,road_width):
        self.game=game
        self.img=pg.Surface((width,25))
        self.img.fill(LIGHTGREY)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.topleft=self.pos
        self.clicked=False
        self.dif=0
        self.interactable=False
        self.road_width=road_width
    def update(self):
        if self.interactable:

            self.rect.width=self.game.screen_rect.width*(self.game.screen_rect.width/self.game.qe_template.rect.width)
            self.img=pg.transform.scale(self.img,(int(self.rect.width),25))
            if self.clicked:
                self.rect.x=pg.mouse.get_pos()[0]+self.dif
                self.pos=self.rect.topleft
            else:
                self.dif=self.rect.x-pg.mouse.get_pos()[0]
            if self.rect.left<0:
                self.rect.left=0
                self.pos=self.rect
            elif self.rect.right>self.game.screen_rect.width:
                self.rect.right=self.game.screen_rect.width
                self.pos=self.rect

class ScrollBarBottomQE:
    def __init__(self,game,pos):
        self.game=game
        self.pos=pos
        self.img=pg.Surface((self.game.screen.get_width(),25))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.rect.bottomleft=self.pos
        self.bar=ScrollBarBarQE(self.game,(self.game.surf_rect.x,self.rect.top),self.game.screen_rect.width-(self.game.qe_template.rect.width-self.game.screen_rect.width),self.rect.width)
    def draw(self):
        if self.bar.interactable:
            self.game.screen.blit(self.img,self.rect)
            self.game.screen.blit(self.bar.img,self.bar.rect)
    def update(self):
        if self.bar.interactable:
            self.rect.width=self.game.qe_template.rect.width
            self.img= pg.transform.scale(self.img,(self.rect.width,self.rect.height))
            self.rect.bottomleft=self.game.qe_template.rect.bottomleft
            self.bar.rect.bottom=self.rect.bottom
            self.bar.pos=self.bar.rect.topright
class DerivativeManager:
    def __init__(self,game,pos):
        self.drawing=False
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomleft=pos
        self.colors={}
        self.color_input=False
        self.text=''
        self.text_color=''
        self.color_inp_img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.color_inp_img.fill(WHITE)
        self.rect2=self.color_inp_img.get_rect()
        self.rect.bottomleft=pos
    def draw(self):
        if self.drawing:
            self.game.screen.blit(self.img,self.rect)
            self.yr=self.game.draw_text('Derivative for f(x)',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-22)
            self.yr=self.game.draw_text('input:',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-5)
            self.game.draw_text(self.text,self.game.font,20,BLACK,self.rect.left+50,self.rect.y+self.rect.height/2-5)
        if self.color_input:
            self.game.screen.blit(self.color_inp_img,self.rect2)
            self.game.draw_text('RGB:',self.game.font,20,BLACK,self.rect2.left,self.rect2.y+self.rect2.height/2-5)
            self.game.draw_text(self.text_color,self.game.font,20,BLACK,self.rect2.left+50,self.rect2.y+self.rect.height/2-5)

    def update(self):
        self.rect.bottomleft=self.pos
        self.rect2.bottom=self.pos[1]
        self.rect2.left=self.pos[0]+self.rect.width*1.2
    def get_coords(self,pos):
        self.pos=pos



class DerivativeLegend:
    def __init__(self,game,pos,dict):
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//3))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomright=pos
        self.dict=dict
        self.drawing=False
        self.dict_right={}
    def draw(self):
        if self.drawing:
            self.game.screen.blit(self.img,self.rect)
            pg.draw.rect(self.game.screen,BLACK,self.rect,3)
            self.game.draw_text('Derivatives:',self.game.font,20,BLACK,self.rect.left+45,self.rect.y)
            if self.dict:
                height=0
                for key,val in self.dict.items():
                    height+=20
                    if self.dict_right[key]>self.rect.right:
                        self.game.draw_text("-"+" "+str(diff(parse_expr(key),abc.x)),self.game.font,int(20/(self.dict_right[key]/self.rect.right)),BLACK,self.rect.left+45,self.rect.y+height)


                    else:
                        self.game.draw_text("-"+"  "+str(diff(parse_expr(key),abc.x)),self.game.font,20,BLACK,self.rect.left+45,self.rect.y+height)
                        # if str(diff(parse_expr(key),abc.x)) not in self.game.derivative_fns_copy:
                        #     self.game.derivative_fns_copy.append(str(diff(parse_expr(key),abc.x)))
                    pg.draw.rect(self.game.screen,eval(val),pg.Rect(self.rect.left+30,self.rect.y+height+10,10,10))
                    self.game.draw_text(str(list(self.dict.keys()).index(key))+')',self.game.font,20,BLACK,self.rect.left+10,self.rect.y+height)
    def update(self):
        self.rect.topright=self.pos
        height=0
        for key,val in self.dict.items():
            height+=20
            rect=self.game.draw_text("-"+"  "+str(diff(parse_expr(key),abc.x)),self.game.font,20,BLACK,self.rect.left+45,self.rect.y+height)
            self.dict_right[key]=rect.right
    def get_coords(self,pos):
        self.pos=pos


class IntegralManager:
    def __init__(self,game,pos):
        self.drawing=False
        self.game=game
        self.img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.img.fill(WHITE)
        self.rect=self.img.get_rect()
        self.pos=pos
        self.rect.bottomleft=pos
        self.colors={}
        self.der_or_func_input=False
        self.text=''
        self.der_or_func_text=''
        self.der_or_func_img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.der_or_func_img.fill(WHITE)
        self.rect2=self.der_or_func_img.get_rect()
        self.rect.bottomleft=pos
        self.function_input=False
        self.func_text=''
        self.func_img=pg.Surface((WIDTH//5,HEIGHT//20))
        self.func_img.fill(WHITE)
        self.rect3=self.der_or_func_img.get_rect()
    def draw(self):
        if self.drawing:
            self.game.screen.blit(self.img,self.rect)
            yr=self.game.draw_text('Start,End:',self.game.font,20,BLACK,self.rect.left,self.rect.y+self.rect.height/2-10)
            self.game.draw_text(self.text,self.game.font,20,BLACK,yr.right+5,yr.top)
        if self.der_or_func_input:
            self.game.screen.blit(self.der_or_func_img,self.rect2)
            self.game.draw_text('Derivative or f(x):',self.game.font,20,BLACK,self.rect2.left,self.rect2.y+self.rect2.height/2-20)
            rect=self.game.draw_text('(d or f):',self.game.font,20,BLACK,self.rect2.left,self.rect2.y+self.rect2.height/2-3)
            self.game.draw_text(self.der_or_func_text,self.game.font,20,BLACK,rect.right+3,rect.top)
        if self.function_input:
            self.game.screen.blit(self.func_img,self.rect3)
            self.game.draw_text('Choose a function:',self.game.font,20,BLACK,self.rect3.left,self.rect3.y+self.rect3.height/2-20)
            rect=self.game.draw_text('(number):',self.game.font,20,BLACK,self.rect3.left,self.rect3.y+self.rect3.height/2-3)
            self.game.draw_text(self.func_text,self.game.font,20,BLACK,rect.right+3,rect.top)

    def update(self):
        self.rect.bottomleft=self.pos
        self.rect2.bottom=self.pos[1]
        self.rect2.left=self.pos[0]+self.rect.width*1.2
        self.rect3.bottom=self.pos[1]
        self.rect3.left=self.pos[0]+self.rect2.width*1.2+self.rect.width*1.2
    def get_coords(self,pos):
        self.pos=pos

