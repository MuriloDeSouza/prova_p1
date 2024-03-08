# robo.py

# Traz a ferramenta serial para apresentar quais portas estão disponíveis
from serial.tools import list_ports
import inquirer
import pydobot
from yaspin import yaspin
import typer
import time

# Classe para mover o robo com as juntas
class InteliArm(pydobot.Dobot):
    def __init__(self, port=None, verbose=False):
        super().__init__(port=port, verbose=verbose)
    
    def movej_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)

    def movel_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVL_XYZ, wait=wait)

#Instância de aplicação
app = typer.Typer()

# Traz o spinner para apresentar uma animação enquanto o robô está se movendo
spinner = yaspin(text="Processando...", color="white")

# Listas as portas seriais disponíveis
available_ports = list_ports.comports()

# Pede para o usuário escolher uma das portas disponíveis
porta_escolhida = inquirer.prompt([
    inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])
])["porta"]

# Cria uma instância do robô
robo = InteliArm(port=porta_escolhida, verbose=False)

@app.command()
def movimentos():
    # realiza lista de perguntas para o usuário
    perguntas = [
        inquirer.List("movimento", message="Qual movimento você deseja que o robô faça?", choices=["Home", "Ligar_Ferramenta","Desligar_Ferramenta","Posição_Atual","Vá_até(x,y,z,r):","Qual eixo vc quer mexer?","Sair"])
    ]
    continuar = True
    while continuar:
        # realiza a leitura das respostas
        respostas = inquirer.prompt(perguntas)
        # chama a funcao que processa a operação e exibe uma spinner para o usuário
        spinner = yaspin(text="Processando...", color="yellow")
        # realiza a operação
        saida = processar(respostas)
        # exibe o resultado
        print(saida)
    continuar = typer.confirm("Deseja continuar?")

# Função que processa a operação
def processar(dados):
    operacao = dados["movimento"]

    if operacao == "Home":
        robo.speed(100, 100)
        spinner.start()
        robo.movej_to(238, -11, 150, 0, wait=True)
        posicao_atual = robo.pose()
        print(f"Posição atual: {posicao_atual}")
        spinner.stop()

    elif operacao == "Ligar_Ferramenta":
        spinner.start()
        robo.suck(True)
        spinner.stop()

    
    elif operacao == "Desligar_Ferramenta":
        spinner.start()
        robo.suck(False)
        spinner.stop()

    elif operacao == "Posição_Atual":
        posicao_atual = robo.pose()
        print(f"Posição atual: {posicao_atual}")
        spinner.stop()


    elif operacao == "Vá_até(x,y,z,r):":
        x = typer.prompt("Digite o valor de X", type=float)
        y = typer.prompt("Digite o valor de Y", type=float)
        z = typer.prompt("Digite o valor de Z", type=float)
        r = typer.prompt("Digite o valor de R", type=float)

        spinner.start()
        robo.movej_to(x, y, z, r, wait=True)
        posicao_atual = robo.pose()
        spinner.stop()

    elif operacao == "Qual eixo vc quer mexer?":
        eixos = inquirer.prompt([
            inquirer.List("eixo", choices=["X", "Y", "Z", "R"])
        ])   
        operacao_1 = eixos["eixo"]   
        if operacao_1 == "X":
            posicao_atual = robo.pose()
            x = typer.prompt("Digite o valor de X", type=float)
            robo.speed(100, 100)
            spinner.start()
            robo.movej_to(posicao_atual[0]+x, posicao_atual[1], posicao_atual[2], posicao_atual[3], wait=True)
            posicao_atual = robo.pose()
            spinner.stop()

        elif operacao_1 == "Y":
            posicao_atual = robo.pose()
            y = typer.prompt("Digite o valor de Y", type=float)
            robo.speed(100, 100)
            spinner.start()
            robo.movej_to(posicao_atual[0], posicao_atual[1]+y, posicao_atual[2], posicao_atual[3], wait=True)
            posicao_atual = robo.pose()
            spinner.stop()

        elif operacao_1 == "Z":
            posicao_atual = robo.pose()
            z = typer.prompt("Digite o valor de Z", type=float)
            robo.speed(100, 100)
            spinner.start()
            robo.movej_to(posicao_atual[0], posicao_atual[1], posicao_atual[2]+z, posicao_atual[3], wait=True)
            posicao_atual = robo.pose()
            spinner.stop()

        elif operacao_1 == "R":
            posicao_atual = robo.pose()
            r = typer.prompt("Digite o valor de X", type=float)
            robo.speed(100, 100)
            spinner.start()
            robo.movej_to(posicao_atual[0], posicao_atual[1], posicao_atual[2], posicao_atual[3]+r, wait=True)
            posicao_atual = robo.pose()
            spinner.stop()

    elif operacao == "Sair":
        continuar = False
        quit()

        
#Ele executa a aplicação    
if __name__ == "__main__":
    app()

robo.close()
quit()