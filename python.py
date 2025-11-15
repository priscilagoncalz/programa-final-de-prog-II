# programa-final-de-prog-II
jogo quiz imersivo

# IMPORTAÇÃO DE BIBLIOTECAS

import pygame  
# Biblioteca principal para criação de jogos em Python.
# Fornece recursos para gráficos, sons, eventos e janelas.

from pyvidplayer2 import Video  
# Biblioteca secundária utilizada para reproduzir vídeos dentro de janelas Pygame.
# Permite inserir cenas narrativas ou cutscenes no jogo.

import os  
# Biblioteca padrão do Python que fornece funções de interação
# com o sistema operacional, como manipulação de diretórios,
# caminhos de arquivos e variáveis de ambiente.

import sys  
# Módulo que permite acessar funções e variáveis internas do
# interpretador Python, como parâmetros passados pela linha de
# comando e finalização controlada do programa.

import random  
# Biblioteca de geração de números aleatórios, usada para
# criar variações dinâmicas no jogo (ex.: escolhas, sorteios).



# DESCRIÇÃO DO JOGO (DOCSTRING)


"""
O REINO DAS PALAVRAS ENCANTADAS
É um jogo educativo em estilo mágico que ensina gramática. Ele foi pensado para crianças que estão nos anos iniciais da alfabetização e leitura.
A proposta deste jogo é fornecer o aprendizado extra para crianças, através de perguntas interativas e vídeos narrativos, na qual elas podem reforçar o conhecimento sobre a função da vírgula, concordância verbal e nominal, advérbio, plural. Esse jogo foi criado em código python, com a extensão de bibliotecas: Pygame e PyVidPlayer2. Além disso, esse jogo foi pensado e desenvolvido para demonstrar à turma de Programação II 2025.2 que é possível criar ferramentas educativas para todos as idades utilizando os recursos aprendidos em sala de aula com a incrementação de suas habilidades e/ou hobbies. No caso das criadoras, foi a implementação dos vídeos. 

"""



# DEFINIÇÃO DAS CORES PADRÃO

# Paleta de cores inspirada em tons que remetem à fantasia e realeza.
# Cada cor é definida como uma tupla RGB (Red, Green, Blue).

BRANCO = (255, 255, 255)        # Branco puro: usado para textos e destaques.
DOURADO = (255, 215, 0)         # Dourado: remete a elementos reais e mágicos.
ROXO_ESCURO = (60, 0, 80)       # Roxo profundo: cor base do tema fantástico.
LILAS = (180, 120, 255)         # Lilás: cor suave para menus e elementos.
LILAS_CLARO = (200, 160, 255)   # Lilás claro: variação usada para contraste.
VERDE = (0, 200, 0)             # Verde: geralmente usado para mensagens positivas.
VERMELHO = (200, 0, 0)          # Vermelho: utilizado para erros, alertas ou feedback negativo.

# CLASSE: LetraFlutuante
# Representa uma letra decorativa que se move suavemente pela
# tela, criando um efeito de partículas mágicas no plano de fundo.
# É usada apenas para estética e ambientação do jogo.

class LetraFlutuante:
    """
    Classe responsável por criar e controlar letras decorativas
    que flutuam pelo fundo da interface do jogo, contribuindo para
    a estética mágica do ambiente.
    Atributos:
        x (int): posição horizontal da letra na tela.
        y (int): posição vertical da letra.
        velocidade (float): velocidade de queda da letra.
        char (str): caractere (A–Z) exibido na tela.
        fonte (pygame.font.Font): objeto de fonte usado para desenhar o texto. 
        """
    def __init__(self, largura, altura, fonte):
        """
        Método construtor da classe LetraFlutuante.
        Inicializa uma letra com:
        - posição x aleatória dentro da largura da tela,
        - posição y aleatória acima da área visível,
        - velocidade de queda baixa (efeito de flutuação),
        - letra aleatória de A a Z,
        - objeto de fonte recebido como parâmetro.
        Args:
            largura (int): largura da janela do jogo.
            altura (int): altura da janela do jogo.
            fonte (pygame.font.Font): fonte usada para desenhar a letra.
        """
        self.x = random.randint(0, largura)
        self.y = random.randint(-altura, 0)
        self.velocidade = random.uniform(0.3, 1.2)
        self.char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.fonte = fonte
   def atualizar(self, altura):
        """
        Atualiza a posição vertical da letra, fazendo-a cair
        suavemente pela tela de acordo com sua velocidade.
        Se a letra ultrapassar a parte inferior da tela,
        ela é reposicionada acima do topo para reaparecer
        em um ponto aleatório, mantendo o ciclo infinito
        do efeito de flutuação.
        Args:
            altura (int): altura da janela do jogo.
        """
        self.y += self.velocidade
        # Quando a letra sai da área visível, ela é reiniciada acima da tela
        if self.y > altura:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, 1000)
    def desenhar(self, tela, cor):
        """Esta é a terceira e ultima função dentro da classe LetraFlutuante. Ela mostra a letra na tela na cor indicada."""
        texto = self.fonte.render(self.char, True, cor)
        tela.blit(texto, (self.x, self.y))


# CLASSES DE PERGUNTAS

class PerguntaBase:
    """
   Esta classe base é responsável por gerenciar todas as perguntas do quiz. Ela quem possui os atributos para as opções de respostas, feedback e demais ferramentas necessárias para a funcionalização das perguntas específicas.
      """
    def __init__(self, texto, opcoes, resposta_correta, feedback):
        ''' É a primeira função dentro da classe PerguntaBase. Nesta função contém os conteúdos (atributos) e sequencia de ações dentro da tela ao ser emitido a pergunta.’’’
        self.texto = texto
        self.opcoes = opcoes
        self.resposta_correta = resposta_correta
        self.feedback = feedback
        self.botoes_rects = []'''
    def desenhar(self, jogo):
        """
        Exibe a pergunta e as opções nos botões mágicos na tela.
        Os botões são centralizados e realçados ao passar o mouse.
        """
        tela = jogo.tela
        fonte_texto = jogo.fonte_pergunta  # Usa fonte nobre da pergunta
        pergunta_surface = fonte_texto.render(self.texto, True, BRANCO)
        tela.blit(pergunta_surface, (jogo.largura//2 - pergunta_surface.get_width()//2, 100))
        largura_botao = 600
        altura_botao = 60
        espacamento = 20
        inicio_y = jogo.altura // 2
        self.botoes_rects = []
        for i, opcao in enumerate(self.opcoes):
            rect = pygame.Rect(
                (jogo.largura - largura_botao)//2,
                inicio_y + i*(altura_botao + espacamento),
                largura_botao,
                altura_botao
            )
            jogo.desenhar_botao(opcao, rect, LILAS, LILAS_CLARO)
            self.botoes_rects.append(rect)
    def verificar_clique(self, pos):
        """Verifica se o jogador clicou em uma das opções."""
        for i, rect in enumerate(self.botoes_rects):
            if rect.collidepoint(pos):
                return True, i
        return False, None
    def resposta_valida(self, indice):
        """
        Verifica se a resposta escolhida é correta.
        Retorna se acertou, o feedback correspondente e a resposta certa.
        """
        acertou = (indice == self.resposta_correta)
        mens = self.feedback[self.resposta_correta if acertou else indice]
        texto_correto = self.opcoes[self.resposta_correta]
        return acertou, mens, texto_correto

# PERGUNTAS ESPECÍFICAS

class Pergunta1(PerguntaBase):
    """Pergunta sobre o uso da vírgula."""
    def __init__(self):
        super().__init__(
            "Qual é a função da vírgula?",
            ["Separar elementos", "Não serve pra nada", "Indicar verbo"],
            0,
            [
                "Correto! A vírgula separa elementos como se fosse um feitiço de ordem.",
                "Poxa! A vírgula serve, sim! Ela organiza a magia do texto.",
                "Ops! Verbo não tem nada a ver com isso."
            ]
        )

class Pergunta2(PerguntaBase):
    """Pergunta sobre concordância verbal."""
    def __init__(self):
        super().__init__(
            "Assinale a frase com concordância correta.",
            ["Os menino brinca no parque", "Os meninos brincam no parque", "Os menino brincam no parque"],
            1,
            [
                "Não deu! O feitiço da concordância falhou!",
                "Perfeito! A gramática te aplaude de pé!",
                "Quase, mas a concordância fugiu!"
            ]
        )

class Pergunta3(PerguntaBase):
    """Pergunta sobre advérbio."""
    def __init__(self):
        super().__init__(
            "Qual palavra é advérbio?",
            ["Rapidamente", "Bonito", "Casa"],
            0,
            [
                "Acertou! Rapidamente é um advérbio mágico da velocidade.",
                "Ih, não! 'Bonito' é adjetivo, não advérbio.",
                "Nem pensar! 'Casa' é um substantivo comum."
            ]
        )

class Pergunta4(PerguntaBase):
    """Pergunta sobre plural de 'pão'."""
    def __init__(self):
        super().__init__(
            "Qual é a forma correta do plural de 'pão'?",
            ["Pães", "Pãos", "Pões"],
            0,
            [
                "Certo! 'Pães' é o plural encantado de 'pão'.",
                "Não existe 'pãos' nem no mundo da fantasia!",
                "'Pões'? Só se for feitiço de conjugar errado!"
            ]
        )


# CLASSE PRINCIPAL: Jogo

class Jogo:
    """
    Classe principal responsável por controlar toda a execução do jogo, como  inicialização, telas, vídeos, perguntas e pontuação.
    Esta classe gerencia:
    - Inicialização do Pygame.
    - Carregamento de fontes, imagens e configurações gráficas.
    - Execução da tela inicial, transições com vídeos e interface das perguntas.
    - Exibição de feedbacks e da pontuação final.
    - Laço principal que coordena vídeos + perguntas + pontuação.
    """
    def __init__(self):
        """
        Construtor da classe Jogo.
        Faz as seguintes operações:
        - Inicializa módulos do pygame (vídeo, áudio e fontes).
        - Define o tamanho da janela principal.
        - Carrega a imagem de fundo da cena (ou usa fallback caso não exista).
        - Carrega todas as fontes usadas no jogo.
        - Inicializa lista de letras mágicas flutuantes para compor o fundo animado.
        - Define lista de perguntas exibidas durante o quiz.
        - Carrega os caminhos dos vídeos de transição entre as perguntas.
        """
        pygame.init()
        pygame.mixer.init()
        # Tamanho da tela
        self.largura, self.altura = 1900, 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("O Reino das Palavras Encantadas")
        self.clock = pygame.time.Clock()
        # ---------- FUNDO DO JOGO ----------
        caminho_fundo = os.path.join(os.path.dirname(__file__), "menu.png")
        # Verifica se imagem existe. Caso não exista, usa fallback com cor sólida.
        if os.path.exists(caminho_fundo):
            self.imagem_fundo = pygame.image.load(caminho_fundo)
            self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.largura, self.altura))
        else:
            self.imagem_fundo = pygame.Surface((self.largura, self.altura))
            self.imagem_fundo.fill(ROXO_ESCURO)
        # ---------- FONTES ----------
        pygame.font.init()
        self.fonte_titulo = pygame.font.Font("CinzelDecorative-Regular.ttf", 74)
        self.fonte_letras = pygame.font.Font("Parisienne-Regular.ttf", 40)
        self.fonte_texto = pygame.font.Font("Parisienne-Regular.ttf", 32)
        self.fonte_botao = pygame.font.Font("Alice.ttf", 30)
        self.fonte_pergunta = pygame.font.Font("CinzelDecorative-black.ttf", 44)
        # Criação de letras animadas exibidas ao fundo
        self.letras = [LetraFlutuante(self.largura, self.altura, self.fonte_letras) for _ in range(30)]
        # Controle de perguntas e progresso
        self.total_acertos = 0
        self.total_partidas = 0
        # Instâncias das perguntas do quiz
        self.perguntas = [Pergunta1(), Pergunta2(), Pergunta3(), Pergunta4()]
        self.indice = 0
        # ---------- VÍDEOS DE TRANSIÇÃO ----------
        # Cada vídeo está ligado à pergunta seguinte.
        self.videos = [
            {"caminho": r"C:\Users\Priscila\Desktop\Vídeos prontos\introducaoP1.mp4", "pergunta": Pergunta1()},
            {"caminho": r"C:\Users\Priscila\Desktop\Vídeos prontos\entreP1eP2.mp4", "pergunta": Pergunta2()},
            {"caminho": r"C:\Users\Priscila\Desktop\Vídeos prontos\entreP2eP3.mp4", "pergunta": Pergunta3()},
            {"caminho": r"C:\Users\Priscila\Desktop\Vídeos prontos\entreP3eP4.mp4", "pergunta": Pergunta4()},
            {"caminho": r"C:\Users\Priscila\Desktop\Vídeos prontos\Final.mp4", "pergunta": None},
        ]
    # DESENHO DOS BOTÕES
    def desenhar_botao(self, texto, rect, cor_base, cor_hover):
        """
        Desenha botões interativos com efeito de hover.
        Parâmetros:
            texto (str): Texto exibido no botão.
            rect (pygame.Rect): Área do botão.
            cor_base (tuple): Cor normal do botão.
            cor_hover (tuple): Cor ao passar o mouse.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Troca cor se o mouse estiver sobre o botão
        cor = cor_hover if rect.collidepoint(mouse_x, mouse_y) else cor_base
        pygame.draw.rect(self.tela, cor, rect, border_radius=10)
        txt_surface = self.fonte_botao.render(texto, True, BRANCO)
        self.tela.blit(txt_surface, (
            rect.x + (rect.width - txt_surface.get_width()) // 2,
            rect.y + (rect.height - txt_surface.get_height()) // 2
        ))
    # TELA INICIAL
    def tela_inicial(self):
        """
        Exibe a tela inicial do jogo.
        A tela contém:
        - A imagem de fundo.
        - Uma frase inspiradora.
        - Uma instrução para clicar e iniciar o jogo.
        A tela só fecha quando:
        - O usuário clicar com o mouse.
        - Ou encerrar a janela (QUIT).
        """
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    rodando = False  # passa para a próxima etapa
            self.tela.blit(self.imagem_fundo, (0, 0))
            frase = "A magia começa quando a palavra é dita com sabedoria."
            texto = self.fonte_texto.render(frase, True, DOURADO)
            self.tela.blit(texto, texto.get_rect(center=(self.largura/2, self.altura/2)))
            aviso = self.fonte_botao.render("Clique para continuar", True, BRANCO)
            self.tela.blit(aviso, aviso.get_rect(center=(self.largura/2, self.altura/2 + 60)))
            pygame.display.update()
            self.clock.tick(60)
    # VÍDEOS ENTRE AS PERGUNTAS
    def reproduzir_video(self, caminho):
        """
        Reproduz vídeos de introdução ou transição entre perguntas.
        - Usa Video() da biblioteca pyvidplayer2.
        - Exibe frame por frame em um loop até o vídeo terminar.
        - Permite fechar a janela durante o vídeo.
        Parâmetro:
            caminho (str): Caminho absoluto do arquivo de vídeo.
        """
        video = Video(caminho)
        while video.active:
            video.draw(self.tela, (0, 0))
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    video.close()
                    pygame.quit()
                    sys.exit()
            self.clock.tick(30)
        video.close()
    # FEEDBACK DAS RESPOSTAS
    def tela_feedback(self, acertou, feedback, resposta_certa):
        """
        Exibe tela de feedback visual e textual após cada resposta:
        verde para acerto, vermelho para erro após responder cada pergunta.
        Parâmetros:
            acertou (bool): True se a resposta foi correta.
            feedback (str): Texto exibido ao usuário.
            resposta_certa (str): Texto da resposta correta (somente se errou).
        A tela:
        - Fica verde em caso de acerto.
        - Fica vermelha em caso de erro.
        - Fecha ao clicar com o mouse.
        """
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    rodando = False
            cor_fundo = VERDE if acertou else VERMELHO
            self.tela.fill(cor_fundo)
            texto = self.fonte_texto.render(feedback, True, BRANCO)
            self.tela.blit(texto, texto.get_rect(center=(self.largura/2, self.altura/2 - 40)))
            if not acertou:
                certo = self.fonte_texto.render(f"Resposta certa: {resposta_certa}", True, DOURADO)
                self.tela.blit(certo, certo.get_rect(center=(self.largura/2, self.altura/2 + 20)))
            pygame.display.update()
            self.clock.tick(60)
    # EXECUÇÃO DO QUIZ
    def rodar_quiz(self):
        """
        Controla toda a lógica do quiz:
        Para cada item da lista self.videos:
            1. Reproduz o vídeo anterior à pergunta.
            2. Se existir pergunta associada, exibe:
                - Fundo animado com letras flutuantes.
                - Enunciado e alternativas.
                - Interação via clique.
            3. Mostra feedback (acerto/erro).
        Ao final, chama a tela de pontuação final.
        """
        acertos = 0
        for i, item in enumerate(self.videos):
            caminho = item["caminho"]
            pergunta = item["pergunta"]
            # Executa vídeo de transição
            self.reproduzir_video(caminho)
            # Se houver pergunta associada ao vídeo
            if pergunta:
                rodando = True
                while rodando:
                    self.tela.blit(self.imagem_fundo, (0, 0))
                    # Letras animadas
                    for letra in self.letras:
                        letra.atualizar(self.altura)
                        letra.desenhar(self.tela, DOURADO)
                    # Desenha pergunta e alternativas
                    pergunta.desenhar(self)
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if evento.type == pygame.MOUSEBUTTONDOWN:
                            clicou, escolhido = pergunta.verificar_clique(evento.pos)
                            if clicou:
                                acertou, mens, texto_certo = pergunta.resposta_valida(escolhido)
                                if acertou:
                                    acertos += 1
                                self.tela_feedback(acertou, mens, texto_certo)
                                rodando = False
                    pygame.display.update()
                    self.clock.tick(60)
        # Depois da última pergunta e do último vídeo
        self.mostrar_pontuacao_final(acertos, len(self.perguntas))
    # TELA FINAL
    def mostrar_pontuacao_final(self, acertos, total):
        """
        Exibe tela final com o total de acertos do jogador.
        Parâmetros:
            acertos (int): Número de respostas corretas.
            total (int): Total de perguntas do quiz.
        A tela fecha ao clicar com o mouse.
        """
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    rodando = False
            self.tela.blit(self.imagem_fundo, (0, 0))
            msg = f"Você acertou {acertos} de {total} perguntas!"
            texto = self.fonte_titulo.render(msg, True, DOURADO)
            self.tela.blit(texto, texto.get_rect(center=(self.largura/2, self.altura/2)))
            pygame.display.update()
            self.clock.tick(60)
    # INÍCIO DO JOGO
    def rodar(self):
        """
        Método principal para executar o fluxo completo do jogo.
        Executa:
        1. Tela inicial.
        2. Sequência de vídeos + perguntas.
        3. Tela final de pontuação.
        """
        self.tela_inicial()
        self.rodar_quiz()

# EXECUÇÃO PRINCIPAL

if __name__ == "__main__":
    """
    Ponto de entrada do jogo.
    É executado apenas quando o arquivo é rodado diretamente.
    """
    Jogo().rodar()
