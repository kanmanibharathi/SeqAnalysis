# SeqAnalysis: A Modern Bioinformatics Suite
**SeqAnalysis** is a high-performance, cross-platform application designed for comprehensive sequence analysis, including assembly, preprocessing, and extracting specific DNA/Protein sequences from large datasets. It features a modern, fluid GUI inspired by macOS and Windows 11 aesthetics.

![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Framework](https://img.shields.io/badge/Framework-PyQt6-emerald)

## 🚀 Key Features
*   **Modern UI**: Sleek dark-mode interface with emerald highlights, glassmorphism, and hardware acceleration.
*   **DNA Sequence Assembly**: Powered by an in-house **De Bruijn Graph Assembler** with path compaction, tip removal, and bubble popping.
*   **FASTQ Preprocessing**: Bulk extraction and quality filtering of sequencing reads with Phred score analysis and automated trimming.
*   **Sequence Classification**: Integrated nt/aa classification using native logic and NCBI BLAST (via R-Engine).
*   **Embedded Assets**: All fonts (Isidora) and icons are embedded directly into the binary for zero-dependency execution.
*   **Cross-Platform**: Native standalone builds for Windows, macOS, and Linux.

## 📥 Download (No Installation Required)
SeqAnalysis is available as a single, portable executable. You do not need to install Python or any dependencies.

1.  Go to the **Actions** (or Releases) page on GitHub.
2.  Download the specialized artifact for your operating system:
    *   **Windows**: `SeqAnalysis.exe`
    *   **macOS**: `SeqAnalysis-macos.zip` (Unzip to get `SeqAnalysis.app`)
    *   **Linux**: `SeqAnalysis-Linux` (Mark as executable: `chmod +x SeqAnalysis-Linux`)
    *   **R Engine**: `SeqAnalysis.R` (Run via RStudio for statistical analysis)
3.  **Run**: Just double-click the downloaded file (or run from terminal) to start.

## 🛠️ Cross-Platform Build Instructions
This project is optimized for automated packaging. No external dependencies are required for the final user.

### 1. 🪟 Windows
Generates a standalone `.exe` with embedded icon.
*   **Script**: `SeqAnalysis.spec`
*   **Command**: `pyinstaller --clean SeqAnalysis.spec`
*   **Output**: `dist/SeqAnalysis.exe`

### 2. 🍎 macOS
Generates a high-resolution `.app` bundle.
*   **Command**: `pyinstaller --clean SeqAnalysis.spec`
*   **Packaging**: `zip -r SeqAnalysis_Mac.zip dist/SeqAnalysis.app`
*   **Output**: `dist/SeqAnalysis_Mac.zip`

### 3. 🐧 Linux
Generates a standalone binary for Ubuntu/Debian/CentOS.
*   **Dependencies**: Requires `libxcb` and `PyQt6` build tools.
*   **Command**: `pyinstaller --clean SeqAnalysis.spec`
*   **Output**: `dist/SeqAnalysis`

## 🧬 Development Setup
To run the code from source:
1.  **Install Requirements**:
    ```bash
    pip install PyQt6 requests
    ```
2.  **Run Application**:
    ```bash
    python SeqAnalysis.py
    ```

## 📁 Project Structure
*   **`SeqAnalysis.py`**: The master source code (Logic + UI + Embedded Assets).
*   **`SeqAnalysis.R`**: The R-Shiny engine for advanced bioinformatics statistics.
*   **`SeqAnalysis.spec`**: Universal PyInstaller configuration for all platforms.
*   **`.github/workflows//`**: Multi-OS automated build pipeline (CI/CD).
*   **`requirements.txt`**: Python dependency manifest.

## ⚖️ License
This project is licensed under the **MIT License**. See the `LICENSE` file for details. Developed by **Dr. Kanmani Bharathi**.

---
*Support: support@oneresearchhub.in*
*Copyright © 2026 ONE RESEARCH HUB. ALL RIGHTS RESERVED*
