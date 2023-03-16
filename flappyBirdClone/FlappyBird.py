import pygame
import os
import random

tela_largura = 500
tela_altura = 800

img_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
img_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
img_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imgs_passaro = [
            pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()

fonte_pontos = pygame.font.SysFont('arial', 30)

class Passaro:
    imgs = imgs_passaro
    # animações da rotação
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.img = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        #angulo do passo
        if deslocamento < 0 or self.y (self.altura + 50):
            if self.altura < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):
        # definir a imagem do passaro a ser utilizada
        self.contagem_img += 1

        if self.contagem_img < self.tempo_animacao:
            self.img = self.imgs[0]
        elif self.contagem_img < self.tempo_animacao*2:
            self.img < self.imgs[1]
        elif self.contagem_img < self.tempo_animacao*3:
            self.img = self.imgs[2]
        elif self.contagem_img < self.tempo_animacao*4:
            self.img = self.imgs[1]
        elif self.contagem_img >= self.tempo_animacao*4 + 1:
            self.img = self.imgs[0]
            self.contagem_img = 0

        # se o pássaro cair, não bater asa
        if self.angulo <= -80:
            self.img = self.imgs[1]
            self.contagem_img = self.tempo_animacao*2

        # desenhar a imagem
        img_rotacionada = pygame.transform.rotate(self.img, self.angulo)
        pos_centro_img = self.img.get_rect(topleft=(self.x, self.y)).center
        retangulo = img_rotacionada.get_rect(center=pos_centro_img)
        tela.blit(img_rotacionada, retangulo.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.img)
        
class Cano:
    distancia = 200
    velocidade = 5

    def __int__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(img_cano, False, True)
        self.cano_base = img_cano
        self.passou = False
        self.definir_altura()
    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_base = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask - passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro.mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro.mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = img_chao.get_width()
    imagem = img_cano

    def __int__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x1 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x2 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(img_fundo, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = fonte_pontos.render(f"Pontuação: {pontos}", 1, (255,255,255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_largura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()()


        desenhar_tela(tela, passaros, canos, chao, pontos)