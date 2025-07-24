import os
import openai
import pyxel
from AIchatBot import AIchatBotTest001
import openai
import PyxelUniversalFont as puf

SCREEN_WIDTH = 1400 #うぃず
SCREEN_HEIGHT = 800 #はいと

dankaibutai = 0#0="終了",1="タイトル",2="メイン".9="オプション"

class xy:#xyクラス
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

#本編
class App:

    #初期化
    def __init__(self):
        self.ai = AIchatBotTest001()

        self.MaxWindowSizeXY = xy(160, 120)
        self.StartXY = xy(70, 60)

        self.FontSize = 30
        self.text = "なにがききたい？"
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT, title="えーあいえーじぇんと")
        pyxel.mouse(True)
        self.writer = puf.Writer("misaki_gothic.ttf")#フォントを指定
        self.number = 0
        pyxel.run(self.update, self.draw)

        pass

    #アプデ
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.text = self.ai_kotae()
            pyxel.mouse_x

       
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
                pass
            case 2:#メイン
                pass
            case 9:#オプション

        pyxel.cls(pyxel.COLOR_BLACK)
#        pyxel.text(50,50, self.text, pyxel.COLOR_YELLOW)
        y = 50
        for HText in HyoujiText:

            self.writer.draw(0,y, HText,self.FontSize, pyxel.COLOR_YELLOW)
            y = y + self.FontSize

        self.writer.draw(0,SCREEN_HEIGHT -200, "ステータス", 25,pyxel.COLOR_WHITE)
        self.writer.draw(0,SCREEN_HEIGHT -200+self.FontSize, "教えたがり",20,pyxel.COLOR_WHITE)

        pass
    
    #ＡＩの答え
    def ai_kotae(self):
#        text = self.ai.response("ツンデレ風","最新の日本の政治の状況")
        text = "こたえ"
        return text

App()

