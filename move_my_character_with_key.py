from typing import List, Any
from pico2d import *
import string
from random import *
from enum import Enum, auto
from time import *


#2020182009


'''
==README==

화살표 상,하,좌,우 로 움직입니다 

'''

BackGround_Width, BackGround_Height = 1280, 1024

open_canvas(BackGround_Width, BackGround_Height)

BackGround = load_image("TUK_GROUND.png")



running = True


class Timer:
    pass


class Image:
    def __init__(self, path=string, frame=int, width=int, height=int):
        # 이미지 이름
        self.Path = path
        # 스프라이트의 총 프레임 수
        self.Frame = frame
        # 스프라이트의 단위 가로 길이
        self.Width = width

        # 스프라이트의 단위 세로 길이
        self.Height = height


class Behavior(Enum):
    Idle = auto()
    Run = auto()

class arrow:
    def __init__(self,path = string,x = int,y=  int):
        self.Object = load_image(path)
        self.x = x;
        self.y = y;



    def Render(self):
        self.Object.draw(self.x,self.y)

    def GetPosition(self):
        return (self.x,self.y)








class Character:
    def __init__(self, DefaultImg=Image):
        self.IdleImage = DefaultImg
        self.RunImage = None
        self.CurrentImage = DefaultImg
        self.Object = load_image(DefaultImg.Path)
        self.FrameCount = 0
        self.DirectionX = 0
        self.DirectionY = 0
        self.x = 400
        self.y = 400
        self.speed = 5
        self.isComposite = False
        self.State = Behavior.Idle.name


        self.OldX = 0
        self.OldY = 0
        self.T              = 0.0
        self.isDestinating  = False





    def ChangeBehavior(self, TargetBehavior=Behavior):
        if TargetBehavior == Behavior.Idle.name:
            self.FrameCount = 0
            if self.State == Behavior.Run.name:
                if self.IdleImage is not None:
                    self.CurrentImage = self.IdleImage
                    self.State = "Idle"




        elif TargetBehavior == Behavior.Run.name:
            if self.State == Behavior.Idle.name:
                self.FrameCount = 0
                if self.RunImage is not None:
                    self.CurrentImage = self.RunImage
                    print("Run")
                    self.State = "Run"





        self.Object = load_image(self.CurrentImage.Path)




    def NextCoordinate(self,Ar = arrow):
        if Ar == None:
            return
        if not self.isDestinating:
            self.OldX = self.x
            self.OldY = self.y

            self.isDestinating = True

            self.ChangeBehavior("Run")


        x2 = Ar.GetPosition()[0]
        y2 = Ar.GetPosition()[1]

        if self.x > x2 :
            self.isComposite = True
        else :
            self.isComposite = False



        if 0.0 <=  self.T < 0.3:
            self.T += 0.003
        elif 0.3 <= self.T < 0.6:
            self.T += 0.07
        elif 0.6 <= self.T < 1.0:
            self.T += 0.01


        self.x  = (1-self.T)*self.OldX + self.T * x2
        self.y  = (1-self.T)*self.OldY + self.T * y2


        if self.T >= 1:
            self.T = 0
            self.isDestinating = False
            self.OldX = 0
            self.OldY = 0
            return True

        return False

    def GetCenterCoordinate(self):
        print(  (self.x - self.CurrentImage.Width / 2 , self.y - self.CurrentImage.Height / 2)  )
        return (self.x - self.CurrentImage.Width / 2 , self.y - self.CurrentImage.Height / 2)



    def ResisterRunImage(self,runImage = Image):
        self.RunImage = runImage


    def Draw(self,Scale=int):

        self.FrameCount = (self.FrameCount + 1) % self.CurrentImage.Frame

        self.x = clamp(20,self.x,get_canvas_width())
        self.y = clamp(20,self.y,get_canvas_height())

        DrawX = self.x
        DrawY = self.y + self.CurrentImage.Height



        if not self.isComposite:
            self.Object.clip_draw(
                self.CurrentImage.Width * self.FrameCount,
                0,
                self.CurrentImage.Width,
                self.CurrentImage.Height,
                DrawX,
                DrawY,
                150 * Scale,
                100 * Scale
            )
        elif self.isComposite:
            self.Object.clip_composite_draw(
                self.CurrentImage.Width * self.FrameCount,
                0,
                self.CurrentImage.Width,
                self.CurrentImage.Height,
                0,
                'h',
                DrawX,
                DrawY,
                150 * Scale,
                100 * Scale,
            )

def HandleEvent(Events = List[Any]):
    global running


    for event in Events:
        if event.type == SDL_QUIT:
            running = False
            return
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                return






Character_IdleImage = Image("_Idle.png", 10, 120, 80)
Character_RunImage = Image("_Run.png", 10, 120, 80)



MainCharacter = Character(Character_IdleImage)
MainCharacter.ResisterRunImage(Character_RunImage)


Arrow = arrow("hand_arrow.png",randint(0,1280),randint(0,1024))


Arrows: List[Any] = []
EventList: List[Any] = []

MainCharacter.x = 640
MainCharacter.y = 512

# Main Process
while running:
    clear_canvas()
    EventList = get_events()
    BackGround.draw(BackGround_Width // 2, BackGround_Height // 2)
    # Calculate Between here

    if MainCharacter.NextCoordinate(Arrow):
        Arrow = arrow("hand_arrow.png",randint(0,1280),randint(0,1024))


    # Calculate Between here
    # Draw between here


    MainCharacter.Draw(4)
    Arrow.Render()

    # Draw between here
    delay(0.05)
    HandleEvent(EventList)
    update_canvas()
