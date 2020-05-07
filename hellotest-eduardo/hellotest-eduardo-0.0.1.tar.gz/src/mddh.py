from src.fcf import fcf
from itertools import product, repeat
from cvxopt.modeling import op, variable, matrix
import cvxopt.solvers as solvers
# import matplotlib
# matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from multiprocessing import Pool
from src.pmo import pmo
from src.dadosgerais import dadosgerais
from functools import partial
from timeit import default_timer as timer


class mddh(object):
    # Classe contendo informacoes sobre os arquivos de entrada e saida
    caso = None
    dger = None
    npmc = 1

    # Define listas
    cadr_uh = []  # Lista com usinas hidraulicas do cadastro (HIDR.DAT)
    cadr_ut = []  # Lista com usinas termicas do cadastro (TERM.DAT)
    conf_ut = []  # Lista com usinas termicas da configuracao em estudo (CONFT.DAT)
    conf_uh = []  # Lista com usinas hidraulicas da configuracao em estudo (CONFHD.DAT)
    cfuturo = []  # Lista com funcoes de custo futuro obtidas pela PDE ou PDDE
    ree = []  # Lista com os reservatorios equivalentes de energia
    submercado = []  # Lista com os submercados
    intercambio = []  # Lista com intercambios entre submercados

    # Parametros Gerais
    ano_ini = 2018
    mes_ini = 12
    nanos = 5
    cdef = 4000
    mercado = 270
    ordmaxparp = 6

    def __init__(self, diretorio):

        # Leitura de arquivos
        self.caso = pmo(diretorio)
        self.caso.le_caso()

        self.cadr_uh = self.caso.le_hidr(self.cadr_uh)
        self.conf_uh = self.caso.le_confh(self.conf_uh, self.cadr_uh, self.nanos)
        self.cadr_ut = self.caso.le_term(self.cadr_ut)
        self.conf_ut = self.caso.le_conft(self.conf_ut, self.cadr_ut)
        self.conf_ut = self.caso.le_clast(self.conf_ut)
        self.conf_uh = self.caso.le_modif(self.conf_uh, self.ano_ini, self.nanos)
        self.conf_uh = self.caso.le_exph(self.conf_uh, self.ano_ini, self.nanos)
        self.ree = self.caso.le_ree(self.ree)
        # Cria Sistema
        self.dger = dadosgerais(self.nanos)
        self.submercado, self.intercambio, self.npmc = self.caso.le_sistema(self.submercado, self.intercambio,
                                                                            self.nanos, self.npmc)

        # Calcula produtibilidades acumuladas
        for iusina in self.conf_uh:
            iusina.ProdAcum(self.conf_uh)

        # Calcula Energias Armazenadas
        for ires in self.ree:
            ires.CalcEArmMax(self.conf_uh)
            ires.CalcENA(self.conf_uh)

        for isist in self.submercado:
            if isist.Ficticio == 0:
                isist.CalcEArmMax(self.conf_uh)
                isist.CalcENA(self.conf_uh)

    #############################################################################
    #############################################################################
    # Programacao Dinamica Estocastica Sequencial e Multiprocessing
    #############################################################################
    #############################################################################

    def pde(self, nr_discret, nr_estagios, nr_cenarios):

        t = timer()

        solvers.options['show_progress'] = True
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        # Define estados a serem visitados em cada estagio
        estados = []
        for i in range(nr_discret):
            estados.append(i / (nr_discret - 1))

        if nr_estagios > 12:
            print('Este exemplo didatico soh funciona para no maxima 12 estagios. Desculpe.')
            return

        # Cria Funcao objetivo, restricoes e inicializa rest. atend. dmenada
        objetivo = 0
        restricoes = []
        atendimentodemanda = 0

        # Cria variaveis de decisao Volume Final, Vertimento e Turbinamento
        vf = variable(len(self.conf_uh), 'vf')
        vv = variable(len(self.conf_uh), 'vv')
        vt = variable(len(self.conf_uh), 'vt')
        for i, iusina in enumerate(self.conf_uh):
            objetivo = objetivo + 0.001 * vv[i]
            # Limite inferior das variaveis hidraulicas
            restricoes.append(vf[i] >= iusina.VolMin)
            restricoes.append(vt[i] >= 0)
            restricoes.append(vv[i] >= 0)
            # Limite superior das variaveis hidraulicas
            restricoes.append(vf[i] <= iusina.VolMax)
            restricoes.append(vt[i] <= iusina.Engolimento)
            restricoes.append(vv[i] <= 100000)
            # Restricao de atendimento a demanda
            prod = float(iusina.Ro65[0][0])
            atendimentodemanda = atendimentodemanda + prod * vt[i]

        # Cria variaveis de decisao Geracao Termica
        gt = variable(len(self.conf_ut), 'gt')
        for i, iusina in enumerate(self.conf_ut):
            objetivo = objetivo + float(iusina.Custo[0]) * gt[i]
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + gt[i]
            # Limite inferior de gt
            restricoes.append(gt[i] >= 0)
            # Limite superior de gt
            restricoes.append(gt[i] <= iusina.Potencia)

        # Cria variaveis de decisao associadas ao deficit
        deficit = variable(1, 'deficit')
        objetivo = objetivo + self.cdef * deficit[0]
        restricoes.append(deficit >= 0)
        restricoes.append(deficit <= 100000)
        atendimentodemanda = atendimentodemanda + deficit[0]

        # Cria Variavel de decisao associada ao custo futuro
        alpha = variable(1, 'alpha')
        objetivo = objetivo + alpha[0]
        restricoes.append(alpha >= 0)
        restricoes.append(alpha <= 10000000)

        restricoes.append(atendimentodemanda == self.mercado)

        # Calcula funcoes objetivos por estado
        for imes in range(nr_estagios, 0, -1):  # Loop de estagio
            print('###############', imes)

            # Cria Função de Custo Futuro Vazia Associada ao Estagio (imes)
            self.cfuturo.append(fcf(imes))

            if len(self.cfuturo) > 1:
                rest_cortes = self.cfuturo[len(self.cfuturo) - 2].get_fcf(vf, alpha)
            else:
                rest_cortes = []

            apontador = len(restricoes)

            # Gera discretizacoes
            discret = product(estados, repeat=len(self.conf_uh))
            for idisc, idiscret in enumerate(discret):  # Loop de discretizacao
                # Inicializa volumes (estados) das usinas correspondentes a iteracao corrente
                VI = matrix(0, (len(self.conf_uh), 1), 'd')
                LAMBDA = matrix(0, (len(self.conf_uh), 1), 'd')
                CUSTO = 0
                for i, iusina in enumerate(self.conf_uh):
                    VI[i] = iusina.VolMin + iusina.VolUtil * idiscret[i]
                    for icen in range(1, nr_cenarios + 1):  # Loop de cenario
                        AFL = matrix(0, (len(self.conf_uh), 1), 'd')
                        for i, iusina in enumerate(self.conf_uh):
                            AFL[i] = float(iusina.Vazoes[icen - 1][imes - 1])
                            restricoes.append(vf[i] == VI[i] + 2.592 * AFL[i] - 2.592 * vt[i] - 2.592 * vv[i])

                        todas = self.reuni(restricoes, rest_cortes)
                        problema = op(objetivo, todas)

                        problema.solve('dense', 'glpk')

                        if problema.status == 'optimal':
                            for i, iusina in enumerate(self.conf_uh):
                                LAMBDA[i] = LAMBDA[i] + todas[apontador + i].multiplier.value
                            CUSTO = CUSTO + problema.objective.value()[0]
                            for i, iusina in enumerate(self.conf_uh):
                                CUSTO = CUSTO - vv[i].value() * 0.001
                        else:
                            print('oops')
                            print(problema.status)
                            problema.tofile('andre.mps')
                            return

                        # Apaga restricoes de Balanco Hidrico
                        ultimo = len(restricoes) - 1
                        for i, iusina in enumerate(self.conf_uh):
                            del restricoes[ultimo]
                            ultimo = ultimo - 1

                    self.cfuturo[len(self.cfuturo) - 1].add_corte(LAMBDA, CUSTO, VI, nr_cenarios)

            # self.plota_corte(imes, nr_discret)
        print(timer() - t)

    def reuni(self, restricoes, rest_cortes):
        tudo = []
        for i in range(0, len(restricoes)):
            tudo.append(restricoes[i])
        for i in range(0, len(rest_cortes)):
            tudo.append(rest_cortes[i])
        return tudo

    def pde_par(self, nr_discret, nr_estagios, nr_cenarios):

        t = timer()

        solvers.options['show_progress'] = False
        solvers.options['glpk'] = dict(msg_lev='GLP_MSG_OFF')

        # Define estados a serem visitados em cada estagio
        estados = []
        for i in range(nr_discret):
            estados.append(i / (nr_discret - 1))

        if nr_estagios > 12:
            print('Este exemplo didatico soh funciona para no maxima 12 estagios. Desculpe.')
            return

        # Cria Funcao objetivo, restricoes e inicializa rest. atend. dmenada
        objetivo = 0
        restricoes = []
        atendimentodemanda = 0

        # Cria variaveis de decisao Volume Final, Vertimento e Turbinamento
        vf = variable(len(self.conf_uh), 'vf')
        vv = variable(len(self.conf_uh), 'vv')
        vt = variable(len(self.conf_uh), 'vt')
        for i, iusina in enumerate(self.conf_uh):
            objetivo = objetivo + 0.001 * vv[i]
            # Limite inferior das variaveis hidraulicas
            restricoes.append(vf[i] >= iusina.VolMin)
            restricoes.append(vt[i] >= 0)
            restricoes.append(vv[i] >= 0)
            # Limite superior das variaveis hidraulicas
            restricoes.append(vf[i] <= iusina.VolMax)
            restricoes.append(vt[i] <= iusina.Engolimento)
            restricoes.append(vv[i] <= 100000)
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + iusina.Ro65 * vt[i]

        # Cria variaveis de decisao Geracao Termica
        gt = variable(len(self.conf_ut), 'gt')
        for i, iusina in enumerate(self.conf_ut):
            objetivo = objetivo + float(iusina.Custo[0]) * gt[i]
            # Restricao de atendimento a demanda
            atendimentodemanda = atendimentodemanda + gt[i]
            # Limite inferior de gt
            restricoes.append(gt[i] >= 0)
            # Limite superior de gt
            restricoes.append(gt[i] <= iusina.Potencia)

        # Cria variaveis de decisao associadas ao deficit
        deficit = variable(1, 'deficit')
        objetivo = objetivo + self.cdef * deficit[0]
        restricoes.append(deficit >= 0)
        restricoes.append(deficit <= 100000)
        atendimentodemanda = atendimentodemanda + deficit[0]

        # Cria Variavel de decisao associada ao custo futuro
        alpha = variable(1, 'alpha')
        objetivo = objetivo + alpha[0]
        restricoes.append(alpha >= 0)
        restricoes.append(alpha <= 10000000)

        restricoes.append(atendimentodemanda == self.mercado)

        # Calcula funcoes objetivos por estado
        for imes in range(nr_estagios, 0, -1):  # Loop de estagio
            print('###############', imes)

            # Cria Função de Custo Futuro Vazia Associada ao Estagio (imes)
            self.cfuturo.append(fcf(imes))

            if len(self.cfuturo) > 1:
                rest_cortes = self.cfuturo[len(self.cfuturo) - 2].get_fcf(vf, alpha)
            else:
                rest_cortes = []

            apontador = len(restricoes)

            # Gera discretizacoes
            discret = product(estados, repeat=len(self.conf_uh))
            C = list(discret)  # Loop de discretizacao

            parametros = {'Sist': self,
                          'nr_cenarios': nr_cenarios,
                          'imes': imes,
                          'restricoes': restricoes,
                          'rest_cortes': rest_cortes,
                          'objetivo': objetivo,
                          'apontador': apontador,
                          'vv': vv,
                          'vt': vt,
                          'vf': vf}

            # self.TaskFcn( parametros, C[0] )
            pool = Pool(processes=4)

            funcao = partial(self.TaskFcn, param=parametros)

            # Resolve com multiprocessing
            res = pool.map(funcao, C)
            # res = map(funcao, C)

            for solucao in res:
                LAMBDA = solucao[2]
                CUSTO = solucao[1]
                VI = solucao[3]
                self.cfuturo[len(self.cfuturo) - 1].add_corte(LAMBDA, CUSTO, VI, nr_cenarios)

            # self.plota_corte(imes, nr_discret)

        print(timer() - t)

    def TaskFcn(self, C, param):

        idiscret = C
        nr_cenarios = param['nr_cenarios']
        sist = param['Sist']
        imes = param['imes']
        restricoes = param['restricoes']
        rest_cortes = param['rest_cortes']
        objetivo = param['objetivo']
        apontador = param['apontador']
        vv = param['vv']
        vt = param['vt']
        vf = param['vf']

        # Inicializa volumes (estados) das usinas correspondentes a iteracao corrente
        VI = matrix(0, (len(sist.conf_uh), 1), 'd')
        LAMBDA = matrix(0, (len(sist.conf_uh), 1), 'd')
        CUSTO = 0
        for i, iusina in enumerate(sist.conf_uh):
            VI[i] = iusina.VolMin + iusina.VolUtil * idiscret[i]
            for icen in range(1, nr_cenarios + 1):  # Loop de cenario
                AFL = matrix(0, (len(sist.conf_uh), 1), 'd')
                for i, iusina in enumerate(sist.conf_uh):
                    AFL[i] = float(iusina.Vazoes[icen - 1][imes - 1])
                    restricoes.append(vf[i] == VI[i] + 2.592 * AFL[i] - 2.592 * vt[i] - 2.592 * vv[i])

                todas = sist.reuni(restricoes, rest_cortes)
                problema = op(objetivo, todas)

                problema.solve('dense', 'glpk')

                if problema.status == 'optimal':
                    for i, iusina in enumerate(sist.conf_uh):
                        LAMBDA[i] = LAMBDA[i] + todas[apontador + i].multiplier.value
                    CUSTO = CUSTO + problema.objective.value()[0]
                    for i, iusina in enumerate(sist.conf_uh):
                        CUSTO = CUSTO - vv[i].value() * 0.001
                else:
                    print('oops')
                    print(problema.status)
                    problema.tofile('andre.mps')
                    return

                # Apaga restricoes de Balanco Hidrico
                ultimo = len(restricoes) - 1
                for i, iusina in enumerate(sist.conf_uh):
                    del restricoes[ultimo]
                    ultimo = ultimo - 1
        return idiscret, CUSTO, LAMBDA, VI

    ####################################################################
    ####################################################################
    # Plotagens Diversas
    ####################################################################
    ####################################################################

    def plota_corte(self, imes, nr_discret):
        for i, ifcf in enumerate(self.cfuturo):
            if ifcf.estagio == imes:
                if len(self.conf_uh) == 1:
                    fig, ax = plt.subplots(figsize=(8, 8))
                    volumes = np.linspace(self.conf_uh[0].VolMin, self.conf_uh[0].VolMax, nr_discret)
                    maior = 0
                    for i in range(0, ifcf.nr_cortes):
                        plt.plot(volumes, (ifcf.coef_vf[i] * volumes + ifcf.termo_i[i]).transpose(), 'b-', lw=3)
                        a = ifcf.coef_vf[i]
                        b = ifcf.termo_i[i]
                        custo = np.array(a * volumes + b)
                        custo.shape = (nr_discret,)
                        if max(custo) > maior:
                            maior = max(custo)
                        plt.fill_between(volumes, 0, custo, facecolor='blue', alpha=0.1)

                    plt.xlabel('Volume Inicial (hm^3)', fontsize=16)
                    titulo = 'Funcao de Custo Futuro do Mes ' + str(imes)
                    plt.title(titulo, fontsize=16)
                    plt.ylabel('Custo (R$)', fontsize=16)
                    plt.xlim(self.conf_uh[0].VolMin, self.conf_uh[0].VolMax)
                    # plt.ylim(0,max(ifcf.termo_i))
                    plt.ylim(0, maior)
                    plt.show()
                    return
                else:
                    print('Somente imprime fcf se existir apenas 1 uh')

    # Plota Usinas Não Existentes e Existentes em Expansao
    def Plota_Expansao_Uh(self):

        # Conta quantas usinas estao
        cont = 0
        nomes = []
        for usina in self.conf_uh:
            if usina.Status == 'EE' or usina.Status == 'NE':
                cont += 1
                nomes.append(usina.Nome)

        motorizada = np.zeros(cont)
        vazia = np.zeros(cont)
        enchendo = np.zeros(cont)
        submotorizada = np.zeros(cont)

        ind = np.arange(cont)
        cont = 0
        for usina in self.conf_uh:
            if usina.Status == 'EE' or usina.Status == 'NE':
                # Meses em que a usina esta motorizada
                motorizada[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusMotoriz - 2)

                # Meses que a usina ainda nao iniciou o enchimento do volume morto
                vazia[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusVolMorto)

                # Meses que a usina encontra-se enchendo o volume morto
                enchendo[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusVolMorto - 1)

                # Meses que a usina encontra-se motorizando
                submotorizada[cont] = self.nanos * 12 - np.count_nonzero(usina.StatusMotoriz - 1)

                cont += 1

        width = 0.35  # the width of the bars: can also be len(x) sequence

        ax = plt.axes()
        p1 = plt.barh(ind, vazia, width, color='w')
        p2 = plt.barh(ind, enchendo, width, color='lime', left=vazia)
        p3 = plt.barh(ind, submotorizada, width, color='sienna', left=vazia + enchendo)
        p4 = plt.barh(ind, motorizada, width, color='black', left=vazia + enchendo + submotorizada)

        plt.ylabel('Usinas', fontsize=16)
        plt.title('Usinas Hidreletricas em Expansao', fontsize=16)
        plt.yticks(ind, nomes, fontsize=12)
        plt.xticks(np.arange(0, self.nanos * 12 + 2, 12))
        # plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Nao Entrou', 'Enchendo Vol. Morto', 'Submotorizada', 'Motorizada'),
                   fontsize=12)
        plt.xlabel('Meses do Estudo', fontsize=16)
        ax.xaxis.grid()

        plt.show()

    # Plota Mercado de Todos os Submercados
    def PlotaMercado(self):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.submercado[0].Mercado) - 1
        nr_col = len(self.submercado[0].Mercado[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for mercado in self.submercado:
            if mercado.Ficticio == 0:
                if mercado.Codigo == 1:
                    cor = 'lime'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 2:
                    cor = 'blue'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 3:
                    cor = 'chocolate'
                    linha = '--'
                    LineWidth = 2
                elif mercado.Codigo == 4:
                    cor = 'black'
                    linha = '-'
                    LineWidth = 3
                else:
                    cor = 'orange'
                y = np.arange(1, nr_lin * nr_col + 1)
                y = mercado.Mercado[0:nr_lin][0:nr_col]
                ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                        lw=LineWidth, label=mercado.Nome)
                ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                                (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
                total += y

        titulo = 'Evolucao da Demanda Total do Sistema'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Demanda de Energia (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    # Plota Energia Armazenada Maxima de Todos REEs
    def PlotaEArmMaxRee(self):

        f, (ax) = plt.subplots(1, 1)
        nr_lin = len(self.ree[0].EArmMax)
        nr_col = len(self.ree[0].EArmMax[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for ree in self.ree:
            linha = '--'
            LineWidth = 2
            if ree.Codigo == 0:
                cor = 'lime'
            elif ree.Codigo == 1:
                cor = 'blue'
            elif ree.Codigo == 2:
                cor = 'chocolate'
            elif ree.Codigo == 3:
                cor = 'darkgreen'
            elif ree.Codigo == 4:
                cor = 'fuchsia'
            elif ree.Codigo == 5:
                cor = 'gold'
            elif ree.Codigo == 6:
                cor = 'maroon'
            elif ree.Codigo == 7:
                cor = 'orangered'
            elif ree.Codigo == 8:
                cor = 'orchid'
            elif ree.Codigo == 9:
                cor = 'violet'
            elif ree.Codigo == 10:
                cor = 'yellowgreen'
            elif ree.Codigo == 11:
                cor = 'tan'
            else:
                cor = 'black'

            y = np.arange(1, nr_lin * nr_col + 1)
            y = ree.EArmMax[0:nr_lin][0:nr_col]
            ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                    lw=LineWidth, label=ree.Nome)
            ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                            (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
            total += y

        titulo = 'Evolução da Energia Armazenada Máxima \n Por Reservatorio Equivalente de Energia'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armazenada Maxima (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()

    # Plota Energia Armazenada Maxima de Todos Submercados
    def PlotaEArmMaxSist(self):

        f, (ax) = plt.subplots(1, 1)

        nr_lin = len(self.submercado[0].Mercado) - 1
        nr_col = len(self.submercado[0].Mercado[0])
        total = np.zeros((nr_lin, nr_col), 'd')

        for mercado in self.submercado:
            if mercado.Ficticio == 0:
                linha = '--'
                LineWidth = 2
                if mercado.Codigo == 1:
                    cor = 'lime'
                elif mercado.Codigo == 2:
                    cor = 'blue'
                elif mercado.Codigo == 3:
                    cor = 'chocolate'
                elif mercado.Codigo == 4:
                    cor = 'darkgreen'
                else:
                    cor = 'acqua'

                y = np.arange(1, nr_lin * nr_col + 1)
                y = mercado.EArmMax[0:nr_lin][0:nr_col]
                ax.plot(np.arange(1, nr_lin * nr_col + 1), (total + y).reshape(nr_lin * nr_col, ), linha, color=cor,
                        lw=LineWidth, label=mercado.Nome)
                ax.fill_between(np.arange(1, nr_lin * nr_col + 1), total.reshape(nr_lin * nr_col, ),
                                (total + y).reshape(nr_lin * nr_col, ), facecolor=cor, alpha=0.1)
                total += y

        titulo = 'Evolução da Energia Armazenada Máxima \n Por Submercado'
        f.canvas.set_window_title(titulo)

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel('Meses de Estudo', fontsize=14)
        ax.set_ylabel('Energia Armazenada Maxima (MWmes)', fontsize=14)
        ax.legend(fontsize=12)

        plt.show()
