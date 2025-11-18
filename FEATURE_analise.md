# 📊 FEATURE: Análise Estatística do Dataset

## 📋 Descrição

Sistema de análise automática que mostra estatísticas do dataset antes do treino.

## 🎯 Objetivo

Fornecer insights sobre a distribuição dos dados para melhor compreensão do problema e dos resultados esperados.

## ⚙️ Funcionalidades

### `analyze_dataset(evidence, labels)`

Calcula e exibe:

1. **Total de Entradas**: Número total de sessões no dataset
2. **Distribuição de Classes**: 
   - Quantos compraram (label=1)
   - Quantos não compraram (label=0)
3. **Percentagens**: Proporção de cada classe
4. **Rácio**: Relação entre não-compradores e compradores
5. **Aviso de Desbalanceamento**: Alerta se dataset está desbalanceado

## 📊 Output Exemplo
```
==================================================
📊 ANÁLISE DO DATASET
==================================================
Total de sessões: 12330
Compradores (label=1): 1908 (15.5%)
Não-compradores (label=0): 10422 (84.5%)
Rácio: 1:5.5
⚠️  Dataset desbalanceado (poucos compradores)
==================================================
```

## 🤖 Desenvolvimento com IA

Esta feature foi desenvolvida com assistência do **Claude (Anthropic)**.

### Prompt Usado:
```
"Cria uma função Python que analise um dataset de machine learning.
Deve contar labels positivos e negativos, calcular percentagens,
mostrar rácio, e alertar se está desbalanceado (menos de 30% positivos)."
```

### Output da IA:
- Estrutura da função de análise
- Cálculos de percentagens e rácios
- Formatação visual com separadores
- Lógica para detetar desbalanceamento
- Mensagens informativas com emojis

### Iterações:
1. **V1**: Análise básica com contagens
2. **V2**: Adicionadas percentagens e rácios
3. **V3**: Adicionado alerta de desbalanceamento
4. **V4**: Melhorada formatação visual

## 📈 Insights Obtidos

Com esta análise descobrimos que:

- ✅ O dataset tem 12.330 sessões
- ⚠️ Apenas 15.5% são compradores (desbalanceado)
- 📊 Rácio de 1:5.5 (não-comprador:comprador)
- 🎯 Isto explica a specificity alta (91%) vs sensitivity baixa (41%)

## 💡 Implicações

O desbalanceamento explica porque:
- O modelo é melhor a prever "não vai comprar"
- A sensitivity é apenas 41% (perde muitos compradores)
- Um baseline de "sempre prever não-compra" teria 84.5% accuracy

## 🔧 Uso

A análise é executada automaticamente após validação e antes do treino.
Não requer input do utilizador.
```python
# Exemplo de uso na main()
is_valid, errors = validate_data(evidence, labels)
if not is_valid:
    sys.exit(1)

analyze_dataset(evidence, labels)  # ← Chamada automática
```

## 📅 Informação

- **Desenvolvido**: Novembro 2025
- **Branch**: feature/analise-estatistica
- **Ferramenta IA**: Claude (Anthropic)
- **Linhas de Código**: ~25
- **Impacto**: Médio-Alto (insights importantes)git 