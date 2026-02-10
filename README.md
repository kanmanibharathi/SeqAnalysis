# NSeqVerify: A Modern Bioinformatics Suite

**NSeqVerify** is a professional-grade, cross-platform bioinformatics application designed for comprehensive sequence analysis, assembly, and classification. It integrates high-performance Python logic with the statistical power of R Shiny to provide a seamless user experience.

## 🚀 Key Modules & Functionalities

### 🧬 DNA Sequence Assembly
NSeqVerify features a powerful, in-house **De Bruijn Graph Assembler** capable of handling complex genomic data.
- **Multi-Kmer Analysis**: Iterative assembly across multiple k-mer sizes for higher consensus accuracy.
- **Graph Simplification**: Advanced algorithms for:
    - **Path Compaction**: Merging linear nodes.
    - **Tip Removal**: Pruning short, erroneous branches.
    - **Bubble Popping**: Resolving heterozygous or sequencing error-induced deviations.
- **Scalable Processing**: Multi-threaded graph construction for memory efficiency.

### 🧪 FASTQ Preprocessing
Streamline your raw NGS data before downstream analysis.
- **Quality Filtering**: Integrated Phred score analysis to filter low-quality reads.
- **Read Trimming**: Precision trimming of adapters or low-quality ends.
- **Subsampling**: Analyze a subset of your data for rapid verification.
- **Directional Correction**: Optional automated reverse-complementing of reads.

### 📊 Sequence Classification
Rapidly identify pathogens or organismal data in your samples.
- **NSeq-Classifier (nt/aa)**: Native implementation for classifying nucleotide and protein sequences.
- **NCBI BLAST Integration**: (R-Engine) Built-in support for establishing connections to NCBI for remote sample identification.

### 🎨 Modern single-window GUI
- **Hardware Accelerated**: Built with PyQt6 for a fluid, responsive interface.
- **Integrated System Logs**: Real-time console tracking within the app for every computation.
- **Visual Assets**: Fully embedded Isidora High-Fidelity typography and pixel-perfect icons.
- **Theme Engine**: Automated dark-mode optimization for reduced eye strain during long analysis sessions.

## 🛠️ Technical Details

| Feature | Specification |
| :--- | :--- |
| **Development** | Dr. Kanmani Bharathi |
| **Language** | Python 3.10+, R 4.x |
| **UI Framework** | PyQt6, R Shiny (bslib) |
| **Core Logic** | Concurrent Futures, De Bruijn Graph (Pure Python Implementation) |
| **Portability** | Single-file executable (Base64 asset embedding) |

## 📦 File Architecture
- `SeqAnalysis.py`: The Main Python application containing the PyQt6 GUI and Assembler/Preprocessor logic.
- `SeqAnalysis.R`: The R-Shiny bioinformatics analyzer for statistics and visualization.
- `SeqAnalysis.spec`: PyInstaller configuration optimized for Windows artifacts.
- `requirements.txt`: Python package requirements.
- `icon.ico`: High-Resolution application identification.

---

## 🏗️ Building From Source
To generate the standalone executable:
1. Ensure Python 3.10+ is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Bundle the app: `pyinstaller SeqAnalysis.spec`
4. Find your executable in the `/dist` folder.

---

### Developed by **One Research Hub**
*Support: support@oneresearchhub.in*
*Copyright © 2026 ONE RESEARCH HUB. ALL RIGHTS RESERVED*
