import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Gestor Lucro Certo | MEI, ME & EPP", page_icon="📈", layout="wide"
)

# Estilização do Cabeçalho
st.title("📈 Gestor de Margem & Preço de Venda Inteligente")
st.markdown(
    "Ferramenta de diagnóstico e formação de preço com inteligência operacional"
    " e contábil."
)

# Menu Lateral
menu = st.sidebar.selectbox(
    "Navegação do Sistema",
    [
        "1. Formação de Preço & Anamnese",
        "2. Simulador de Descontos e Impacto",
        "3. Guia Contábil: Água, Luz e Custos Fixos",
    ],
)

# -------------------------------------------------------------
# MÓDULO 1: FORMAÇÃO DE PREÇO COM ANAMNESE OPERACIONAL
# -------------------------------------------------------------
if menu == "1. Formação de Preço & Anamnese":
  st.header("🎯 Diagnóstico Operacional e Formação de Preço")
  st.markdown(
      "Responda às perguntas abaixo para que o sistema calcule automaticamente o"
      " frete unitário, a embalagem e o rateio de água e luz."
  )

  with st.expander(
      "📋 Anamnese Operacional (Clique para abrir/fechar as perguntas)",
      expanded=True,
  ):
    st.subheader("1. Custos de Logística e Insumos")
    col_a, col_b = st.columns(2)
    with col_a:
      custo_produto = st.number_input(
          "Custo de Aquisição / Produção da Matéria-Prima (R$)",
          min_value=0.0,
          value=50.0,
          step=5.0,
      )
      valor_total_frete = st.number_input(
          "Valor Total pago pelo Frete da Compra (R$)",
          min_value=0.0,
          value=100.0,
          step=10.0,
      )
      qtd_itens_frete = st.number_input(
          "Quantos itens/materiais vêm nesse mesmo frete?",
          min_value=1,
          value=20,
          step=1,
      )
    with col_b:
      custo_lote_embalagem = st.number_input(
          "Valor Total gasto no lote de Embalagens (R$)",
          min_value=0.0,
          value=50.0,
          step=5.0,
      )
      qtd_embalagens_lote = st.number_input(
          "Quantas embalagens vêm nesse lote?",
          min_value=1,
          value=50,
          step=1,
      )
      vendas_mensais = st.number_input(
          "Média de produtos vendidos por mês",
          min_value=1,
          value=100,
          step=5,
      )

    st.subheader("2. Contas de Consumo (Água e Energia)")
    col_c, col_d = st.columns(2)
    with col_c:
      valor_conta_luz = st.number_input(
          "Valor da Conta de Luz Mensal (R$)",
          min_value=0.0,
          value=300.0,
          step=10.0,
      )
      horas_luz_ligada = st.slider(
          "Quantas horas por dia os equipamentos/luz ficam ligados para o"
          " negócio?",
          min_value=1,
          max_value=24,
          value=8,
          step=1,
      )
    with col_d:
      valor_conta_agua = st.number_input(
          "Valor da Conta de Água Mensal (R$)",
          min_value=0.0,
          value=100.0,
          step=10.0,
      )
      dias_funcionamento = st.slider(
          "Quantos dias por mês a loja/operação funciona?",
          min_value=1,
          max_value=31,
          value=22,
          step=1,
      )

  # Cálculos Automáticos da Anamnese
  frete_unitario = (
      valor_total_frete / qtd_itens_frete if qtd_itens_frete > 0 else 0
  )
  embalagem_unitaria = (
      custo_lote_embalagem / qtd_embalagens_lote
      if qtd_embalagens_lote > 0
      else 0
  )
  custo_direto_total = custo_produto + frete_unitario + embalagem_unitaria

  # Rateio de Água e Luz proporcional ao tempo/dias de operação comercial vs total do mês (estimativa prática)
  # Consideramos um peso baseado nas horas diárias e dias do mês frente a 720h totais do mês (30 dias * 24h)
  fator_uso_energia = (horas_luz_ligada * dias_funcionamento) / 720
  total_utilidades = valor_conta_luz + valor_conta_agua
  utilidades_rateadas_mes = total_utilidades * min(
      fator_uso_energia, 1.0
  )  # Teto de 100%
  rateio_por_produto = (
      utilidades_rateadas_mes / vendas_mensais if vendas_mensais > 0 else 0
  )

  st.markdown("---")
  st.subheader("📊 Resumo dos Custos Calculados pela Anamnese")
  r1, r2, r3, r4 = st.columns(4)
  r1.metric("Frete por Produto", f"R$ {frete_unitario:.2f}")
  r2.metric("Embalagem por Produto", f"R$ {embalagem_unitaria:.2f}")
  r3.metric("Custo Direto Total", f"R$ {custo_direto_total:.2f}")
  r4.metric("Rateio Água/Luz por Item", f"R$ {rateio_por_produto:.2f}")

  st.markdown("---")
  st.subheader("⚙️ Parâmetros Fiscais e de Lucro")
  col_e, col_f = st.columns(2)
  with col_e:
    imposto_percentual = st.slider(
        "Impostos Estimados sobre a Venda (DAS / Nota) (%)",
        min_value=0,
        max_value=20,
        value=6,
        step=1,
    )
  with col_f:
    margem_lucro_desejada = st.slider(
        "Margem de Lucro Líquido Desejada (%)",
        min_value=1,
        max_value=80,
        value=30,
        step=1,
    )

  if st.button("Calcular Preço de Venda Ideal com Base no Diagnóstico"):
    custos_totais_com_rateio = custo_direto_total + rateio_por_produto
    divisor = 1 - ((imposto_percentual + margem_lucro_desejada) / 100)

    if divisor <= 0:
      st.error(
          "Erro: A soma dos impostos com a margem desejada atinge ou ultrapassa"
          " 100%!"
      )
    else:
      preco_venda = custos_totais_com_rateio / divisor
      val_imposto = preco_venda * (imposto_percentual / 100)
      lucro_liquido_reais = preco_venda * (margem_lucro_desejada / 100)

      st.success("Preço calculado com sucesso!")

      m1, m2, m3, m4 = st.columns(4)
      m1.metric("Preço de Venda Sugerido", f"R$ {preco_venda:.2f}")
      m2.metric(
          "Custos Totais (Direto + Fixo)", f"R$ {custos_totais_com_rateio:.2f}"
      )
      m3.metric("Valor do Imposto", f"R$ {val_imposto:.2f}")
      m4.metric(
          "Lucro Líquido no Bolso",
          f"R$ {lucro_liquido_reais:.2f}",
          delta=f"{margem_lucro_desejada}%",
      )

# -------------------------------------------------------------
# MÓDULO 2: SIMULADOR DE DESCONTOS
# -------------------------------------------------------------
elif menu == "2. Simulador de Descontos e Impacto":
  st.header("🏷️ Simulador de Desconto")
  col_a, col_b = st.columns(2)
  with col_a:
    preco_atual = st.number_input(
        "Preço de Venda Atual (R$)", min_value=0.0, value=200.0, step=10.0
    )
    custo_total_produto = st.number_input(
        "Custo Total Estimado do Produto (R$)",
        min_value=0.0,
        value=110.0,
        step=10.0,
    )
  with col_b:
    desconto_dado = st.slider(
        "Desconto Pretendido (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=1,
    )

  if st.button("Analisar Viabilidade"):
    novo_preco = preco_atual * (1 - (desconto_dado / 100))
    novo_lucro = novo_preco - custo_total_produto
    nova_margem = (
        (novo_lucro / novo_preco) * 100 if novo_preco > 0 else 0
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Novo Preço", f"R$ {novo_preco:.2f}")
    c2.metric("Novo Lucro Líquido", f"R$ {novo_lucro:.2f}")
    c3.metric("Nova Margem", f"{nova_margem:.1f}%")

    if novo_lucro <= 0:
      st.error("⚠️ Prejuízo: Você está pagando para trabalhar com esse desconto!")
    elif nova_margem < 15:
      st.warning("⚠️ Atenção: Margem muito espremida.")
    else:
      st.success("✅ Venda segura e com margem saudável.")

# -------------------------------------------------------------
# MÓDULO 3: GUIA CONTÁBIL DE CUSTOS FIXOS
# -------------------------------------------------------------
elif menu == "3. Guia Contábil: Água, Luz e Custos Fixos":
  st.header("💡 Guia Prático de Contabilidade para Pequenos Negócios")

  st.info(
      "Muitos empresários esquecem de embutir contas básicas no preço, achando"
      " que o lucro é apenas a diferença entre o que pagou no atacado e vendeu"
      " no varejo."
  )

  st.info(
      "A anamnese que criamos acima automatiza exatamente o que os contadores"
      " pedem: separar o custo de consumo operacional do custo direto do"
      " produto."
  )

  with st.expander(
      "1. Água e Luz entram no cálculo do produto ou serviço?"
  ):
    st.write(
        "Sim! Se você tem um ponto comercial (loja, escritório, salão),"
        " **Água e Luz são Despesas Fixas Operacionais**. Elas precisam ser"
        " somadas no final do mês e rateadas (divididas) pelo volume de"
        " produtos/serviços vendidos ou pelas horas trabalhadas."
    )

  with st.expander("2. E se eu trabalho em Home Office?"):
    st.write(
        "Para MEIs e MEs que operam de casa, misturar conta pessoal com da"
        " empresa é um erro grave. Deve-se calcular uma estimativa realista"
        " (por exemplo, 20% da conta de luz e internet correspondente ao"
        " cômodo/tempo dedicado ao negócio) e lançar como custo fixo da"
        " empresa."
    )

  with st.expander("3. Qual a diferença prática para o Contador?"):
    st.write(
        "Quando o empresário usa uma ferramenta que separa **Custos Variáveis**"
        " (matéria-prima) de **Custos Fixos** (aluguel, água, luz), ele entrega"
        " relatórios gerenciais muito mais limpos para a contabilidade oficial,"
        " facilitando a apuração de lucros isentos de imposto na distribuição"
        " para a Pessoa Física."
    )
  with st.expander("4. Por que calcular o rateio de água e luz por produto?"):
    st.write(
        "Porque se você paga R$ 300 de luz e R$ 100 de água, esse dinheiro sai"
        " da caixa da empresa todo mês. Se você não embutir uma fração disso no"
        " preço de cada produto vendido, o seu lucro líquido real evapora no"
        " pagamento das contas fixas."
    )
