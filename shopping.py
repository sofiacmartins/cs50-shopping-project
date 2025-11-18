import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

"""
🛒 Shopping - Sistema de Previsão de Compras Online com IA

Este programa utiliza machine learning (algoritmo K-Nearest Neighbors)
para prever se um cliente numa loja online irá completar uma compra,
baseado em 17 características do seu comportamento de navegação.

Features Implementadas:
    1. load_data() - Carregamento e processamento de dados CSV
    2. train_model() - Treino com K-Nearest Neighbors (k=1)
    3. evaluate() - Avaliação com Sensitivity e Specificity
    4. validate_data() - Validação automática de integridade [IA]
    5. analyze_dataset() - Análise estatística do dataset [IA]

Dataset: 12.330 sessões reais de utilizadores de e-commerce
Resultados: Accuracy ~83% | Sensitivity ~41% | Specificity ~91%

Desenvolvido por: Sofia Martins
Data: Novembro 2025
"""

TEST_SIZE = 0.4  # 40% dos dados para teste, 60% para treino


def main():
    """
    Função principal que coordena todo o fluxo do programa.
    """
    # Verificar argumentos da linha de comandos
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # PASSO 1: Carregar dados do CSV
    # Transforma texto em dados numéricos prontos para ML
    evidence, labels = load_data(sys.argv[1])
    
    # PASSO 2: Validar dados (FEATURE EXTRA 1 - desenvolvida com IA)
    # Garante que os dados estão corretos antes do treino
    is_valid, errors = validate_data(evidence, labels)
    if not is_valid:
        print("Erros encontrados:")
        for error in errors[:10]:  # Mostrar apenas primeiros 10
            print(f"  - {error}")
        sys.exit(1)
    
    # PASSO 3: Analisar estatísticas (FEATURE EXTRA 2 - desenvolvida com IA)
    # Mostra distribuição dos dados e explica os resultados
    analyze_dataset(evidence, labels)
    
    # PASSO 4: Dividir dados em treino (60%) e teste (40%)
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # PASSO 5: Treinar o modelo KNN
    model = train_model(X_train, y_train)
    
    # PASSO 6: Fazer previsões nos dados de teste
    predictions = model.predict(X_test)
    
    # PASSO 7: Avaliar a qualidade das previsões
    sensitivity, specificity = evaluate(y_test, predictions)

    # PASSO 8: Mostrar resultados finais
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    ═══════════════════════════════════════════════════════════════
    FUNÇÃO 1 (OBRIGATÓRIA): CARREGAR E PROCESSAR DADOS
    ═══════════════════════════════════════════════════════════════
    
    Transforma um CSV de texto em dados numéricos para ML.
    
    INPUT: Nome do ficheiro CSV
    OUTPUT: Tuplo (evidence, labels)
            - evidence: lista de 12.330 listas com 17 features cada
            - labels: lista de 12.330 valores (0 ou 1)
    
    APRESENTAÇÃO: Explicar o mapeamento de meses e as conversões
    """
    
    # Inicializar listas vazias
    evidence = []   # Vai guardar as 17 características de cada sessão
    labels = []     # Vai guardar se comprou (1) ou não (0)
    
    # IMPORTANTE PARA APRESENTAÇÃO: Dicionário para converter meses
    # No CSV está "Jan", "Feb" etc. → Precisamos de números (0-11)
    months = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    
    # Abrir ficheiro CSV
    with open(filename, 'r') as file:
        # IMPORTANTE: DictReader lê cada linha como dicionário
        # Permite aceder aos valores pelo nome: row["Month"]
        reader = csv.DictReader(file)

        # Processar cada sessão de utilizador (12.330 no total)
        for row in reader:
            # Criar lista com 17 FEATURES NUMÉRICAS para este utilizador
            # APRESENTAÇÃO: Destacar as conversões int() e float()
            user_evidence = [
                # Features 0-5: Páginas visitadas e durações
                int(row["Administrative"]),              # Nº páginas admin
                float(row["Administrative_Duration"]),   # Tempo em admin
                int(row["Informational"]),               # Nº páginas info
                float(row["Informational_Duration"]),    # Tempo em info
                int(row["ProductRelated"]),              # Nº páginas produtos
                float(row["ProductRelated_Duration"]),   # Tempo em produtos
                
                # Features 6-9: Métricas do Google Analytics
                float(row["BounceRates"]),               # Taxa de rejeição
                float(row["ExitRates"]),                 # Taxa de saída
                float(row["PageValues"]),                # Valor da página
                float(row["SpecialDay"]),                # Proximidade a data especial
                
                # Feature 10: AQUI USA O DICIONÁRIO! "Feb" → 1
                months[row["Month"]],
                
                # Features 11-14: Informação técnica do utilizador
                int(row["OperatingSystems"]),            # Sistema operativo
                int(row["Browser"]),                     # Navegador
                int(row["Region"]),                      # Região geográfica
                int(row["TrafficType"]),                 # Tipo de tráfego
                
                # Feature 15: EXPRESSÃO CONDICIONAL TERNÁRIA
                # Se "Returning_Visitor" → 1, senão → 0
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                
                # Feature 16: Outra expressão condicional
                # Se "TRUE" → 1, senão → 0
                1 if row["Weekend"] == "TRUE" else 0
            ]
            
            # Adicionar esta sessão à lista geral
            evidence.append(user_evidence)
            
            # Adicionar o LABEL: comprou (1) ou não (0)
            # Esta é a variável que queremos PREVER!
            labels.append(1 if row["Revenue"] == "TRUE" else 0)
    
    # Retornar dados processados
    # No final: 12.330 listas de 17 números + 12.330 labels
    return (evidence, labels)


def train_model(evidence, labels):
    """
    ═══════════════════════════════════════════════════════════════
    FUNÇÃO 2 (OBRIGATÓRIA): TREINAR MODELO KNN
    ═══════════════════════════════════════════════════════════════
    
    Treina um classificador K-Nearest Neighbors com k=1.
    
    INPUT: evidence (lista de features), labels (lista de resultados)
    OUTPUT: Modelo treinado pronto para fazer previsões
    
    APRESENTAÇÃO: Explicar o que é KNN com analogia:
    "Procura o vizinho mais parecido no histórico e prevê o mesmo"
    """
    
    # Criar classificador KNN com k=1 (apenas 1 vizinho mais próximo)
    # APRESENTAÇÃO: k=1 significa "olha só para a pessoa MAIS parecida"
    model = KNeighborsClassifier(n_neighbors=1)
    
    # TREINAR o modelo - aqui acontece a "aprendizagem"!
    # O modelo MEMORIZA os 12.330 exemplos e seus resultados
    # ANALOGIA: Como mostrar 12.330 exemplos a um estudante
    model.fit(evidence, labels)
    
    # Retornar modelo treinado
    return model


def evaluate(labels, predictions):
    """
    ═══════════════════════════════════════════════════════════════
    FUNÇÃO 3 (OBRIGATÓRIA): AVALIAR QUALIDADE DO MODELO
    ═══════════════════════════════════════════════════════════════
    
    Calcula Sensitivity e Specificity do modelo.
    
    INPUT: labels reais, predictions do modelo
    OUTPUT: (sensitivity, specificity)
    
    APRESENTAÇÃO: Explicar com exemplos:
    - Sensitivity: "Dos que compraram, quantos % acertei?"
    - Specificity: "Dos que NÃO compraram, quantos % acertei?"
    """
    
    # Inicializar contadores
    # APRESENTAÇÃO: Explicar TP, TN com exemplos concretos
    true_positives = 0   # Previu compra E comprou → ACERTOU!
    true_negatives = 0   # Previu não-compra E não comprou → ACERTOU!
    total_positives = 0  # Total de compradores reais
    total_negatives = 0  # Total de não-compradores reais
    
    # Percorrer todas as previsões
    # zip() permite iterar sobre duas listas simultaneamente
    for actual, predicted in zip(labels, predictions):
        # Se a pessoa REALMENTE COMPROU (actual = 1)
        if actual == 1:
            total_positives += 1
            # E o modelo TAMBÉM PREVIU compra (predicted = 1)
            if predicted == 1:
                true_positives += 1  # ACERTOU!
        # Se a pessoa NÃO COMPROU (actual = 0)
        else:
            total_negatives += 1
            # E o modelo TAMBÉM PREVIU não-compra (predicted = 0)
            if predicted == 0:
                true_negatives += 1  # ACERTOU!
    
    # Calcular SENSITIVITY (True Positive Rate)
    # Fórmula: TP / Total Positivos
    # APRESENTAÇÃO: "Dos 100 compradores, identifiquei 41" → 41%
    sensitivity = true_positives / total_positives if total_positives > 0 else 0
    
    # Calcular SPECIFICITY (True Negative Rate)
    # Fórmula: TN / Total Negativos
    # APRESENTAÇÃO: "Dos 1000 não-compradores, identifiquei 910" → 91%
    specificity = true_negatives / total_negatives if total_negatives > 0 else 0
    
    # Retornar as duas métricas
    return (sensitivity, specificity)


def validate_data(evidence, labels):
    """
    ═══════════════════════════════════════════════════════════════
    FEATURE EXTRA 1 (COMPLEXA): VALIDAÇÃO DE DADOS
    ═══════════════════════════════════════════════════════════════
    
    PROMPT USADO:   "Cria função para validar dados de ML. Verifica:
                    17 features por entrada, labels 0 ou 1, sem None."
    
    VALOR: Previne crashes durante o treino ao validar dados primeiro.
    
    APRESENTAÇÃO: Mostrar que é executada ANTES do treino e o output
    "✓ Validação: 12330 entradas válidas..."
    """
    
    errors = []  # Lista para acumular erros encontrados
    
    # VALIDAÇÃO 1: Verificar se há dados
    if len(evidence) == 0:
        errors.append("Nenhum dado foi carregado")
        return (False, errors)
    
    # VALIDAÇÃO 2: Verificar número de features (deve ser 17)
    expected_features = 17
    for i, entry in enumerate(evidence):
        if len(entry) != expected_features:
            errors.append(f"Entrada {i}: esperadas {expected_features} features, encontradas {len(entry)}")
            if len(errors) >= 5:  # Limitar mensagens
                break
    
    # VALIDAÇÃO 3: Verificar labels válidos (apenas 0 ou 1)
    valid_labels = {0, 1}
    for i, label in enumerate(labels):
        if label not in valid_labels:
            errors.append(f"Label {i}: valor inválido {label} (deve ser 0 ou 1)")
            if len(errors) >= 10:
                break
    
    # VALIDAÇÃO 4: Verificar valores None
    for i, entry in enumerate(evidence[:100]):  # Verificar primeiras 100
        if None in entry:
            errors.append(f"Entrada {i}: contém valores None")
    
    # Determinar se é válido
    is_valid = len(errors) == 0
    
    # Mostrar mensagem apropriada
    if is_valid:
        print(f"✓ Validação: {len(evidence)} entradas válidas com {expected_features} features cada")
    else:
        print(f"✗ Validação: encontrados {len(errors)} erros")
    
    return (is_valid, errors)


def analyze_dataset(evidence, labels):
    """
    ═══════════════════════════════════════════════════════════════
    FEATURE EXTRA 2 (REGULAR): ANÁLISE ESTATÍSTICA
    ═══════════════════════════════════════════════════════════════
    
    PROMPT USADO:   "Cria função de análise estatística. Conta
                    positivos/negativos, calcula percentagens,
                    alerta se desbalanceado (< 30%)."
    
    VALOR:  Explica PORQUÊ sensitivity é 41% e specificity 91%.
            Dataset desbalanceado: 85% não compram!
    
    APRESENTAÇÃO: Mostrar o quadro formatado que aparece no output.
    """
    
    # Contar compradores e não-compradores
    total = len(labels)
    positives = sum(labels)       # Quantos compraram (label=1)
    negatives = total - positives # Quantos não compraram (label=0)
    
    # Mostrar estatísticas formatadas
    print("\n" + "="*50)
    print("📊 ANÁLISE DO DATASET")
    print("="*50)
    print(f"Total de sessões: {total}")
    print(f"Compradores: {positives} ({100*positives/total:.1f}%)")
    print(f"Não-compradores: {negatives} ({100*negatives/total:.1f}%)")
    print(f"Rácio: 1:{negatives/positives:.1f}")
    
    # Verificar balance do dataset
    # APRESENTAÇÃO: Isto explica porque specificity é alta (91%)!
    # O modelo vê 5.5x mais não-compradores, aprende melhor a identificá-los
    if positives / total < 0.3:
        print("⚠️  Dataset desbalanceado (poucos compradores)")
    else:
        print("✓ Dataset razoavelmente balanceado")
    
    print("="*50 + "\n")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()