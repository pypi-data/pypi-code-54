#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


def LogisticRegression_Classifier(x_train, y_train, x_test, y_test, class_weight=None, tol=1e-4,
                                  max_iter=100, intercept_scaling=1,
                                  warm_start=False, n_jobs=None, verbose=0, random_state=None):

    # list_penalty = ['l2', 'l1', 'elasticnet', 'none']
    list_penalty = ['l2', 'l1']
    # Usado para especificar a norma usada na penalização.
    # Os solucionadores 'newton-cg', 'sag' e 'lbfgs' suportam apenas penalidades de l2.
    # 'elasticnet' é suportado apenas pelo solucionador de 'saga'.
    # Se 'none' (não suportado pelo solucionador liblinear), nenhuma regularização será aplicada.

    list_dual = [False, True]
    # Formulação dupla ou primária. A formulação dupla é implementada apenas para penalidade
    # de l2 com o solucionador liblinear. Prefira dual = False quando n_samples> n_features.

    list_fit_intercept = [True, False]
    # Especifica se uma constante (também conhecida como
    # viés ou interceptação) deve ser adicionada à função de decisão.

    # list_solver = ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga']
    list_solver = ['lbfgs', 'newton-cg', 'liblinear']
    # Algoritmo a ser usado no problema de otimização.
    # Para conjuntos pequenos, 'liblinear' é uma boa opção, enquanto 'sag' e 'saga' são mais rápidos para os grandes.
    # Para problemas multiclasses, apenas 'newton-cg', 'sag', 'saga' e 'lbfgs' lidam
    # com a perda multinomial; 'liblinear' é limitado a esquemas de um contra o resto.
    # newton-cg', 'lbfgs', 'sag' e 'saga' lidam com L2 ou sem penalidade
    # 'liblinear' e 'saga' também são penalizados com L1
    # 'saga' também suporta pena 'elasticnet'
    # 'liblinear' não suporta configuração penalty='none'
    # Observe que a convergência rápida 'sag' e 'saga' é garantida apenas em recursos com aproximadamente
    # a mesma escala. Você pode pré-processar os dados com um scaler em sklearn.preprocessing.

    list_multi_class = ['auto', 'ovr', 'multinomial']
    # Se a opção escolhida for 'ovr', um problema binário é adequado para cada etiqueta. Para 'multinomial', a perda
    # minimizada é a perda multinomial que se ajusta a toda a distribuição de probabilidade, mesmo quando os dados
    # são binários. 'multinomial' fica indisponível quando solver = 'liblinear'. 'auto' seleciona 'ovr' se os dados
    # são binários ou se solver = 'liblinear' e, de outra forma, seleciona 'multinomial'.

    result = 0
    list_res = []
    for penalty in list_penalty:
        for dual in list_dual:
            for fit_intercept in list_fit_intercept:
                for solver in list_solver:
                    for multi_class in list_multi_class:
                        for C in [0.1, 1.0, 0.1]:

                            if solver == 'liblinear' and multi_class == 'multinomial':
                                continue

                            if solver in ['lbfgs', 'newton-cg', 'sag', 'saga'] and dual:
                                continue

                            if solver in ['lbfgs', 'newton-cg', 'sag'] and penalty == 'l1':
                                continue

                            if penalty == 'l1' and dual:
                                continue

                            model = LogisticRegression(penalty=penalty, dual=dual, fit_intercept=fit_intercept,
                                                       solver=solver, multi_class=multi_class, C=C,
                                                       class_weight=class_weight, tol=tol, max_iter=max_iter,
                                                       intercept_scaling=intercept_scaling,
                                                       warm_start=warm_start, n_jobs=n_jobs, verbose=verbose,
                                                       random_state=random_state)
                            model.fit(x_train, y_train.ravel())

                            model.predict(x_test)
                            acc = model.score(x_test, y_test) * 100
                            # acc = accuracy_score(y_test, y_pred) * 100

                            if acc > result:
                                list_res = [[penalty, dual, fit_intercept, class_weight,
                                             solver, multi_class, C, acc]]
                                result = acc

    df = pd.DataFrame(list_res, columns=['penalty', 'dual', 'intercept', 'class_weight',
                                         'solver', 'multi_class', 'C', 'acc'])
    return df


def KNeighbors_Classifier(x_train, y_train, x_test, y_test, n_jobs=None):

    list_metrics = ['minkowski', 'manhattan', 'euclidean', 'chebyshev']
    # Parâmetro de potência para a métrica de Minkowski.
    # Quando p=1, isso equivale a usar manhattan_distance (l1_distance)
    # Quando p=2, isso equivale a usar euclidean_distance (l2_distance).
    # Para p arbitrário, minkowski_distance (l_p) é usado.

    list_algorithms = ['auto', 'ball_tree', 'kd_tree', 'brute']

    list_leaf_size = [30, 40]
    # Tamanho da folha passado para o BallTree ou KDTree.
    # Isso pode afetar a velocidade da construção e consulta, bem como a memória
    # necessária para armazenar a árvore. O valor ideal depende da natureza do problema.

    list_weights = ['uniform', 'distance']
    # 'uniform': pesos uniformes. Todos os pontos em cada vizinhança têm o mesmo peso.
    # 'distance': pontos de peso pelo inverso de sua distância. nesse caso, vizinhos mais
    # próximos de um ponto de consulta terão uma influência maior do que os vizinhos mais distantes.

    result = 0
    list_res = []
    for metric in list_metrics:
        for algorithm in list_algorithms:
            for weight in list_weights:
                for leaf_size in list_leaf_size:
                    for p in [1, 2, 3]:
                        for k in range(1, 6, 2):
                            model = KNeighborsClassifier(n_neighbors=k, weights=weight, algorithm=algorithm,
                                                         metric=metric, p=p, leaf_size=leaf_size, n_jobs=n_jobs)
                            model.fit(x_train, y_train.ravel())

                            model.predict(x_test)
                            acc = model.score(x_test, y_test) * 100
                            # acc = accuracy_score(y_test, y_pred) * 100

                            if acc > result:
                                if metric == 'minkowski':
                                    name_metric = 'l1_distance' if p == 1 else 'l2_distance' if p == 2 else 'minkowski'
                                else:
                                    name_metric = metric

                                list_res = [[name_metric, p, acc, k, weight, algorithm, leaf_size]]
                                # list_res.append([name_metric, p, acc, k, weight, algorithm, leaf_size])
                                result = acc

    df = pd.DataFrame(list_res, columns=['metric', 'p', 'accuracy', 'k', 'weights', 'algorithm', 'leaf_size'])
    return df
