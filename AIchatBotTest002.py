import os
import openai
import pyxel
from AIchatBot import AIchatBotTest001
import openai
import PyxelUniversalFont as puf

SCREEN_WIDTH = 1400 #うぃず
SCREEN_HEIGHT = 800 #はいと

dankaibutai = 0#0="終了",1="タイトル",2="メイン".9="オプション"
dankaibutai = 1


class xy:#xyクラス
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

class hantei:
    def __init__(self, x,y, sizeX, sizeY):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        pass
    def hantei(self, x, y):
        flag = False
        if x > self.x and x < self.x + self.sizeX:
            if y > self.y and y < self.y + self.sizeY:
                flag = True

        return flag
        
#作成予定クラス
#文字列と文字サイズを引数にして文字を中央に表示する座標を戻り値にする
#本編
class App:

    #初期化
    def __init__(self):
        self.ai = AIchatBotTest001()

        self.MaxWindowSizeXY = xy(160, 120)
        self.StartXY = xy(70, 60)
        self.CursorXY = xy(300-50,400+50)
        self.CursorSize = 50 -10
        self.AnimetionCursor = 0
        self.hanten = 1

        self.FontSize = 30
        self.text = "なにがききたい？"
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT, title="えーあいえーじぇんと")
        pyxel.mouse(True)
        self.writer = puf.Writer("misaki_gothic.ttf")#フォントを指定
        self.number = 0



#判定つくり
#initに送る
        self.selecttaitle = 0
        self.titelselecthantei = []
        x = 300
        y = 400
        for i in range(3):

            self.titelselecthantei.append(hantei(x, y, 60, 20))
            y = y + 50

        pyxel.run(self.update, self.draw)

        pass

    #アプデ
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.text = self.ai_kotae()
            pyxel.mouse_x

        #マウス判定
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        no = 0
        for i in self.titelselecthantei:
            if i.hantei(x,y):
                self.selecttaitle = no

            no = no + 1

        pass
    
    #表示
    #0=終了
    #1=タイトル
    #2=メイン
    def draw(self):
        HyoujiText = []
        susumu = 0
        gyosize = int(SCREEN_WIDTH / self.FontSize)


        while len(self.text) > susumu + gyosize:
            HyoujiText.append(self.text[susumu:susumu + gyosize])
            susumu = susumu + gyosize
        HyoujiText.append(self.text[susumu:-1])

        match dankaibutai:
            case 0:#終了
                pass
            case 1:#タイトル



                mojiretu = "始める","終わる","設定"
                pyxel.cls(pyxel.COLOR_DARK_BLUE)
                self.writer.draw(100,100, "AIエージェント", 150,pyxel.COLOR_WHITE)
                y = 50
                for i in mojiretu:
                    self.writer.draw(300,400 + y, i, 50,pyxel.COLOR_WHITE)
                    y = y + 50
                
                #カーソル関係

                x = 300 - 50
                y = 400 + 50
                pyxel.rect(x, y + (50 * self.selecttaitle) -10, 50 -10, 50 -10 , 8)
                self.writer.draw(0,0,f"{self.selecttaitle=} {pyxel.mouse_x=} { pyxel.mouse_y=}", 30, pyxel.COLOR_BLACK)

                pass
            case 2:#メイン
                pyxel.cls(pyxel.COLOR_BLACK)
                
                y = 50
                for HText in HyoujiText:
                    self.writer.draw(0,y, HText,self.FontSize, pyxel.COLOR_YELLOW)
                    y = y + self.FontSize
                self.writer.draw(0,SCREEN_HEIGHT -200, "ステータス", 25,pyxel.COLOR_WHITE)
                self.writer.draw(0,SCREEN_HEIGHT -200+self.FontSize, "教えたがり",20,pyxel.COLOR_WHITE)
                pass
            case 9:#オプション
                pass

#        pyxel.text(50,50, self.text, pyxel.COLOR_YELLOW)


        pass
    
    #ＡＩの答え
    def ai_kotae(self):
#        text = self.ai.response("ツンデレ風","最新の日本の政治の状況")
        text = "こたえ"
        return text

App()

