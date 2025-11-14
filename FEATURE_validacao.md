# 🛡️ FEATURE: Validação de Dados

## 📋 Descrição

Sistema de validação automática dos dados carregados do CSV antes do treino do modelo.

## 🎯 Objetivo

Garantir que os dados estão no formato correto para evitar erros durante o treino e aumentar a confiabilidade do sistema.

## ⚙️ Funcionalidades

### `validate_data(evidence, labels)`

Valida os dados carregados verificando:

1. **Número de Features**: Cada entrada deve ter exatamente 17 features
2. **Labels Válidos**: Apenas valores 0 ou 1
3. **Valores None**: Não pode haver valores vazios
4. **Dados Carregados**: Verificar se o dataset não está vazio

## 📊 Output
```
✓ Validação: 12330 entradas válidas com 17 features cada
```

Ou em caso de erro:
```
✗ Validação: encontrados 3 erros
Erros encontrados:
  - Entrada 42: esperadas 17 features, encontradas 16
  - Label 105: valor inválido 2 (deve ser 0 ou 1)
```

## 🤖 Desenvolvimento com IA

Esta feature foi desenvolvida com ajuda do Claude (Anthropic).

### Prompt Usado:
```
"Cria uma função em Python para validar dados de machine learning.
Deve verificar se cada entrada tem 17 features, se os labels são 0 ou 1,
e se não há valores None. Retorna tuplo (is_valid, errors)."
```

### Output da IA:
- Sugestão de estrutura da função
- Verificações necessárias (número de features, labels válidos, valores None)
- Formatação de mensagens de erro claras
- Integração com função main()
- Uso de lista para acumular erros

### Iterações:
1. **V1**: Validação básica de features
2. **V2**: Adicionada validação de labels
3. **V3**: Adicionada verificação de valores None
4. **V4**: Melhoradas mensagens de output

## 📈 Benefícios

- ✅ Deteta erros de dados antes do treino
- ✅ Mensagens de erro claras e úteis
- ✅ Evita crashes durante execução
- ✅ Aumenta confiabilidade do sistema
- ✅ Poupa tempo de debugging

## 🔧 Uso

A validação é executada automaticamente após `load_data()` e antes do treino.
Se houver erros, o programa termina e mostra as mensagens.
```python
# Exemplo de uso na main()
evidence, labels = load_data(sys.argv[1])

is_valid, errors = validate_data(evidence, labels)
if not is_valid:
    print("Erros encontrados:")
    for error in errors[:10]:
        print(f"  - {error}")
    sys.exit(1)
```

## 📅 Informação

- **Desenvolvido**: Novembro 2025
- **Branch**: feature/validacao-dados
- **Ferramenta IA**: Claude (Anthropic)
- **Linhas de Código**: ~40
- **Impacto**: Alto (previne erros críticos)