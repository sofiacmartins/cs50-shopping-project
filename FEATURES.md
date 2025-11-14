# 📚 Índice de Features do Projeto Shopping

## 🎯 Features Principais (Obrigatórias)

### 1. load_data(filename)
- **Descrição**: Carrega e processa dados do CSV
- **Ficheiro**: `shopping.py` (linhas ~30-80)
- **Input**: Nome do ficheiro CSV
- **Output**: Tuplo (evidence, labels)
- **Função**: Converte 12.330 sessões em formato numérico para ML
- **Branch**: `feature/load-data`

### 2. train_model(evidence, labels)
- **Descrição**: Treina classificador KNN
- **Ficheiro**: `shopping.py` (linhas ~83-93)
- **Input**: Evidências e labels de treino
- **Output**: Modelo KNN treinado
- **Função**: Cria modelo com k=1 e treina com dados históricos
- **Branch**: `feature/train-model`

### 3. evaluate(labels, predictions)
- **Descrição**: Calcula métricas de avaliação
- **Ficheiro**: `shopping.py` (linhas ~96-130)
- **Input**: Labels reais e previsões do modelo
- **Output**: Tuplo (sensitivity, specificity)
- **Função**: Avalia performance com TPR e TNR
- **Branch**: `feature/evaluate`

---

## ✨ Features Extra (Desenvolvidas com IA)

### 🛡️ 1. Validação de Dados
- **Branch**: `feature/validacao-dados`
- **Documentação**: [FEATURE_validacao.md](FEATURE_validacao.md)
- **Função**: `validate_data(evidence, labels)`
- **Ficheiro**: `shopping.py` (linhas ~133-170)
- **Descrição**: Sistema de validação automática de integridade dos dados

#### Verificações:
- ✅ Cada entrada tem exatamente 17 features
- ✅ Labels são apenas 0 ou 1
- ✅ Sem valores None ou vazios
- ✅ Dataset não está vazio

#### Benefícios:
- 🛡️ Previne erros antes do treino
- 📋 Mensagens de erro claras
- 🚫 Evita crashes durante execução
- ✅ Aumenta confiabilidade do sistema

#### Desenvolvimento:
- **Ferramenta IA**: Claude (Anthropic)
- **Prompt**: "Cria função para validar dados de ML com 17 features e labels 0/1"
- **Iterações**: 4 versões até versão final

---

### 📊 2. Análise Estatística
- **Branch**: `feature/analise-estatistica`
- **Documentação**: [FEATURE_analise.md](FEATURE_analise.md)
- **Função**: `analyze_dataset(evidence, labels)`
- **Ficheiro**: `shopping.py` (linhas ~173-195)
- **Descrição**: Análise automática da distribuição do dataset

#### Métricas Calculadas:
- 📈 Total de sessões
- 🔢 Distribuição de classes (compradores vs não-compradores)
- 📊 Percentagens de cada classe
- ⚖️ Rácio entre classes
- ⚠️ Alerta de desbalanceamento

#### Insights:
- Dataset tem 12.330 sessões
- Apenas 15.5% são compradores (desbalanceado)
- Rácio de 1:5.5 (não-comprador:comprador)
- Explica specificity alta (91%) vs sensitivity baixa (41%)

#### Desenvolvimento:
- **Ferramenta IA**: Claude (Anthropic)
- **Prompt**: "Cria função para análise estatística de dataset ML com alerta de desbalanceamento"
- **Iterações**: 4 versões com melhorias incrementais

---

## 🤖 Processo de Desenvolvimento com IA

### Metodologia Utilizada:

1. **Identificação da Necessidade**
   - Análise do problema
   - Definição de requisitos

2. **Formulação do Prompt**
   - Prompt claro e específico
   - Contexto completo

3. **Recepção e Análise**
   - Avaliação da sugestão da IA
   - Verificação de qualidade

4. **Implementação**
   - Adaptação ao código existente
   - Testes e validação

5. **Documentação**
   - Registo do processo
   - Ficheiro FEATURE_*.md

### Prompts Utilizados:

#### Feature 1 - Validação:
```
"Cria uma função em Python para validar dados de machine learning.
Deve verificar se cada entrada tem 17 features, se os labels são 0 ou 1,
e se não há valores None. Retorna tuplo (is_valid, errors)."
```

#### Feature 2 - Análise:
```
"Cria uma função Python que analise um dataset de machine learning.
Deve contar labels positivos e negativos, calcular percentagens,
mostrar rácio, e alertar se está desbalanceado (menos de 30% positivos)."
```

---

## 📊 Comparação de Features

| Feature | Tipo | Linhas Código | Complexidade | Impacto | IA Usada |
|---------|------|---------------|--------------|---------|----------|
| load_data | Obrigatória | ~50 | Média | ⭐⭐⭐ Crítico | Não |
| train_model | Obrigatória | ~10 | Baixa | ⭐⭐⭐ Crítico | Não |
| evaluate | Obrigatória | ~35 | Média | ⭐⭐⭐ Crítico | Não |
| validate_data | Extra | ~40 | Média | ⭐⭐ Alto | Sim |
| analyze_dataset | Extra | ~25 | Baixa | ⭐⭐ Médio | Sim |

---

## 🔄 Fluxo de Execução
```
1. Carregar dados (load_data)
   ↓
2. Validar dados (validate_data) ← EXTRA
   ↓ [se válido]
3. Analisar dataset (analyze_dataset) ← EXTRA
   ↓
4. Dividir treino/teste (train_test_split)
   ↓
5. Treinar modelo (train_model)
   ↓
6. Fazer previsões (model.predict)
   ↓
7. Avaliar resultados (evaluate)
   ↓
8. Mostrar métricas
```

---

## 🔍 Como Usar Este Índice

### Para entender uma feature:
1. Consulta a tabela de comparação
2. Lê a descrição resumida aqui
3. Vai ao ficheiro `FEATURE_*.md` para detalhes
4. Consulta o código em `shopping.py`

### Para adicionar nova feature:
1. Cria branch `feature/nome`
2. Implementa a função
3. Testa thoroughly
4. Cria `FEATURE_nome.md`
5. Atualiza este índice
6. Faz commit e merge

---

## 📁 Documentação Relacionada

- [README.md](README.md) - Documentação principal do projeto
- [FEATURE_validacao.md](FEATURE_validacao.md) - Feature de validação
- [FEATURE_analise.md](FEATURE_analise.md) - Feature de análise
- `shopping.py` - Código fonte completo

---

## 📈 Estatísticas do Projeto

- **Total de Funções**: 5
- **Funções Obrigatórias**: 3
- **Features Extra com IA**: 2
- **Linhas de Código**: ~200
- **Ficheiros de Documentação**: 4
- **Branches Criados**: 5+
- **Commits**: 10+

---

## 🎓 Aprendizagens com Features Extra

### Técnicas:
- ✅ Validação de dados em ML
- ✅ Análise exploratória de datasets
- ✅ Tratamento de erros robusto
- ✅ Formatação de output informativo

### Uso de IA:
- ✅ Formulação de prompts eficazes
- ✅ Integração de sugestões de IA
- ✅ Documentação do processo
- ✅ Validação de código gerado

---

**Última atualização**: Novembro 2025  
**Desenvolvido por**: Sofia Martins
**Ferramenta IA**: Claude (Anthropic)