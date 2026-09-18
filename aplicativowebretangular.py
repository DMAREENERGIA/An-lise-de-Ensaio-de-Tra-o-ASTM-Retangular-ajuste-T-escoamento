import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Gerar dados simulados (semelhantes à curva do ficheiro 1_2.jpg)
# Num cenário real, deverá substituir 'deformacao' e 'tensao' pelos seus próprios arrays de dados (ex: lidos de um CSV)
deformacao = np.linspace(0, 4.0, 500)
# Fórmula aproximada para gerar uma curva com comportamento semelhante
tensao = 1425 * np.tanh(1.2 * deformacao) 

# Parâmetros Iniciais
declive_inicial = 1710.0  # Módulo de elasticidade inicial (declive)
offset_inicial = 0.2      # Valor de offset inicial em % (o utilizador pediu 2%, ajustável no slider)

# 2. Configurar a figura e reservar espaço inferior para os controlos manuais
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.3)

# Desenhar a curva principal
ax.plot(deformacao, tensao, 'b-', label='Curva de Tração', linewidth=2)

# 3. Criar as duas linhas pontilhadas (inicialmente vazias ou com valores base)
# Linha 1: Relação linear a partir da origem
linha_elastica, = ax.plot([], [], 'k--', alpha=0.5, label='Região Elástica (Base)')

# Linha 2: Reta de Offset (Móvel)
linha_offset, = ax.plot([], [], 'r--', alpha=0.7, label=f'Reta Offset ({offset_inicial}%)')

# Ponto para marcar a Tensão de Escoamento (intersecção)
ponto_escoamento, = ax.plot([], [], 'yo', markersize=7, label='Escoamento')

ax.set_title('Curva Tensão-Deformação interativa com Ajuste de Escoamento')
ax.set_xlabel('Deformação (%)')
ax.set_ylabel('Tensão (N/mm²)')
ax.set_xlim(0, 4.5)
ax.set_ylim(0, 1600)
ax.grid(True, linestyle=':', alpha=0.7)
legenda = ax.legend(loc='lower right')

# 4. Criar eixos para os Sliders
ax_declive = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_offset = plt.axes([0.15, 0.10, 0.65, 0.03])

# Inicializar os Sliders (Declive e Percentagem de Offset)
slider_declive = Slider(ax_declive, 'Módulo (Declive)', 500.0, 3000.0, valinit=declive_inicial)
slider_offset = Slider(ax_offset, 'Offset (%)', 0.0, 3.0, valinit=offset_inicial, valstep=0.01)

# 5. Função de atualização interativa
def atualizar(val):
    declive = slider_declive.val
    offset = slider_offset.val
    
    # Atualizar Linha 1 (Elástica na origem)
    x_lin = np.array([0, 1.5])
    linha_elastica.set_data(x_lin, declive * x_lin)
    
    # Atualizar Linha 2 (Offset Móvel)
    x_off = np.array([offset, offset + 1.5])
    linha_offset.set_data(x_off, declive * (x_off - offset))
    linha_offset.set_label(f'Reta Offset ({offset:.2f}%)')
    
    # Calcular automaticamente a intersecção para encontrar a Tensão de Escoamento
    # Equação da reta de offset em todo o domínio X
    y_reta = declive * (deformacao - offset)
    
    # Encontrar onde a curva real cruza a reta de offset
    diferenca = tensao - y_reta
    cruzamentos = np.where(np.diff(np.sign(diferenca)))[0]
    
    if len(cruzamentos) > 0:
        idx = cruzamentos[0] # Primeiro ponto de cruzamento
        ponto_escoamento.set_data([deformacao[idx]], [tensao[idx]])
        ponto_escoamento.set_label(f'Escoamento: {tensao[idx]:.1f} N/mm²')
    else:
        # Se a reta não cruzar a curva (ex: offset demasiado alto), ocultar o ponto
        ponto_escoamento.set_data([], [])
        ponto_escoamento.set_label('Escoamento: Fora da curva')
    
    # Atualizar a legenda para refletir os novos valores
    ax.legend(loc='lower right')
    fig.canvas.draw_idle()

# Invocar a função de atualização para o estado inicial
atualizar(0)

# Ligar os sliders à função de atualização
slider_declive.on_changed(atualizar)
slider_offset.on_changed(atualizar)

# Mostrar a janela interativa
plt.show()