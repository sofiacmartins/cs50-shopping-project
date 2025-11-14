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

Desenvolvido por: Sofia
Data: Novembro 2025
Curso: Inteligência Artificial - 3º Ano
Ferramentas IA: Claude (Anthropic)
Projeto: CS50's Introduction to Artificial Intelligence with Python
"""

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet
    evidence, labels = load_data(sys.argv[1])
    
    # Validate data ANTES de treinar
    is_valid, errors = validate_data(evidence, labels)
    if not is_valid:
        print("Erros encontrados:")
        for error in errors[:10]:  # Mostrar apenas primeiros 10
            print(f"  - {error}")
        sys.exit(1)
    
    analyze_dataset(evidence, labels)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    
    # Mapeamento de meses para números
    months = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Criar lista de evidências (17 features)
            user_evidence = [
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                months[row["Month"]],
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ]
            
            evidence.append(user_evidence)
            labels.append(1 if row["Revenue"] == "TRUE" else 0)
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Criar classificador KNN com k=1
    model = KNeighborsClassifier(n_neighbors=1)
    
    # Treinar o modelo
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives = 0
    true_negatives = 0
    total_positives = 0
    total_negatives = 0
    
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            total_positives += 1
            if predicted == 1:
                true_positives += 1
        else:
            total_negatives += 1
            if predicted == 0:
                true_negatives += 1
    
    # Calcular métricas
    sensitivity = true_positives / total_positives if total_positives > 0 else 0
    specificity = true_negatives / total_negatives if total_negatives > 0 else 0
    
    return (sensitivity, specificity)


def validate_data(evidence, labels):
    """
    Valida se os dados carregados estão corretos.
    
    Verifica:
    - Número de features por entrada
    - Tipos de dados corretos
    - Labels válidos (0 ou 1)
    - Sem valores None ou vazios
    
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Verificar se há dados
    if len(evidence) == 0:
        errors.append("Nenhum dado foi carregado")
        return (False, errors)
    
    # Verificar número de features
    expected_features = 17
    for i, entry in enumerate(evidence):
        if len(entry) != expected_features:
            errors.append(f"Entrada {i}: esperadas {expected_features} features, encontradas {len(entry)}")
            if len(errors) >= 5:  # Limitar mensagens de erro
                break
    
    # Verificar labels
    valid_labels = {0, 1}
    for i, label in enumerate(labels):
        if label not in valid_labels:
            errors.append(f"Label {i}: valor inválido {label} (deve ser 0 ou 1)")
            if len(errors) >= 10:
                break
    
    # Verificar valores None
    for i, entry in enumerate(evidence[:100]):  # Verificar primeiras 100
        if None in entry:
            errors.append(f"Entrada {i}: contém valores None")
    
    is_valid = len(errors) == 0
    
    if is_valid:
        print(f"✓ Validação: {len(evidence)} entradas válidas com {expected_features} features cada")
    else:
        print(f"✗ Validação: encontrados {len(errors)} erros")
    
    return (is_valid, errors)

def analyze_dataset(evidence, labels):
    """
    Analisa estatísticas básicas do dataset.
    
    Mostra:
    - Total de entradas
    - Distribuição de labels (compradores vs não-compradores)
    - Percentagem de cada classe
    - Balance do dataset
    """
    total = len(labels)
    positives = sum(labels)  # Quantos compraram (label=1)
    negatives = total - positives  # Quantos não compraram (label=0)
    
    print("\n" + "="*50)
    print("📊 ANÁLISE DO DATASET")
    print("="*50)
    print(f"Total de sessões: {total}")
    print(f"Compradores (label=1): {positives} ({100*positives/total:.1f}%)")
    print(f"Não-compradores (label=0): {negatives} ({100*negatives/total:.1f}%)")
    print(f"Rácio: 1:{negatives/positives:.1f}")
    
    # Verificar balance
    if positives / total < 0.3:
        print("⚠️  Dataset desbalanceado (poucos compradores)")
    else:
        print("✓ Dataset razoavelmente balanceado")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    main()