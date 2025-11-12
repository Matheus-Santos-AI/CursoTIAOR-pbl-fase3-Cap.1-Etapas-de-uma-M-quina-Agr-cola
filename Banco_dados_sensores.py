#IMPORTANDO BIBLIOTECAS
import os
import oracledb
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Try para tentativa de Conexão com o Banco de Dados
try:
    # Efetua a conexão com o Usuário no servidor
    conn = oracledb.connect(user='rm566901', password="160393", dsn='oracle.fiap.com.br:1521/ORCL')
    # Cria as instruções para cada módulo

    inst_consulta = conn.cursor()

except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True
margem = ' ' * 4 # Define uma margem para a exibição da aplicação

# Enquanto o flag conexao estiver apontado com True
while conexao:
    # Limpa a tela via SO
    os.system('cls')

    # Apresenta o menu
    print("------- Logistica Facil -------")
    print("""
    1 - Consultar dados
    2 - Analisar DADOS DO PERIODO 
    3 - SAIR
    """)

    # Captura a escolha do usuário
    escolha = input(margem + "Escolha -> ")

    # Verifica se o número digitado é um valor numérico
    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 4
        print("Digite um número.\nReinicie a Aplicação!")

    os.system('cls')  # Limpa a tela via SO


    # VERIFICA QUAL A ESCOLHA DO USUÁRIO
    match escolha:

        case 1:
            try:
                data_consulta_inicio = input("Digite o periodo a ser consultado. (exemplo:10/11/2025)\n Inicio:\n ")
                data_consulta_fim = input("Fim:\n ")



                # CONSULTA O BANCO DE DADOS E CRIA UM DATAFRAME

                query= f"SELECT * FROM DADOS_GERADOS_SENSORES WHERE TIMESTAMP >= TO_DATE('{data_consulta_inicio}', 'DD/MM/YYYY') AND TIMESTAMP < TO_DATE('{data_consulta_fim} 23:59:59', 'DD/MM/YYYY HH24:MI:SS')"
                df2 = pd.DataFrame (inst_consulta.execute(query), columns=['TIMESTAMP','NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH', 'UMIDADE_SOLO'])


            except:
                # Caso ocorra algum erro de conexão ou no BD
                print("Erro!!!\nTENTE NOVAMENTE\nCaso o ERRO persista procure o suporte")
            else:
                print("----- LISTAR DADOS DO PERIODO SELECIONADO -----\n")
                print(df2)
        case 2:
            try:
                data_consulta_inicio = input("Digite o periodo a ser consultado. (exemplo:10/11/2025)\n Inicio:\n ")
                data_consulta_fim = input("Fim:\n ")
                inicio_rega = input("Digite o harario em que é feito a rega (Exemplo: 14:30) :\n Inicio:...\n")
                fim_rega = input("Fim:...\n ")
                query= f"SELECT * FROM DADOS_GERADOS_SENSORES WHERE TIMESTAMP >= TO_DATE('{data_consulta_inicio}', 'DD/MM/YYYY') AND TIMESTAMP < TO_DATE('{data_consulta_fim} 23:59:59', 'DD/MM/YYYY HH24:MI:SS')"
                df2 = pd.DataFrame (inst_consulta.execute(query), columns=['TIMESTAMP','NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH', 'UMIDADE_SOLO'])


                analise_um = pd.DataFrame(df2.mean(numeric_only=True), columns = ['Medias/Periodo'])
                print(f"Médias de cada Indice pelo periodo selecionado {analise_um}")

                #analise grafica


                sns.histplot(data=df2, x='VALOR_PH')
                plt.title("Histograma do pH")
                plt.xticks(rotation=45)
                plt.show()


                # Plotando gráfico de linha

                plt.figure(figsize=(10, 5))
                plt.plot(df2["TIMESTAMP"], df2["VALOR_PH"], marker="o", linestyle="-", color="blue")
                plt.title("Leituras de Sensores ao Longo do Tempo(PH)")
                plt.xlabel("Timestamp")
                plt.ylabel("Valor do PH")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()

                #periodo de rega
                for day in df2["TIMESTAMP"].dt.date.unique():
                    start_rega = pd.Timestamp.combine(day, pd.Timestamp(f"{inicio_rega}:00").time())
                    end_rega = pd.Timestamp.combine(day, pd.Timestamp(f"{fim_rega}:00").time())

                plt.axvspan(start_rega,end_rega, color='orange', alpha=0.3)


                # Exibir o gráfico
                plt.show()

                plt.figure(figsize=(10, 5))
                plt.plot(df2["TIMESTAMP"], df2["UMIDADE_SOLO"], marker="o", linestyle="-", color="blue")
                plt.title("Leituras de Sensores ao Longo do Tempo(UMIDADE DO SOLO)")
                plt.xlabel("Timestamp")
                plt.ylabel("UMIDADE DO SOLO")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                # periodo de rega
                for day in df2["TIMESTAMP"].dt.date.unique():
                    start_rega = pd.Timestamp.combine(day, pd.Timestamp(f"{inicio_rega}:00").time())
                    end_rega = pd.Timestamp.combine(day, pd.Timestamp(f"{fim_rega}:00").time())
                    plt.axvspan(start_rega, end_rega, color='orange', alpha=0.3,
                                label="FAIXA LARANJA REPRESENTA PERIODO DE IRRIGAÇÃO")
                    plt.legend()



                # Exibir o gráfico
                plt.show()
            except:
        # Caso ocorra algum erro de conexão ou no BD
                print("Erro!!!\nTENTE NOVAMENTE\nCaso o ERRO persista procure o suporte")
            else:
                print("----- DADOS ANALISADOS -----\n")

        case 3:
            # Modificando o flag da conexão
            conexao = False

        case _:
            input(margem + "Digite um número entre 1 e 3.")



