import os
import re
import json
import argparse
import threading
import requests
from graphviz import Digraph
import matplotlib.pyplot as plt

# Função para definir o caminho do Graphviz dinamicamente
def set_graphviz_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
    graphviz_path = os.path.join(current_dir, 'lib', 'Graphviz')  # Define o caminho para a pasta Graphviz
    os.environ['PATH'] += os.pathsep + graphviz_path  # Adiciona o caminho ao PATH do sistema


# Função para ler arquivo Lua com verificação dinâmica de codificação
def read_lua_file(file_path):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Não foi possível decodificar o arquivo {file_path} com as codificações tentadas.")

# Função para criar um fluxograma visualmente aprimorado a partir do código Lua
def parse_lua_to_flowchart(lua_code):
    graph = Digraph(comment='Fluxograma Lua')
    
    # Estilo global para o gráfico
    graph.attr(rankdir='TB', size='10,10')  # Layout de cima para baixo, tamanho adequado

    # Dividir o código em linhas
    lines = lua_code.splitlines()

    # Inicializar variáveis
    node_counter = 0
    stack = []
    
    def add_node(label, shape='box', color='black', style='filled', fillcolor='white'):
        nonlocal node_counter
        node_name = f'node{node_counter}'
        graph.node(node_name, label, shape=shape, color=color, style=style, fillcolor=fillcolor)
        node_counter += 1
        return node_name

    def add_edge(from_node, to_node):
        graph.edge(from_node, to_node)

    current_node = None
    
    # Expressões regulares para corresponder a estruturas de controle Lua
    patterns = {
        'if': r'^\s*if\s+(.*)\s+then\s*$',
        'else': r'^\s*else\s*$',
        'elseif': r'^\s*elseif\s+(.*)\s+then\s*$',
        'for': r'^\s*for\s+(.*)\s+do\s*$',
        'while': r'^\s*while\s+(.*)\s+do\s*$',
        'function': r'^\s*function\s+(.*)\s*$',
        'end': r'^\s*end\s*$',
    }
    
    # Definir esquemas de cores e formas para diferentes estruturas Lua
    node_styles = {
        'if': {'shape': 'diamond', 'color': 'blue', 'fillcolor': 'lightblue'},
        'else': {'shape': 'ellipse', 'color': 'orange', 'fillcolor': 'lightyellow'},
        'elseif': {'shape': 'diamond', 'color': 'blue', 'fillcolor': 'lightblue'},
        'for': {'shape': 'parallelogram', 'color': 'green', 'fillcolor': 'lightgreen'},
        'while': {'shape': 'parallelogram', 'color': 'green', 'fillcolor': 'lightgreen'},
        'function': {'shape': 'ellipse', 'color': 'purple', 'fillcolor': 'lavender'},
        'action': {'shape': 'box', 'color': 'black', 'fillcolor': 'white'}
    }
    
    for line in lines:
        line = line.strip()
        
        for key, pattern in patterns.items():
            match = re.match(pattern, line)
            if match:
                if key == 'if' or key == 'elseif':
                    condition = match.group(1)
                    style = node_styles[key]
                    node = add_node(f'{key.upper()} {condition}?', 
                                    shape=style['shape'], 
                                    color=style['color'], 
                                    fillcolor=style['fillcolor'])
                    if current_node:
                        add_edge(current_node, node)
                    stack.append(node)
                    current_node = node
                elif key == 'else':
                    style = node_styles['else']
                    node = add_node('ELSE', shape=style['shape'], color=style['color'], fillcolor=style['fillcolor'])
                    add_edge(current_node, node)
                    current_node = node
                elif key == 'for':
                    loop = match.group(1)
                    style = node_styles['for']
                    node = add_node(f'FOR {loop}', 
                                    shape=style['shape'], 
                                    color=style['color'], 
                                    fillcolor=style['fillcolor'])
                    if current_node:
                        add_edge(current_node, node)
                    stack.append(node)
                    current_node = node
                elif key == 'while':
                    condition = match.group(1)
                    style = node_styles['while']
                    node = add_node(f'WHILE {condition}', 
                                    shape=style['shape'], 
                                    color=style['color'], 
                                    fillcolor=style['fillcolor'])
                    if current_node:
                        add_edge(current_node, node)
                    stack.append(node)
                    current_node = node
                elif key == 'function':
                    func_name = match.group(1)
                    style = node_styles['function']
                    node = add_node(f'FUNCTION {func_name}', 
                                    shape=style['shape'], 
                                    color=style['color'], 
                                    fillcolor=style['fillcolor'])
                    if current_node:
                        add_edge(current_node, node)
                    stack.append(node)
                    current_node = node
                elif key == 'end':
                    if stack:
                        stack.pop()
                    if stack:
                        current_node = stack[-1]
                    else:
                        current_node = None
                break
        else:
            if current_node:
                # Padrão para linhas normais
                style = node_styles['action']
                action_node = add_node(line, shape=style['shape'], color=style['color'], fillcolor=style['fillcolor'])
                add_edge(current_node, action_node)
                current_node = action_node

    return graph

# Função para analisar o código Lua para insights
def analyze_lua_code(lua_code):
    analysis = {
        'if': 0,
        'elseif': 0,
        'else': 0,
        'for': 0,
        'while': 0,
        'function': 0,
        'total_lines': 0,
        'longest_function': {'name': '', 'lines': 0}
    }
    
    current_function = None
    function_line_count = 0
    
    # Dividir o código Lua em linhas
    lines = lua_code.splitlines()
    analysis['total_lines'] = len(lines)
    
    patterns = {
        'if': r'^\s*if\s+(.*)\s+then\s*$',
        'elseif': r'^\s*elseif\s+(.*)\s+then\s*$',
        'else': r'^\s*else\s*$',
        'for': r'^\s*for\s+(.*)\s+do\s*$',
        'while': r'^\s*while\s+(.*)\s+do\s*$',
        'function': r'^\s*function\s+([a-zA-Z0-9_]+)\s*\(.*\)\s*$',
        'end': r'^\s*end\s*$'  # Usado apenas para lidar com funções
    }
    
    for line in lines:
        line = line.strip()

        for key, pattern in patterns.items():
            match = re.match(pattern, line)
            if match:
                if key == 'function':
                    current_function = match.group(1)
                    function_line_count = 0
                elif key == 'end' and current_function:
                    # Lidar com o fim de um bloco de função
                    if function_line_count > analysis['longest_function']['lines']:
                        analysis['longest_function'] = {
                            'name': current_function,
                            'lines': function_line_count
                        }
                    current_function = None
                    function_line_count = 0
                elif key != 'end':  # Incrementar apenas para outras chaves, ignorar 'end'
                    analysis[key] += 1
                
        # Incrementar contagem de linhas para a função atual
        if current_function:
            function_line_count += 1

    return analysis

# Função para criar a legenda dos estilos de nó
def add_legend(graph):
    legend = Digraph('cluster_legend')  # Subgráfico para a legenda
    legend.attr(label='Legenda', color='black', fontsize='20')

    # Adicionar cada item à legenda: rótulo, forma, cor
    legend.node('if_legend', 'Condição IF/ELSEIF', shape='diamond', color='blue', style='filled', fillcolor='lightblue')
    legend.node('else_legend', 'Condição ELSE', shape='ellipse', color='orange', style='filled', fillcolor='lightyellow')
    legend.node('for_legend', 'Loop FOR', shape='parallelogram', color='green', style='filled', fillcolor='lightgreen')
    legend.node('while_legend', 'Loop WHILE', shape='parallelogram', color='green', style='filled', fillcolor='lightgreen')
    legend.node('function_legend', 'Definição de FUNÇÃO', shape='ellipse', color='purple', style='filled', fillcolor='lavender')
    legend.node('action_legend', 'Ação/Declaração', shape='box', color='black', style='filled', fillcolor='white')

    return legend

# Função para gerar um fluxograma com uma legenda
def generate_flowchart_with_legend(lua_code, output_path, dpi=300, size='15,15'):
    flowchart = Digraph(comment='Fluxograma Lua com Legenda')

    # Adicionar o subgráfico da legenda à esquerda
    legend = add_legend(flowchart)
    flowchart.subgraph(legend)

    # Gerar o fluxograma em si
    code_flowchart = parse_lua_to_flowchart(lua_code)
    
    # Mesclar o fluxograma e a legenda juntos
    for node in code_flowchart.body:
        flowchart.body.append(node)

    # Definir tamanho e DPI para qualidade aprimorada
    flowchart.attr(size=size)
    flowchart.render(output_path, format='svg', cleanup=True)
    
    return lua_code  # Retornar o lua_code para análise

# Função para gerar gráficos matplotlib para análise de código Lua e salvá-los como imagens
def generate_analysis_graphs(analysis, output_dir):
    # Garantir que o diretório de saída exista
    os.makedirs(output_dir, exist_ok=True)
    
    # Gráfico 1: Distribuição de tipos de nó (Gráfico de barras)
    labels = ['if', 'elseif', 'else', 'for', 'while', 'function']
    counts = [analysis[label] for label in labels]
    
    if any(counts):
        plt.figure(figsize=(10, 5))
        plt.bar(labels, counts, color=['blue', 'blue', 'orange', 'green', 'green', 'purple'])
        plt.title('Distribuição de Tipos de Nó')
        plt.ylabel('Contagem')
        plt.xlabel('Tipo de Nó')
        plt.savefig(os.path.join(output_dir, 'distribuicao_tipos_no.png'))
        plt.close()

    # Gráfico 2: Condições vs Loops (Gráfico de pizza)
    condition_count = analysis['if'] + analysis['elseif'] + analysis['else']
    loop_count = analysis['for'] + analysis['while']
    
    if condition_count + loop_count > 0:
        plt.figure(figsize=(7, 7))
        plt.pie([condition_count, loop_count], labels=['Condições', 'Loops'], colors=['lightblue', 'lightgreen'], autopct='%1.1f%%')
        plt.title('Condições vs Loops')
        plt.savefig(os.path.join(output_dir, 'condicoes_vs_loops.png'))
        plt.close()

    # Gráfico 3: Informações fora da caixa (Função mais longa e total de linhas)
    if analysis['total_lines'] > 0 or analysis['longest_function']['lines'] > 0:
        plt.figure(figsize=(5, 5))
        plt.bar(['Total de Linhas', 'Função Mais Longa'], [analysis['total_lines'], analysis['longest_function']['lines']], color=['gray', 'purple'])
        plt.title('Análise de Código: Linhas e Funções')

        # Anotar o nome da função mais longa
        longest_func_name = analysis['longest_function']['name']
        plt.text(1, analysis['longest_function']['lines'] + 10, f'Função Mais Longa: {longest_func_name}', ha='center', color='purple')

        plt.ylabel('Número de Linhas')
        plt.savefig(os.path.join(output_dir, 'analise_codigo_linhas_funcoes.png'))
        plt.close()

def get_path_for_file(dir, file, abs_path=False):
    if abs_path:
        return os.path.abspath(dir)
    
    return os.path.join(dir, file)

def generate_report(lua_code, output_path, index, total_files, relative_path, file):
    prompt = f"Analise o seguinte código Lua e identifique possíveis erros de performance ou oportunidades de refatoração. Por favor, forneça um relatório detalhado em português (PT-BR):\n\n{lua_code}"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'llama3.1:latest',
        'prompt': prompt,
        'gpu': True
    }
    response = requests.post('http://localhost:11434/api/generate', headers=headers, json=data)
    response.raise_for_status()
    
    try:
        # Accumulate the response chunks
        response_text = response.content.decode('utf-8')
        response_lines = response_text.splitlines()
        
        # Parse each line as a separate JSON object
        json_responses = [json.loads(line) for line in response_lines if line.strip()]
        
        # Extract the 'response' field from each JSON object
        report = ''.join([item['response'] for item in json_responses])
    except (ValueError, KeyError) as e:
        print(f"Erro ao decodificar JSON para o arquivo {file}: {e}")
        print(f"Resposta bruta do servidor: {response.content.decode('utf-8')}")
        return
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(report)
    
    print(f'\r[{index}/{total_files}] Relatório gerado para pasta: {relative_path} nome: {file}', end='')

# Função para processar todos os arquivos .lua em um diretório recursivamente
def process_lua_files_in_directory(input_dir, output_base_dir, skip_fxmanifest):
    lua_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.lua') and not (skip_fxmanifest and file == 'fxmanifest.lua'):
                lua_files.append((root, file))
    
    total_files = len(lua_files)
    for index, (root, file) in enumerate(lua_files, start=1):
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(root, input_dir)
        output_dir = os.path.join(output_base_dir, relative_path)
        flowchart_dir = os.path.join(output_dir, 'fluxograma')
        analysis_dir = os.path.join(output_dir, 'analise_grafica')
        report_dir = os.path.join(output_dir, 'relatorios')  # New directory for reports
        os.makedirs(flowchart_dir, exist_ok=True)
        os.makedirs(analysis_dir, exist_ok=True)
        os.makedirs(report_dir, exist_ok=True)  # Ensure the report directory exists
        
        output_file_path = os.path.join(flowchart_dir, file)
        report_file_path = os.path.join(report_dir, f'{os.path.splitext(file)[0]}_relatorio.txt')  # Save reports in the new directory
        
        lua_code = read_lua_file(file_path)
        generate_flowchart_with_legend(lua_code, output_file_path, dpi=300, size='15,15')
        
        analysis = analyze_lua_code(lua_code)
        generate_analysis_graphs(analysis, analysis_dir)
        
        # Gerar relatório em uma thread separada
        report_thread = threading.Thread(target=generate_report, args=(lua_code, report_file_path, index, total_files, relative_path, file))
        report_thread.start()
        
        print(f'\r[{index}/{total_files}] pasta: {relative_path} nome: {file}', end='')

    print()  # Para mover para a próxima linha após o loop

# Função principal para analisar argumentos e executar o script
def main():
    parser = argparse.ArgumentParser(description='Processar arquivos Lua para gerar fluxogramas e gráficos de análise.')
    parser.add_argument('--input', required=True, help='Diretório de entrada contendo arquivos Lua')
    parser.add_argument('--output', default='./', help='Diretório base de saída para salvar os resultados')
    parser.add_argument('--skip', action='store_true', help='Pular arquivos fxmanifest.lua')
    
    args = parser.parse_args()
    
    input_directory = args.input
    output_base_directory = args.output
    skip_fxmanifest = args.skip
    
    set_graphviz_path()
    process_lua_files_in_directory(input_directory, output_base_directory, skip_fxmanifest)

if __name__ == '__main__':
    main()