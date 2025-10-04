# LuaFlowChart

A comprehensive Python application for analyzing Lua code and generating visual flowcharts, statistical analysis graphs, and AI-powered code reports with support for multiple encoding formats and batch processing.

## Project Description

LuaFlowChart is a powerful code analysis tool specifically designed for Lua programming language. It automatically processes Lua files to create visual flowcharts, generate statistical analysis graphs, and produce detailed AI-powered code reports. The application is particularly useful for developers working with FiveM, Roblox, or other Lua-based platforms who need to understand code structure and identify potential improvements.

### Key Features

- **Visual Flowcharts**: Generate professional flowcharts from Lua code with color-coded elements
- **Statistical Analysis**: Create comprehensive graphs showing code structure metrics
- **AI-Powered Reports**: Generate detailed code analysis reports using local AI models
- **Batch Processing**: Process entire directories of Lua files recursively
- **Multiple Encodings**: Support for UTF-8, Latin-1, and CP1252 file encodings
- **FiveM Support**: Special handling for fxmanifest.lua files
- **High-Quality Output**: SVG flowcharts with customizable DPI and size settings
- **Progress Tracking**: Real-time progress indicators for batch operations

## Installation Instructions

### Prerequisites

- Python 3.7 or higher
- Graphviz installed on your system
- Local AI model server (Ollama recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/York-Lucis/lua-to-flowchart.git
   cd lua-to-flowchart
   ```

2. **Install Graphviz**:
   - **Windows**: Download from [Graphviz website](https://graphviz.org/download/)
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz`

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up AI model server** (optional):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model (e.g., Llama 3.1)
   ollama pull llama3.1:latest
   ```

### Dependencies

- `graphviz` - Graph visualization library
- `matplotlib` - Statistical graph generation
- `requests` - HTTP requests for AI model communication

## Usage Guide

### Basic Usage

#### Process a single directory:
```bash
python main.py --input /path/to/lua/files --output /path/to/output
```

#### Skip fxmanifest.lua files:
```bash
python main.py --input /path/to/lua/files --output /path/to/output --skip
```

### Command Line Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `--input` | Directory containing Lua files to process | Yes |
| `--output` | Base output directory for results | No (defaults to current directory) |
| `--skip` | Skip fxmanifest.lua files | No |

### Output Structure

The application creates a comprehensive output structure:

```
output_directory/
├── relative_path_1/
│   ├── fluxograma/
│   │   └── file1.lua.svg
│   ├── analise_grafica/
│   │   ├── distribuicao_tipos_no.png
│   │   ├── condicoes_vs_loops.png
│   │   └── analise_codigo_linhas_funcoes.png
│   └── relatorios/
│       └── file1_relatorio.txt
└── relative_path_2/
    └── ...
```

### Output Types

#### 1. Flowcharts (SVG)
- **Color-coded elements**: Different colors for conditions, loops, functions, and actions
- **High resolution**: 300 DPI by default, customizable
- **Interactive**: SVG format allows zooming and detailed inspection
- **Legend included**: Visual guide to element types

#### 2. Statistical Graphs (PNG)
- **Distribution of Node Types**: Bar chart showing count of different code structures
- **Conditions vs Loops**: Pie chart comparing conditional and loop structures
- **Code Analysis**: Bar chart showing total lines and longest function metrics

#### 3. AI Reports (TXT)
- **Performance Analysis**: Identifies potential performance issues
- **Refactoring Suggestions**: Recommendations for code improvement
- **Best Practices**: Lua-specific coding recommendations
- **Detailed Insights**: Comprehensive analysis of code structure

## Technical Details

### Supported Lua Structures

The application recognizes and visualizes:

- **Conditional Statements**: `if`, `elseif`, `else`
- **Loops**: `for`, `while`
- **Functions**: `function` definitions
- **Actions**: Regular code statements

### Color Coding System

| Element Type | Color | Shape |
|--------------|-------|-------|
| IF/ELSEIF | Blue | Diamond |
| ELSE | Orange | Ellipse |
| FOR/WHILE | Green | Parallelogram |
| FUNCTION | Purple | Ellipse |
| ACTION | Black | Rectangle |

### AI Integration

The application integrates with local AI models through HTTP API:

- **Model**: Configurable (default: llama3.1:latest)
- **Server**: Local Ollama instance (http://localhost:11434)
- **Analysis**: Performance optimization and refactoring suggestions
- **Language**: Reports generated in Portuguese (PT-BR)

### Encoding Support

Automatic detection and handling of multiple file encodings:
- UTF-8 (primary)
- Latin-1 (fallback)
- CP1252 (Windows fallback)

## Advanced Features

### Batch Processing

Process entire project directories with progress tracking:
- Recursive directory traversal
- Progress indicators for large projects
- Error handling for individual files
- Resume capability for interrupted operations

### Customization Options

#### Flowchart Settings
```python
# Modify in the code for custom settings
dpi=300  # Resolution (default: 300)
size='15,15'  # Output size (default: 15x15)
```

#### AI Model Configuration
```python
# Change AI model in generate_report function
'model': 'llama3.1:latest'  # or other available models
```

### Performance Optimization

- **Parallel Processing**: AI reports generated in separate threads
- **Memory Management**: Efficient handling of large codebases
- **Caching**: Graphviz path optimization for faster execution

## Development

### Architecture

The application follows a modular design:

1. **File Processing Module**: Handles file reading and encoding detection
2. **Flowchart Generation Module**: Creates visual representations
3. **Analysis Module**: Generates statistical insights
4. **AI Integration Module**: Produces intelligent reports
5. **Batch Processing Module**: Manages large-scale operations

### Key Functions

- **`read_lua_file()`**: Multi-encoding file reading
- **`parse_lua_to_flowchart()`**: Flowchart generation with regex parsing
- **`analyze_lua_code()`**: Statistical analysis of code structure
- **`generate_analysis_graphs()`**: Matplotlib graph generation
- **`generate_report()`**: AI-powered code analysis

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various Lua codebases
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Graphviz not found**: Ensure Graphviz is installed and in PATH
2. **AI reports not generating**: Check if Ollama server is running
3. **Encoding errors**: The application handles multiple encodings automatically
4. **Memory issues**: For very large codebases, process in smaller batches

### Performance Tips

- Use `--skip` flag for FiveM projects to exclude fxmanifest.lua
- Process large projects in smaller directory chunks
- Ensure adequate disk space for output files
- Close other applications during batch processing

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/York-Lucis/lua-to-flowchart) or create an issue.

---

**Author**: [York-Lucis](https://github.com/York-Lucis)  
**Repository**: [lua-to-flowchart](https://github.com/York-Lucis/lua-to-flowchart)