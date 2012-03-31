#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:59:27 2012

@author: flam
"""


#from configobj import ConfigObj
try:
    import xml.etree.ElementTree as xml
except ImportError:
    xml = None    
import random as rd
import copy
from operator import itemgetter, attrgetter

b_void=0
b_wall=1
b_mob=2
b_targ=3
b_val=4
b_mobsel=5

  
d_up=0
d_right=1
d_down=2
d_left=3

charboard=[' ','#','O','X','V','0']

svg_styles=['fill:white;stroke:black;stroke-width:1',
            'fill:#A05A2C;stroke:black;stroke-width:1',
            'fill:#0000FF;stroke:black;stroke-width:1',
            'fill:#FF0000;stroke:black;stroke-width:1',
            'fill:#FF6600;stroke:black;stroke-width:1',
            'fill:#00FF00;stroke:black;stroke-width:1',
            ]

depthmaxsearch=5


def get_random_defykub(sx=20,sy=10,nbwall=30,nbtarg=2,nbmob=2,nbactions=20,seed=0):
    res=defykub()
    #seed=4
    if seed:
        rd.seed(seed)
    
    def gen_walls():
        while res.nbwall<nbwall:
            x=rd.randint(0,sx-1)
            y=rd.randint(0,sy-1)
            if res.board[x][y]==b_void:
                res.board[x][y]=b_wall
                res.nbwall+=1
                res.walls.append((x,y))
                
    
                
    def gen_targsmobs(nbtarg,nbmob):   
        
        lst=list()
        depth=list()
        
        # list potential target spaces
        for x in range(sx-2):
            for y in range(sy-2):
                i=x+1
                j=y+1
                if res.potential_start(i,j):
                    lst.append((i,j))
                    depth.append(res.depth_cell_min(i,j,depthmaxsearch))
        #print "lst:",lst
        #print "depth:",depth                    

        # handle lack of places
        if len(lst)<nbtarg:
            nbmob=nbmob-nbtarg-len(lst)-1
            nbtarg=len(lst)
        
        # add places randomly
        while res.nbtarg<nbtarg:
            #t=rd.randint(0,len(lst)-1)
            t,dtemp=max(enumerate(depth),key=itemgetter(1))
            #print "dtemp:",dtemp
            x,y=lst.pop(t)
            depth.pop(t)
            if res.potential_start(x,y):               
                res.board[x][y]=b_val
                res.targs.append((x,y))
                res.nbtarg+=1
                res.mobs.append((x,y))
                res.nbmob+=1
            
#            depth=list()
#            for i,j in lst:
#                depth.append(res.depth_cell_min(i,j,depthmaxsearch))
        
        lst=list()
        
        # get potential mobile places
        for x in range(sx-2):
            for y in range(sy-2):
                i=x+1
                j=y+1
                if res.board[i][j]==b_void:
                    lst.append((i,j))
                    
        # create mobiles            
        while res.nbmob<nbmob:
            t=rd.randint(0,len(lst)-1)
            x,y=lst.pop(t)
            res.board[x][y]=b_mob
            res.mobs.append((x,y))
            res.nbmob+=1 
            
    def move_mobs():
        res.cactions=list()        
        
        moving=[1 for i in range(res.nbmob)]
        forbidendir=[5 for i in range(res.nbmob)] 
        
        nbmoving=res.nbmob
        #print nbactions
        
        while len(res.cactions)<nbactions:
            sel=0
            tmp=rd.randint(0,nbmoving-1)
            
            # select a moving mobile
            ind=[i for i, e in enumerate(moving) if e != 0]
            sel=ind[tmp]
            
            #print "sel:",sel
            #print moving
            
            i,j=res.mobs[sel]            
            

            #print i,j
            
            d=res.potential_dir(i,j,forbidendir[sel])
                        
            
            dinv=d+2 % 4
            
            #print "d:",d
            
            
            if True: # if possible direction
            # list possible  spaces for continuing or stop (lst0)
                lst,lst0=res.list_cells_in_dir(i,j,d)
                #print "lst:",lst
                #print "lst0:",lst0
           
                # select and move mobile
                if len(lst):
                    #print "encours"
                    t=rd.randint(0,len(lst)-1)
                    res.mobs[sel]=lst[t]               
                else:
                    #print "stop"
                    if len(lst0)>1:
                        t=rd.randint(0,len(lst0)-1)
                    else: 
                        t=0
                    if len(lst0):
                        res.mobs[sel]=lst0[t]    
                        moving[sel]=0
                        nbmoving-=1
                    
                forbidendir[sel]=dinv
                
                res.cactions.append((sel,dinv))
            
            # check if targets are alone now
            res.update_board()

            #print res.mobs
            #print res.targs
            #res.print_board()  
            
            test=0
            for temp in moving:
                test+=temp
            if not test:
                break
            
    # init defykub
    res.sx=sx
    res.sy=sy 
    res.board= [[b_void for i in range(res.sy)] for j in range(res.sx)]
    
    # Ego boost
    res.name="Random "+str(seed)
    res.author="Flam's random generator"
    
    gen_walls()
    #res.print_board()
    gen_targsmobs(nbtarg,nbmob)
    #res.print_board()
    move_mobs()
    
    res.clean_done()
    res.update_board()
    rd.shuffle(res.mobs)
    
    res.complexity=len(res.cactions)
    
    res.defy0=copy.deepcopy(res)
    
    return res    
    
    




class defykub:
    def __init__(self):
        self.sx=0
        self.sy=0
        self.nbmob=0
        self.nbtarg=0
        self.nbwall=0
        
        self.nbval=0
        
        self.mobs=list()
        self.targs=list()
        self.walls=list()
        self.vals=list()
        
        self.name="level"
        self.author="author"
        
        
        self.board=[]
        self.old=b_void
        
        self.complexity=0
        self.cactions=list()
        self.sactions=list()
        
        
        self.nb_actions=0
        self.actions=list()
        
        self.svgw=30
        
    def from_string(self,string):
        
        level = xml.fromstring(string)
        self.level=level
        
        self.name=level.find('header').find('title').text
        self.author=level.find('header').find('author').text
        
        self.sx=int(level.find('description').attrib['sx'])
        self.sy=int(level.find('description').attrib['sy'])
        
        self.board= [[b_void for i in range(self.sy)] for j in range(self.sx)]
        
        self.mobs=list()
        self.targs=list()
        self.walls=list()
        self.vals=list()

        self.nbmob=0
        self.nbtarg=0
        self.nbwall=0
        self.nbval=0
        
        for item in level.findall("description/mobs/m"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_mob
            self.mobs.append((int(x),int(y)))
            self.nbmob+=1   

            
        for item in level.findall("description/targs/t"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_targ
            self.targs.append((int(x),int(y)))
            self.nbtarg+=1
            
        for item in level.findall("description/walls/w"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_wall
            self.walls.append((int(x),int(y)))
            self.nbwall+=1    
            
        for item in level.findall("description/vals/v"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_val
            self.vals.append((int(x),int(y)))
            self.nbval+=1               
        
        self.defy0=copy.deepcopy(self)
            
    def from_file(self,fname):
        level = xml.parse(fname)
        self.level=level
        
        self.name=level.find('header').find('title').text
        self.author=level.find('header').find('author').text
        
        self.sx=int(level.find('description').attrib['sx'])
        self.sy=int(level.find('description').attrib['sy'])
        
        self.board= [[b_void for i in range(self.sy)] for j in range(self.sx)]
        
        self.nbmob=0
        self.nbtarg=0
        self.nbwall=0
        self.nbval=0
        
        self.mobs=list()
        self.targs=list()
        self.walls=list()
        self.vals=list()        
        
        for item in level.findall("description/mobs/m"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_mob
            self.mobs.append((int(x),int(y)))
            self.nbmob+=1   

            
        for item in level.findall("description/targs/t"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_targ
            self.targs.append((int(x),int(y)))
            self.nbtarg+=1
            
        for item in level.findall("description/walls/w"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_wall
            self.walls.append((int(x),int(y)))
            self.nbwall+=1    

        for item in level.findall("description/vals/v"):
            x=item.attrib['x']
            y=item.attrib['y']
            self.board[int(x)][int(y)]=b_val
            self.vals.append((int(x),int(y)))
            self.nbval+=1         
        
        self.defy0=copy.deepcopy(self)
        
    def update_board(self):
        
        self.board= [[b_void for i in range(self.sy)] for j in range(self.sx)]
            
        for i,j in self.walls:
            self.board[i][j]=b_wall  
        
        for i,j in self.mobs:
            self.board[i][j]=b_mob
            
        for i,j in self.targs:
            self.board[i][j]=b_targ     
 
        for i,j in self.vals:
            self.board[i][j]=b_val  
            
        for i,targ in enumerate(self.targs):
            for j,mob in enumerate(self.mobs):
                isupon=False
                if mob==targ:
                    isupon=True
                    itemp=i
                    jtemp=j
                    
            if isupon:
                x,y=targ
                self.board[x][y]=b_val

                
    def to_xml(self,selected=0):
        
        level = xml.Element('level')
        
        header=xml.Element('header')
        level.append(header)
        title=xml.SubElement(header, "title")
        title.text=self.name
        auth=xml.SubElement(header, "author")
        auth.text=self.author
        
        desc=xml.Element('description',sx=str(self.sx),sy=str(self.sy))
        level.append(desc)
        
        xmobs=xml.SubElement(desc, "mobs")
        for x,y in self.mobs:
            xml.SubElement(xmobs, "m",x=str(x),y=str(y))
        
        xwalls=xml.SubElement(desc, "walls")
        for x,y in self.walls:
            xml.SubElement(xwalls, "w",x=str(x),y=str(y))
        
        xtargs=xml.SubElement(desc, "targs")
        for x,y in self.targs:
            xml.SubElement(xtargs, "t",x=str(x),y=str(y))

        xvals=xml.SubElement(desc, "vals")
        for x,y in self.vals:
            xml.SubElement(xvals, "v",x=str(x),y=str(y))
        
        return level
            
    def to_string(self):
        
        temp= self.to_xml()
        return xml.tostring(temp)
            
    def to_file(self,fname):
        
        level=self.to_xml()
            
        self.level=level
        
        file = open(fname,'w')
        xml.ElementTree(level).write(file)
        
    def get_svg(self,selected=0):
        
        svg = xml.Element('svg',xmlns="http://www.w3.org/2000/svg",version="1.1",width=str(self.svgw*(self.sx+2)),height=str(self.svgw*(self.sy+2)))
        
        for x in range(self.sx+2):
            xml.SubElement(svg, "rect",x=str(x*self.svgw),y=str(0),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_wall])
            xml.SubElement(svg, "rect",x=str(x*self.svgw),y=str((self.sy+1)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_wall])

        for y in range(self.sy+2):
            xml.SubElement(svg, "rect",x=str(0),y=str(y*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_wall])
            xml.SubElement(svg, "rect",x=str((self.sx+1)*self.svgw),y=str((y)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_wall])
            
        for x in range(self.sx):
            for y in range(self.sy):
                xml.SubElement(svg, "rect",x=str((x+1)*self.svgw),y=str((y+1)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_void])
                
        for x,y in self.walls:
            xml.SubElement(svg, "rect",x=str((x+1)*self.svgw),y=str((y+1)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_wall])

        for x,y in self.mobs:
            xml.SubElement(svg, "circle",cx=str((x+1)*self.svgw+self.svgw/2),cy=str((y+1)*self.svgw+self.svgw/2),r=str(self.svgw/2),style=svg_styles[b_mob])
            
        for x,y in self.targs:
            xml.SubElement(svg, "rect",x=str((x+1)*self.svgw),y=str((y+1)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_targ])

        for x,y in self.vals:
            xml.SubElement(svg, "rect",x=str((x+1)*self.svgw),y=str((y+1)*self.svgw),width=str(self.svgw),height=str(self.svgw),style=svg_styles[b_val])
        
        if len(self.mobs):
            x,y=self.mobs[selected]
            xml.SubElement(svg, "circle",cx=str((x+1)*self.svgw+self.svgw/2),cy=str((y+1)*self.svgw+self.svgw/2),r=str(self.svgw/2),style=svg_styles[b_mobsel])
        
        return xml.tostring(svg) 
            
    def passing_cell(self,t):
        return t==b_void or t==b_targ
        
    def passing_next_cell(self,i,j,d):
        return self.passing_cell(self.safe_board_pos(self. next_cell(i,j,d)))
        
    def next_cell_type(self,mob=0,d=0):
        i,j=self.mobs[mob]
        i,j=self.next_cell(i,j,d)
        if i>=self.sx or i<0 or j>= self.sy or j<0:
            return b_wall
        else:
            return self.board[i][j]
            
    def depth_cell_min(self,i,j,depthmax):
        #print depthmax
        if depthmax<=0:
            return 0
        else:
            lst,lst0=self.list_cells_in_dir(i,j,self.potential_dir(i,j))
            if not len(lst):
                return 0
            else:
                depth=list()
                for i,j in lst:
                    depth.append(self.depth_cell_min(i,j,depthmax-1))
                return min(depth)+1
            
        
            
    def is_border(self,pos):
        i,j=pos
        if i>=self.sx-1 or i<=0 or j>= self.sy-1 or j<=0:
            return True
        else:
            return False       
            
    def safe_board(self,i,j):
        if i>=self.sx or i<0 or j>= self.sy or j<0:
            return b_wall
        else:
            return self.board[i][j]     
            
    def safe_board_pos(self,pos):
        i,j=pos
        return self.safe_board(i,j)
            
    def passing_neighboor(self,i,j,d):
        i,j=self.next_cell(i,j,d)
        return self.passing_cell(self.safe_board(i,j))
            
    def potential_start(self,i,j):
        return (self.passing_neighboor(i,j,d_up) ^ self.passing_neighboor(i,j,d_down)) or (self.passing_neighboor(i,j,d_left) ^ self.passing_neighboor(i,j,d_right))
        
    def list_cells_in_dir(self,i,j,d):
        lst=list()
        lst0=list()      
        # list possible  spaces for continuing or stop (lst0)
        if d<=3:
            while self.passing_next_cell(i,j,d):
                i,j=self.next_cell(i,j,d)
                if self.potential_start_dir(i,j,d):
                    lst.append((i,j))
                if self.safe_board(i,j)==b_void:
                    lst0.append((i,j))
        return lst,lst0

    def potential_start_dir(self,i,j,d):
        d=(d+1) % 4
        d2=(d+2) % 4
        return self.board[i][j]==b_void and(self.passing_neighboor(i,j,d) ^ self.passing_neighboor(i,j,d2))
    
    def potential_dir(self,i,j,forbid=4):
        if self.passing_cell(self.safe_board_pos(self.next_cell(i,j,d_up))) and not self.passing_cell(self.safe_board_pos(self. next_cell(i,j,d_down))) and not forbid==d_up:
            res=(d_up)
        elif self.passing_cell(self.safe_board_pos(self.next_cell(i,j,d_down))) and not self.passing_cell(self.safe_board_pos(self. next_cell(i,j,d_up))) and not forbid==d_down:
            res=(d_down)
        elif self.passing_cell(self.safe_board_pos(self.next_cell(i,j,d_left))) and not self.passing_cell(self.safe_board_pos(self. next_cell(i,j,d_right))) and not forbid==d_left:
            res=(d_left)
        elif self.passing_cell(self.safe_board_pos(self.next_cell(i,j,d_right))) and not self.passing_cell(self.safe_board_pos(self. next_cell(i,j,d_left)))and not forbid==d_right:
            res=(d_right)
        else: res=forbid
        return res
        
    def next_cell(self,i,j,d):
        if d==d_up:
            j=j-1
        elif d==d_right:
            i=i+1
        elif d==d_down:
            j=j+1
        elif d==d_left:
            i=i-1
        return i,j
        
    def id_from_pos(self,i,j,t):
        res=-1
        id=0
        if t==b_targ:
            for x,y in self.targs:
                if x==i and y==j:
                    res=id
                id+=1
        elif t==b_mob:
            for x,y in self.mobs:
                if x==i and y==j:
                    res=id
                id+=1
        elif t==b_wall:
            for x,y in self.walls:
                if x==i and y==j:
                    res=id
                id+=1           
        elif t==b_val:
            for x,y in self.vals:
                if x==i and y==j:
                    res=id
                id+=1
        #print res
        return res       

            
    def play_action(self,mob,d):
        old=b_void
        self.nb_actions+=1
        self.actions.append((mob,d))
        while self.passing_cell(self.next_cell_type(mob,d)):
            i,j=self.mobs[mob]
            self.board[i][j]=old
            i,j=self.next_cell(i,j,d)
            old=self.board[i][j]
            self.board[i][j]=b_mob
            self.mobs[mob]=(i,j)
        if old==b_targ:
            self.mobs.pop(mob)
            itemp =self.id_from_pos(i,j,b_targ)
            #print len(self.targs)
            self.targs.pop(itemp)
            self.vals.append((i,j))
            self.nbval+=1
            self.nbmob=self.nbmob-1
            self.nbtarg=self.nbtarg-1
            self.board[i][j]=b_val
            
    def clean_done(self):
        lst=list()
        for i,targ in reversed(list(enumerate(self.targs))):
            for j,mob in enumerate(self.mobs):
                if targ==mob:
                    self.mobs.pop(j)
                    self.nbmob-=1   
                    lst.append(i)

        for i in lst:
            self.vals.append(self.targs.pop(i))
            self.nbtarg-=1
            self.nbval+=1
            
        lst=list()    
        for i,targ in enumerate(self.targs):
            for j,wall in enumerate(self.walls):
                if targ==wall:
                    self.walls.pop(j)
                    self.nbwall-=1                    

           
    def finished(self):
        return self.nbtarg==0
        
    def print_board(self,board=None):
        if board==None:
            board=self.board
        for i in range(self.sx+2):
            print charboard[b_wall],
        print
        for j in range(self.sy):
            print charboard[b_wall],
            for i in range(self.sx):
                print charboard[board[i][j]],
            print charboard[b_wall]
        for i in range(self.sx+2):
            print charboard[b_wall],
        print            
    
    def print_board_selected(self,mob=0,board=None):
        if board==None:
            board=copy.deepcopy(self.board)
        if self.sx and self.sy and mob<self.nbmob:
            x,y=self.mobs[mob]
            board[x][y]=b_mobsel
        for i in range(self.sx+2):
            print charboard[b_wall],
        print
        for j in range(self.sy):
            print charboard[b_wall],
            for i in range(self.sx):
                print charboard[board[i][j]],
            print charboard[b_wall]
        for i in range(self.sx+2):
            print charboard[b_wall],
        print           
        
    
        




if __name__ == "__main__":
    #print 'defykub'
    param_random={'sx':20,
              'sy':20,
              'nbwall':50,
              'nbtarg':3,
              'nbmob':3,
              'nbactions':20}  
    defy = defykub()
#    for i in range(100):
#        seed=i#14
#        defy=get_random_defykub(seed=seed,**param_random)
#        if not defy.nbmob==defy.nbtarg:
#            print i
    seed=0#14
    defy=get_random_defykub(seed=seed,**param_random)    
    #defy.load_level('test.dfk')
    defy.print_board()  
    
#    defy.play_action(0,d_down)
#    defy.print_board()  
#    temp=defy.to_string()
#    print temp
#    defy.from_string(temp)
#    defy.print_board()      
#    
    
    #print defy.to_string()
        
    
