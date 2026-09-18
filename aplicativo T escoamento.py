import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ajuste de Escoamento", layout="wide")

st.title("📈 Curva Tensão-Deformação com Ajuste Manual de Escoamento")
st.write("Utilize os controles abaixo para movimentar a reta de offset e encontrar a tensão de escoamento.")

# 1. Configurar os Sliders nativos do Streamlit
col1, col2 = st.columns(2)
with col1:
    offset = st.slider("Offset (%)", min_value=0.0, max_value=3.0, value=0.20, step=0.01)
with col2:
    declive = st.slider("Módulo de Elasticidade (Declive)", min_value=500.0, max_value=3000.0, value=1710.0, step=10.0)

# 2. Gerar dados simulados (Substitua pelos seus dados reais se necessário)
deformacao = np.linspace(0, 4.0, 500)
tensao = 1425 * np.tanh(1.2 * deformacao) 

# 3. Criar a Figura
fig, ax = plt.subplots(figsize=(10, 6))

# Curva principal
ax.plot(deformacao, tensao, 'b-', label='Curva de Tração', linewidth=2)

# Linha 1 (Elástica na origem)
x_lin = np.array([0, 1.5])
ax.plot(x_lin, declive * x_lin, 'k--', alpha=0.5, label='Região Elástica (Base)')

# Linha 2 (Offset Móvel)
x_off = np.array([offset, offset + 1.5])
ax.plot(x_off, declive * (x_off - offset), 'r--', alpha=0.7, label=f'Reta Offset ({offset:.2f}%)')

# 4. Calcular a intersecção automaticamente
y_reta = declive * (deformacao - offset)
diferenca = tensao - y_reta
cruzamentos = np.where(np.diff(np.sign(diferenca)))[0]

if len(cruzamentos) > 0:
    idx = cruzamentos[0]
    ax.plot(deformacao[idx], tensao[idx], 'yo', markersize=8, label=f'Escoamento: {tensao[idx]:.1f} N/mm²')
    st.success(f"**Tensão de Escoamento Encontrada:** {tensao[idx]:.1f} N/mm² (com {offset:.2f}% de deformação)")
else:
    st.warning("A reta de offset não cruza a curva com os parâmetros atuais.")

# 5. Formatar o Gráfico
ax.set_xlabel('Deformação (%)')
ax.set_ylabel('Tensão (N/mm²)')
ax.set_xlim(0, 4.5)
ax.set_ylim(0, 1600)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='lower right')

# 6. Exibir o gráfico no Streamlit
st.pyplot(fig)