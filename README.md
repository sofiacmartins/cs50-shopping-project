# 🛒 Shopping - Previsão de Compras com IA

## 📖 Introdução

Este projeto implementa um classificador de machine learning baseado no algoritmo **K-Nearest Neighbors (KNN)** para prever se um cliente numa loja online irá completar uma compra. O sistema analisa 17 características diferentes do comportamento de navegação do utilizador, incluindo páginas visitadas, duração das visitas, taxas de rejeição e informações demográficas.

## 🎯 Descrição do Projeto

### Objetivo
Desenvolver um sistema de previsão que ajude websites de e-commerce a identificar clientes com maior probabilidade de compra, permitindo personalizar a experiência do utilizador (por exemplo: mostrar descontos especiais a utilizadores indecisos).

### Funcionalidades Implementadas

#### 1. **load_data(filename)**
Carrega e processa dados do ficheiro CSV:
- Lê 12.330 sessões de utilizadores do ficheiro shopping.csv
- Converte tipos de dados corretamente (int/float conforme especificação)
- Mapeia meses para valores numéricos (Jan=0, Fev=1, ..., Dez=11)
- Processa VisitorType (1=Visitante Recorrente, 0=Novo Visitante)
- Processa Weekend (1=Fim de semana, 0=Dia de semana)
- Processa Revenue como label (1=Comprou, 0=Não comprou)
- Retorna tuplo (evidence, labels) com dados prontos para treino

#### 2. **train_model(evidence, labels)**
Treina o classificador KNN:
- Utiliza algoritmo K-Nearest Neighbors com k=1 (1 vizinho mais próximo)
- Implementado com biblioteca scikit-learn (KNeighborsClassifier)
- Aprende padrões de comportamento a partir de dados históricos
- Retorna modelo treinado pronto para fazer previsões

#### 3. **evaluate(labels, predictions)**
Avalia a performance do modelo:
- **Sensitivity** (True Positive Rate): proporção de compradores corretamente identificados
- **Specificity** (True Negative Rate): proporção de não-compradores corretamente identificados
- Retorna tuplo (sensitivity, specificity) com valores entre 0 e 1

#### 4. **validate_data(evidence, labels)** ✨ EXTRA
Sistema de validação automática:
- Verifica se cada entrada tem exatamente 17 features
- Valida que labels são apenas 0 ou 1
- Deteta valores None ou vazios
- Previne erros antes do treino
- **Documentação**: [FEATURE_validacao.md](FEATURE_validacao.md)

#### 5. **analyze_dataset(evidence, labels)** ✨ EXTRA
Análise estatística automática:
- Mostra total de sessões e distribuição de classes
- Calcula percentagens e rácios
- Alerta sobre desbalanceamento do dataset
- Ajuda a interpretar resultados do modelo
- **Documentação**: [FEATURE_analise.md](FEATURE_analise.md)

### Dataset
- **12.330 sessões de utilizadores** reais de um website de e-commerce
- **17 features** de comportamento de navegação
- **1 label** binária (comprou=TRUE / não comprou=FALSE)

#### Colunas do Dataset:
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| Administrative | int | Nº de páginas administrativas visitadas |
| Administrative_Duration | float | Tempo gasto em páginas administrativas |
| Informational | int | Nº de páginas informativas visitadas |
| Informational_Duration | float | Tempo gasto em páginas informativas |
| ProductRelated | int | Nº de páginas de produtos visitadas |
| ProductRelated_Duration | float | Tempo gasto em páginas de produtos |
| BounceRates | float | Taxa de rejeição (Google Analytics) |
| ExitRates | float | Taxa de saída (Google Analytics) |
| PageValues | float | Valor médio da página (Google Analytics) |
| SpecialDay | float | Proximidade a datas especiais (0-1) |
| Month | int | Mês da visita (0=Jan, 11=Dez) |
| OperatingSystems | int | Sistema operativo do utilizador |
| Browser | int | Navegador utilizado |
| Region | int | Região geográfica |
| TrafficType | int | Tipo de tráfego |
| VisitorType | int | 1=Recorrente, 0=Novo |
| Weekend | int | 1=Fim de semana, 0=Dia de semana |
| **Revenue** | int | **1=Comprou, 0=Não comprou (TARGET)** |

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **scikit-learn 1.6.0**: Biblioteca de machine learning (KNeighborsClassifier)
- **csv**: Módulo standard Python para processamento de ficheiros CSV
- **Git**: Sistema de controlo de versões com conventional commits

## 🤖 Ferramentas de IA Utilizadas

Durante o desenvolvimento deste projeto, utilizei o **Claude (Anthropic)** como assistente de programação para auxiliar em várias etapas do desenvolvimento.

### Exemplos de Prompts e Outputs

#### Prompt 1: Estrutura da Função load_data
```
"Como devo estruturar a função load_data() para ler o CSV e converter 
os dados nos tipos corretos? Preciso de mapear meses, VisitorType e Weekend."
```

**Output recebido:**
- Usar `csv.DictReader` para ler o ficheiro linha a linha
- Criar dicionário para mapear meses: `{"Jan": 0, "Feb": 1, ..., "Dec": 11}`
- Converter Administrative, Informational, ProductRelated para `int()`
- Converter durações, BounceRates, ExitRates, PageValues para `float()`
- Para VisitorType: `1 if row["VisitorType"] == "Returning_Visitor" else 0`
- Para Weekend: `1 if row["Weekend"] == "TRUE" else 0`
- Para Revenue (label): `1 if row["Revenue"] == "TRUE" else 0`
- Retornar tuplo `(evidence, labels)`

#### Prompt 2: Algoritmo KNN
```
"Explica-me como funciona o algoritmo K-Nearest Neighbors 
e porque usamos k=1 neste projeto?"
```

**Output recebido:**
- **KNN** é um algoritmo de classificação baseado em proximidade
- Funciona encontrando os K vizinhos mais próximos de um ponto
- **k=1** significa olhar apenas para o vizinho mais próximo
- **Vantagens de k=1**: Simples, rápido, fronteiras de decisão flexíveis
- **Desvantagens**: Sensível a outliers, pode ter overfitting
- Para treinar: `model = KNeighborsClassifier(n_neighbors=1)` e depois `model.fit(evidence, labels)`

#### Prompt 3: Métricas de Avaliação
```
"Qual a diferença entre sensitivity e specificity? 
Como calculo estas métricas no código?"
```

**Output recebido:**
- **Sensitivity** (Sensibilidade): Taxa de Verdadeiros Positivos
  - Fórmula: `TP / (TP + FN)` = Positivos Reais / Total de Positivos
  - Pergunta: "Dos clientes que compraram, quantos identifiquei?"
- **Specificity** (Especificidade): Taxa de Verdadeiros Negativos
  - Fórmula: `TN / (TN + FP)` = Negativos Reais / Total de Negativos
  - Pergunta: "Dos clientes que não compraram, quantos identifiquei?"
- Implementação: Iterar sobre pares (label_real, previsão) e contar TP, TN, totais

#### Prompt 4: Feature de Validação
```
"Cria uma função em Python para validar dados de machine learning.
Deve verificar se cada entrada tem 17 features, se os labels são 0 ou 1,
e se não há valores None. Retorna tuplo (is_valid, errors)."
```

**Output recebido:**
- Estrutura da função com lista de erros
- Verificação de número de features por entrada
- Validação de labels (apenas 0 ou 1)
- Deteção de valores None
- Mensagens de erro informativas
- Integração na função main() antes do treino

#### Prompt 5: Feature de Análise Estatística
```
"Cria uma função Python que analise um dataset de machine learning.
Deve contar labels positivos e negativos, calcular percentagens,
mostrar rácio, e alertar se está desbalanceado (menos de 30% positivos)."
```

**Output recebido:**
- Cálculo de totais e distribuição de classes
- Fórmulas para percentagens e rácios
- Lógica para detetar desbalanceamento
- Formatação visual com separadores
- Mensagens informativas
- Explicação do impacto do desbalanceamento nos resultados

## 🚀 Como Executar

### Pré-requisitos
```bash
# Python 3.11 ou superior
python --version

# Instalar dependências
pip install scikit-learn
```

### Execução
```bash
# Executar o programa
python shopping.py shopping.csv
```

### Output Esperado
```
✓ Validação: 12330 entradas válidas com 17 features cada

==================================================
📊 ANÁLISE DO DATASET
==================================================
Total de sessões: 12330
Compradores (label=1): 1908 (15.5%)
Não-compradores (label=0): 10422 (84.5%)
Rácio: 1:5.5
⚠️  Dataset desbalanceado (poucos compradores)
==================================================

Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%
```

## 📊 Resultados e Análise

### Métricas Obtidas
- **Previsões Corretas**: 4.088 (82.9%)
- **Previsões Incorretas**: 844 (17.1%)
- **Sensitivity (TPR)**: 41.02% - identifica 41% dos compradores
- **Specificity (TNR)**: 90.55% - identifica 91% dos não-compradores

### Interpretação dos Resultados

#### Pontos Fortes ✅
1. **Alta Specificity (91%)**: O modelo é excelente a identificar quem NÃO vai comprar
2. **Precisão Geral Boa (83%)**: Acima do baseline (85% se prevíssemos sempre "não compra")

#### Limitações ⚠️
1. **Sensitivity Moderada (41%)**: Perde mais de metade dos compradores reais
2. **Assimetria**: Desempenho desigual entre as duas classes (reflexo do dataset desbalanceado)

### Aplicações Práticas no E-Commerce

| Cenário | Aplicação | Benefício |
|---------|-----------|-----------|
| 🎯 Marketing Direcionado | Oferecer cupões apenas a quem o modelo prevê "não compra" | Redução de custos |
| 💰 Otimização de Descontos | Não dar descontos a compradores identificados | Maximização de receita |
| 🚀 UX Personalizada | Simplificar checkout para compradores prováveis | Melhor experiência |

## 📚 Aprendizagens

### Conhecimentos Técnicos
1. **Machine Learning Supervisionado**: Classificação binária com KNN
2. **Pré-processamento de Dados**: Conversão e normalização
3. **Métricas de Avaliação**: Sensitivity vs Specificity
4. **Python Científico**: scikit-learn e manipulação de CSV

### Competências de Desenvolvimento
1. **Git e Controlo de Versões**: Workflow com branches e conventional commits
2. **Documentação Técnica**: READMEs e documentação de features
3. **Uso de IA**: Integração de assistentes AI no workflow
4. **Análise Crítica**: Interpretação de resultados e limitações

## 📁 Estrutura do Projeto
```
shopping/
├── shopping.py              # Código principal (5 funções)
├── shopping.csv             # Dataset (12.330 sessões)
├── README.md                # Documentação principal (este ficheiro)
├── FEATURES.md              # Índice de features
├── FEATURE_validacao.md     # Doc da feature de validação
├── FEATURE_analise.md       # Doc da feature de análise
└── .gitignore              # Ficheiros ignorados pelo Git
```

## 🔄 Histórico de Desenvolvimento

O projeto foi desenvolvido seguindo boas práticas de Git com conventional commits:
```
1. chore: adiciona gitignore
2. chore: adiciona código base e dataset
3. feat: implementa função load_data
4. feat: implementa função train_model
5. feat: implementa função evaluate
6. feat: adiciona sistema de validação de dados
7. feat: adiciona análise estatística do dataset
8. docs: cria documentação completa do projeto
```

Ver: [FEATURES.md](FEATURES.md) para índice completo de features.

## 👤 Autora

**Sofia**  
Curso: Inteligência Artificial - 3º Ano  
Data: Novembro 2025

## 📖 Referências

### Dataset
- Sakar, C.O., Polat, S.O., Katircioglu, M. et al. (2018)  
  Neural Computing and Applications

### Documentação Técnica
- [scikit-learn: K-Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)
- [Python CSV Documentation](https://docs.python.org/3/library/csv.html)

### Curso
- CS50's Introduction to Artificial Intelligence with Python

### Ferramentas de IA
- Claude (Anthropic) - Assistente de programação

## 📅 Informação de Submissão

- **Prazo**: 1 de Julho de 2026, 00:59 GMT+1
- **Plataforma**: CS50 AI (submit50)
- **Avaliação**: check50 + style50 + Git + Documentação

---

**Desenvolvido com 🧠 Machine Learning e 💻 Python**