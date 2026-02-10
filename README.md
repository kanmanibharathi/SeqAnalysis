# NSeqVerify
**A Modern, High-Performance Sequence Analysis & Verification Suite**

**NSeqVerify** is a cross-platform bioinformatics utility designed for streamlined sequence processing and verification. By blending the high-performance logic of **Python (PyQt6)** with the specialized analysis capabilities of **R (Shiny)**, NSeqVerify provides a comprehensive environment for both rapid data exploration and complex assembly workflows.

## 🚀 Key Features

### 1. Dual-Engine Analysis
*   **Python Power**: A sleek, hardware-accelerated GUI built with PyQt6 for intense tasks like De Bruijn Graph assembly and local FASTQ preprocessing.
*   **R Integration**: Embedded R Shiny logic for sophisticated bioinformatics visualizations and statistical sequence metrics.

### 2. Advanced Assembler & Logic
*   **In-House De Bruijn Graph**: Custom implementation for sequence assembly, including path compaction, tip removal, and bubble popping for high-fidelity consensus sequences.
*   **Sequence Verification**: Real-time validation of nucleotide data, including reverse complementation, GC content analysis, and quality score aggregation.

### 3. FASTQ Preprocessing
*   High-speed parsing and filtering of raw sequencing data.
*   Automated quality control and trimming workflows optimized for large-scale datasets.

### 4. Zero-Dependency Portability (Build Ready)
*   **Asset Embedding**: High-fidelity fonts (Isidora) and icons are embedded directly into the source as Base64 data, ensuring a "Single-File" experience without broken paths or missing assets.
*   **Cross-Platform**: Ready for distribution as executable binaries (`.exe`, `.app`, and Linux) using PyInstaller.

## 🛠️ Technology Stack
*   **Frontend**: PyQt6 (Python), R Shiny
*   **Logic**: Python 3.10+ (Collections, Concurrent Futures, De Bruijn Graph)
*   **Visualization**: R (bslib, httr, shiny)
*   **Build Pipeline**: PyInstaller

## 📦 File Structure
*   **`SeqAnalysis.py`**: The core application entry point and GUI logic.
*   **`SeqAnalysis.R`**: The bioinformatics analysis engine.
*   **`SeqAnalysis.spec`**: Optimized PyInstaller build configuration for local executables.
*   **`requirements.txt`**: Minimalist dependency manifest.

---

### How to Build
To generate a standalone executable for your OS:
```bash
pip install -r requirements.txt
pyinstaller SeqAnalysis.spec
```
