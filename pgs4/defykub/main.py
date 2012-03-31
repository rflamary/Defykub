#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:09:47 2012

@author: flam
"""


import pygame
#import pygame as pygame
from defykub import *   
#from pgu import gui
try:
    import android
except ImportError:
    android = None
    
imgdir='assets/imgs/'

imglist=['void.png',
         'wall.png',
         'mob.png',
         'targ.png',
         'val.png',
         'mobsel.png',
         'arrows.png',
         'menu.png',
         'won.png',
         'tuto.png']
         
b_arrows=6
b_menu=7
b_won=8
b_tuto=9   

      
param_random={'sx':20,
              'sy':20,
              'nbwall':50,
              'nbtarg':3,
              'nbmob':5,
              'nbactions':20}    

l_menu=0
l_play=1
l_edit=2

loop=l_menu

action_new=pygame.K_g
action_reset=pygame.K_r
action_next=pygame.K_SPACE

irand=1


def load_images():
    res=list()
    for fname in imglist:
        res.append(pygame.image.load(imgdir+fname))
    return res
        

def click_button(event):
    dic=dict(key=event)
    print pygame.event.Event(pygame.KEYDOWN,dic)    
    

#class TopControl(gui.Table):
#           
#    
#    def __init__(self,**params):
#        gui.Table.__init__(self,**params)
#
#        fg = (255,255,255)
#
#        self.tr()
#
#        self.menubut=gui.Button("Menu")
#        
#        self.td(self.menubut,colspan=2)
#        
#        self.newbut=gui.Button("New")
#        
#        self.td(self.newbut,colspan=2)
#
#        self.resbut=gui.Button("Reset")
#        
#        self.td(self.resbut,colspan=2)
#        
#        
#        self.lblcomp=gui.Label("   Complexity: ",color=fg)      
#        
#        self.td(self.lblcomp,colspan=2)
#
#        self.lblnbact=gui.Label("   Nb actions: ",color=fg)      
#        
#        self.td(self.lblnbact,colspan=2)        
        



class game():
    

    
    def __init__(self):
        self.heigth=480
        self.width=800
#        self.heigth=1024
#        self.width=1280
        self.csize=20
        self.xmargin=0
        self.ymargin=0
        
        self.sel=0
        
        self.defy=get_random_defykub(**param_random)
        self.update_const()
#        self.defy=defykub()
#        self.load_from_file('test.xml')

        #set start loop to menu
        self.loop=l_play
        

        self.imgs= load_images()  
        
        self.screen = pygame.display.set_mode((self.width,self.heigth),pygame.SWSURFACE)
        #pygame.display.set_caption("Defykub")
        
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            
#        self.form = gui.Form()
#
#        self.tbar = gui.App()
#        self.tbarctl = TopControl()
#        # new button
#        self.tbarctl.newbut.connect(gui.CLICK,self.generate_new)
#        # reset button
#        self.tbarctl.resbut.connect(gui.CLICK,self.reset_level)   
#        
#        
#        self.c = gui.Container(align=-1,valign=-1)
#        self.c.add(self.tbarctl,0,0)
#        
#        self.tbar.init(self.c)
        
    def change_loop(self,new):
        self.loop=new
        
    def generate_new(self,irand=0):
        self.sel=0
        self.defy=get_random_defykub(seed=irand,**param_random) 
        
    def reset_level(self):
        self.defy=self.defy.defy0
        self.defy.defy0=copy.deepcopy(self.defy)        
        
    def load_from_file(self,fname):
        self.defy.from_file(fname)
        self.update_const()
        
    def update_const(self):
        sx=self.defy.sx
        sy=self.defy.sy       
        
        hx=(self.width)
        hy=(self.heigth)
        
        self.startx=(hx-sx*self.csize)/2-40
        self.starty=(hy-sy*self.csize)/2-20
        
        
    def print_board(self):
        sx=self.defy.sx
        sy=self.defy.sy
        csize=self.csize
        
#        self.tbarctl.lblcomp.set_text("   Compexity: "+str(self.defy.complexity))
#        self.tbarctl.lblnbact.set_text("   Nb actions: "+str(self.defy.nb_actions))
        
        for i in range(sx+2):
            rec=pygame.Rect((self.startx+i*csize,self.starty),(csize,csize))
            self.screen.blit(self.imgs[b_wall], rec)
            
        for j in range(sy):
            rec=pygame.Rect((self.startx,self.starty+(j+1)*csize),(csize,csize))
            self.screen.blit(self.imgs[b_wall], rec)
            for i in range(self.defy.sx):  
                rec=pygame.Rect((self.startx+(i+1)*csize,self.starty+(j+1)*csize),(csize,csize))
                self.screen.blit(self.imgs[self.defy.board[i][j]], rec)
            rec=pygame.Rect((self.startx+(sx+1)*csize,self.starty+(j+1)*csize),(csize,csize))
            self.screen.blit(self.imgs[b_wall], rec)              

        for i in range(sx+2):
            rec=pygame.Rect((self.startx+i*csize,self.starty+(sy+1)*csize),(csize,csize))
            self.screen.blit(self.imgs[b_wall], rec)
        if  self.sel<self.defy.nbmob :            
            x,y=self.defy.mobs[self.sel]
            rec=pygame.Rect((self.startx+(x+1)*csize,self.starty+(y+1)*csize),(csize,csize))
            self.screen.blit(self.imgs[b_mobsel], rec)
        
        # plot arrows
        rec=pygame.Rect((self.width-200,self.heigth/2-100),(200,200))
        self.screen.blit(self.imgs[b_arrows], rec)
        
        # plot menu
        rec=pygame.Rect((0,0),(150,480))
        self.screen.blit(self.imgs[b_menu], rec)     
        
        
    def play_action(self,mob,d):
        self.defy.play_action(mob,d)
        if self.sel>=self.defy.nbmob:
            self.sel=0
            
    def get_action_from_pos(self,pos):
        
        def dist(pos1,pos2):
            return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2
        
        lst1=list()
        # up right down left
        lst1.append((self.width-100,self.heigth/2-100))
        lst1.append((self.width,self.heigth/2))
        lst1.append((self.width-100,self.heigth/2+100))
        lst1.append((self.width-200,self.heigth/2))
        
        vmin=dist(pos,lst1[0])
        res=0
        
        for i,temp in enumerate(lst1):
            if vmin>dist(pos,temp):
                res=i
                vmin=dist(pos,temp)
                
        return res
        
    def finish_loop(self):
        self.screen.fill((0,0,0))
        self.print_board()
        rec=pygame.Rect((0,0),(800,480))
        self.screen.blit(self.imgs[b_won], rec)          
            #self.tbar.paint()
        pygame.display.flip()
        done = False
        while not done:
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            e = pygame.event.wait()  
            
            if e.type == pygame.MOUSEBUTTONDOWN: 
                done=True
        
    def tuto_loop(self):
        self.screen.fill((0,0,0))
        rec=pygame.Rect((0,0),(800,480))
        self.screen.blit(self.imgs[b_tuto], rec)          
            #self.tbar.paint()
        pygame.display.flip()
        done = False
        while not done:
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            e = pygame.event.wait()  
            
            if e.type == pygame.MOUSEBUTTONDOWN: 
                done=True

        
    def game_loop(self):
        done = False
        p_new=((9,self.heigth-413-55),(131,55))
        p_help=((9,self.heigth-345-55),(131,55))
        p_next=((9,self.heigth-173-133),(133,133))
        p_reset=((9,self.heigth-7-133),(133,133))
        def is_inside(pos,rec):
            return (pos[0]>rec[0][0]) and (pos[0]<rec[0][0]+rec[1][0]) and (pos[1]>rec[0][1]) and (pos[1]<rec[0][1]+rec[1][1])

        self.screen.fill((0,0,0))
        self.print_board()
            #self.tbar.paint()
        pygame.display.flip() 
        
        while not done:
            
         
            
            if android:
                if android.check_pause():
                    android.wait_for_resume()
            #e = pygame.event.wait()        
            for e in pygame.event.get():
                #print e
                if e.type is pygame.QUIT: 
                    done = True
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_ESCAPE: 
                    done = True
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_q: 
                    done = True                    
                elif e.type is pygame.KEYDOWN and e.key == action_next: 
                    self.sel=(self.sel+1) % self.defy.nbmob
                elif e.type is pygame.KEYDOWN and e.key == action_reset: 
                    self.reset_level()
                elif e.type is pygame.KEYDOWN and e.key == action_new: 
                    self.generate_new()   
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_RIGHT: 
                    self.play_action(self.sel,d_right) 
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_DOWN: 
                    self.play_action(self.sel,d_down) 
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_LEFT: 
                    self.play_action(self.sel,d_left) 
                elif e.type is pygame.KEYDOWN and e.key == pygame.K_UP: 
                    self.play_action(self.sel,d_up) 
                elif e.type == pygame.MOUSEBUTTONDOWN:  
                    if e.pos[0]>self.width-250:          
                        action=self.get_action_from_pos(e.pos)
                        self.play_action(self.sel,action) 
                    elif is_inside(e.pos,p_next):
                        self.sel=(self.sel+1) % self.defy.nbmob
                    elif is_inside(e.pos,p_reset):
                        self.reset_level()
                    elif is_inside(e.pos,p_help):
                        self.tuto_loop()    
                    elif is_inside(e.pos,p_new):
                        self.generate_new()

#                else:
#                    self.tbar.event(e)

            self.screen.fill((0,0,0))
            self.print_board()
            #self.tbar.paint()
            pygame.display.flip()   
            
            if self.defy.finished():
                self.finish_loop()
                self.sel=0
                self.defy=get_random_defykub(**param_random)                
                
def main():
    gm=game()
    gm.game_loop()	
            
            

if __name__ == "__main__":
    gm=game()
    gm.game_loop()
