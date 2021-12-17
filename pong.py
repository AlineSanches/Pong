from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *

janela = Window(800,600)  # instancia o objeto janela como classe window pelo construtor Window
janela.set_title("Pong")  # outro método da classe janela

fundo = GameImage("img/sunset.jpg")  # instancia o objeto fundo como gameimage pelo método construtor GameImage
bola = Sprite("img/bola.png", 1)  # 1 para a quantidade de frames do sprite
padD = Sprite("img/pad.png", 1)
padE = Sprite("img/pad.png", 1)

# define as coordenadas da bola no meio da tela, independentemente da resolução
bola.set_position(janela.width/2 - bola.width/2, janela.height/2 - bola.height/2)

# define as coordenadas dos pads
padE.set_position(10, janela.height/2 - padE.height/2)
padD.set_position(janela.width - padD.width - 10, janela.height/2 - padD.height/2)

# variáveis de velocidade
velBolaX = 220
velBolaY = 190
velPad = 230

# variáveis de contagen
pontosE = 0
pontosD = 0
countColisao = 0
countTempo = 0
countFrame = 0
frameRate = 0

# variável do teclado
teclado = Window.get_keyboard()

# gameloop
while True:
    # entrada de dados
    # método que retorna True ou False caso a tecla seja pressionada para mover o pad do jogador
    # (e não passa dos limites superior e inferior)
    if teclado.key_pressed("UP") and padD.y >= 0:
        padD.y -= velPad * janela.delta_time()
    if teclado.key_pressed("DOWN") and padD.y <= janela.height-padD.height:
        padD.y += velPad * janela.delta_time()

    # Update
    # atualiza a posicao da bola de acordo com as variaveis de velocidade
    bola.set_position(bola.x + velBolaX * janela.delta_time(), bola.y + velBolaY * janela.delta_time())
    # delta time para homogeneizar a velocidade independentemente do frame rate

    # IA do pad esquerdo
    if velBolaY > 0 and padE.y <= janela.height-padE.height:
        padE.y += velPad * janela.delta_time()
    elif velBolaY < 0 and padE.y >= 0:
        padE.y -= velPad * janela.delta_time()

    # atualiza a variável de tempo e frame para contabilizar o frame rate
    countTempo += janela.delta_time()
    countFrame += 1
    if countTempo >= 1:
        frameRate = countFrame
        countTempo = 0
        countFrame = 1

    # define a volta da bolinha caso colida com algum pad, e coloca ela necessariamente de forma que não colida de novo
    if bola.collided(padD) or bola.collided(padE):
        countColisao += 1
        if bola.collided(padD):
            bola.x = padD.x-bola.width
        else:
            bola.x = padE.x+padE.width
        # caso tenha 4 colisões, divide o pad do jogador pela metade e volta à posição anterior
        if countColisao == 4:
            coordsAnterioresPad = (padD.x, padD.y)
            padD = Sprite("img/padMetade.png", 1)
            padD.set_position(coordsAnterioresPad[0], coordsAnterioresPad[1])
        velBolaX *= -1

    # define a volta da bolinha caso chegue no canto superior ou inferior
    if bola.y + bola.height >= janela.height or bola.y <= 0:
        if bola.y <= 0:
            bola.y = 0
        else:
            bola.y = janela.height-bola.height
        velBolaY *= -1

    # define a contagem dos pontos e redefine as coordenadas da bolinha pro centro caso a bola saia
    if bola.x + bola.width >= janela.width or bola.x <= 0:
        if bola.x <= 0:
            pontosD += 1
        else:
            pontosE += 1
        # caso o pad do jogador esteja menor, volta ao normal
        if countColisao >= 4:
            coordsAnterioresPad = (padD.x, padD.y)
            padD = Sprite("img/pad.png", 1)
            padD.set_position(coordsAnterioresPad[0], coordsAnterioresPad[1])
        countColisao = 0
        bola.set_position(janela.width / 2 - bola.width / 2, janela.height / 2 - bola.height / 2)

    # desenho
    fundo.draw()
    bola.draw()
    padD.draw()
    padE.draw()
    janela.draw_text(str(pontosE), 150, 0, size=50, color=(0,0,0), font_name="Arial", bold=True, italic=False)
    janela.draw_text(str(pontosD), janela.width-180, 0, size=50, color=(0,0,0), font_name="Arial", bold=True, italic=False)
    janela.draw_text("fps: "+str(frameRate), janela.width-100, 0, size=20, color=(0,0,0), font_name="Arial", bold=False, italic=True)
    janela.update()  # faz o update da janela
