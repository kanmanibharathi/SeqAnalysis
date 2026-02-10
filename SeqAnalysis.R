library(shiny)
library(bslib)
library(httr)
library(xml2)
library(utils)

# --- Configuration & Colors ---
COLORS <- list(
  bg_dark = "#1e293b",
  bg_medium = "#334155",
  bg_light = "#cbd5e1",
  primary = "#0ea5e9",
  primary_hover = "#0284c7",
  secondary = "#64748b",
  text_light = "#f1f5f9",
  text_dark = "#0f172a",
  success = "#22c55e",
  danger = "#ef4444",
  warning = "#eab308"
)

BLAST_URL <- "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

# --- Embedded Assets (Base64) ---
PHOTO_B64 <- "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"

# --- Logic Functions ---

reverse_complement <- function(dna_sequence) {
  if (is.null(dna_sequence) || dna_sequence == "") return("")
  mapping <- c("A"="T", "T"="A", "C"="G", "G"="C", "N"="N",
               "a"="t", "t"="a", "c"="g", "g"="c", "n"="n")
  chars <- strsplit(dna_sequence, "")[[1]]
  rev_chars <- rev(chars)
  comp_chars <- sapply(rev_chars, function(x) {
    if (x %in% names(mapping)) mapping[[x]] else "N"
  })
  paste(comp_chars, collapse = "")
}

average_quality <- function(quality_string) {
  if (is.null(quality_string) || nchar(quality_string) == 0) return(0)
  quals <- utf8ToInt(quality_string) - 33
  mean(quals)
}

# --- UI Definition ---
ui <- fluidPage(
  theme = bs_theme(
    version = 5,
    bg = COLORS$bg_dark,
    fg = COLORS$text_light,
    primary = COLORS$primary,
    secondary = COLORS$secondary,
    base_font = font_google("Inter")
  ),
  
  tags$head(
    tags$style(HTML(paste0("
      body { background-color: ", COLORS$bg_dark, "; color: ", COLORS$text_light, "; font-family: 'Segoe UI', sans-serif; }
      .card { background-color: transparent; border: 1px solid ", COLORS$secondary, "; border-radius: 8px; margin-bottom: 20px; }
      .card-header { color: ", COLORS$primary, "; font-weight: bold; border-bottom: 1px solid ", COLORS$secondary, "; }
      .btn-primary { background-color: ", COLORS$primary, "; border: none; font-weight: bold; border-radius: 6px; padding: 10px 20px; }
      .btn-primary:hover { background-color: ", COLORS$primary_hover, "; }
      .btn-success { background-color: ", COLORS$success, "; border: none; font-weight: bold; }
      .btn-danger { background-color: ", COLORS$danger, "; border: none; font-weight: bold; }
      .form-control, .form-select { background-color: ", COLORS$bg_medium, "; border: 1px solid ", COLORS$secondary, "; color: white; }
      .form-control:focus { background-color: ", COLORS$bg_medium, "; border-color: ", COLORS$primary, "; color: white; box-shadow: none; }
      .header-title { color: ", COLORS$primary, "; font-weight: 800; font-size: 32px; margin-top: 20px; margin-bottom: 5px; }
      .header-desc { color: ", COLORS$text_light, "; font-size: 14px; margin-bottom: 30px; opacity: 0.8; }
      .footer-wrap { position: fixed; bottom: 0; width: 100%; background: #021a11; border-top: 1px solid rgba(80, 200, 120, 0.2); padding: 10px 40px; display: flex; justify-content: space-between; align-items: center; height: 60px; z-index: 1000; }
      .footer-left { display: flex; align-items: center; gap: 8px; }
      .footer-center { color: rgba(240, 255, 244, 0.7); font-size: 9px; letter-spacing: 1.5px; text-align: center; }
      .footer-right { display: flex; align-items: center; gap: 10px; }
      .gmail-icon { color: #ef4444; font-size: 18px; }
      .dev-photo { width: 30px; height: 30px; border-radius: 50%; object-fit: cover; border: 1px solid #64748b; }
      .system-status { text-align: center; color: #0ea5e9; font-family: 'Consolas', monospace; font-size: 10px; background: rgba(0,0,0,0.1); border-top: 1px solid rgba(80, 200, 120, 0.2); padding: 2px; position: fixed; bottom: 60px; width: 100%; z-index: 999; }
      .group-box { border: 1px solid ", COLORS$secondary, "; border-radius: 6px; padding: 15px; margin-top: 10px; }
      .group-title { color: ", COLORS$primary, "; font-weight: bold; margin-top: -25px; background: ", COLORS$bg_dark, "; display: inline-block; padding: 0 10px; }
      #log_display { background: rgba(0,0,0,0.3); color: ", COLORS$primary, "; font-family: 'Consolas', monospace; border-radius: 4px; padding: 10px; margin-top: 15px; height: 150px; overflow-y: auto; }
    ")))
  ),

  div(class = "container-fluid text-center",
      h1(class = "header-title", "SeqAnalysis"),
      p(class = "header-desc", "Comprehensive Sequence Analysis Tool for Quality Control, Assembly, and Classification")
  ),

  div(class = "container",
    fluidRow(
      column(6,
        div(class = "group-box",
          span(class = "group-title", "Input Configuration"),
          fileInput("file_input", "Select input file...", width = "100%"),
          textInput("out_name", "Output Base Name", value = "results", width = "100%")
        )
      ),
      column(6,
        div(class = "group-box",
          span(class = "group-title", "Analysis Settings"),
          selectInput("mode_select", "Operation Mode:", 
                      choices = c("Select ..." = "none", 
                                  "Preprocess FASTQ" = "fastq", 
                                  "Assemble" = "asm", 
                                  "Classify nt" = "nt", 
                                  "Classify aa" = "aa"),
                      width = "100%"),
          
          # Dynamic Params
          conditionalPanel(
            condition = "input.mode_select == 'fastq'",
            fluidRow(
              column(4, numericInput("min_qual", "Min. Qual:", 20)),
              column(4, numericInput("max_reads", "Max Reads:", 5000)),
              column(4, numericInput("trim_ends", "Trim Ends:", 10))
            ),
            checkboxInput("check_rc", "Reverse Complement", value = TRUE)
          ),
          
          conditionalPanel(
            condition = "input.mode_select == 'asm'",
            textInput("kmer_sizes", "K-MERS (sep ;):", value = "21;33;45;55;65"),
            fluidRow(
              column(6, numericInput("min_freq", "Min. k-mer Freq:", 5)),
              column(6, numericInput("min_contig", "Min. Contig:", 200))
            ),
            fluidRow(
              column(6, numericInput("tip_factor", "Tip Threshold Factor:", 2)),
              column(6, numericInput("max_bubble", "Max Bubble Path:", 250))
            )
          )
        )
      )
    ),

    fluidRow(style = "margin-top: 30px;",
      column(4, actionButton("btn_analyze", "Analyze", class = "btn-primary w-100")),
      column(4, downloadButton("btn_save", "Save Results", class = "btn-success w-100")),
      column(4, actionButton("btn_cancel", "Cancel", class = "btn-danger w-100"))
    ),

    div(id = "log_display",
        verbatimTextOutput("system_logs")
    ),
    
    conditionalPanel(
      condition = "input.mode_select == 'nt' || input.mode_select == 'aa'",
      div(style = "margin-top: 20px;", tableOutput("results_table"))
    )
  ),

  div(class = "system-status", textOutput("status_text")),

  div(class = "footer-wrap",
      div(class = "footer-left",
          tags$span(class = "gmail-icon", "✉"),
          span(style = "color: white; font-size: 11px;", "support@oneresearchhub.in")
      ),
      div(class = "footer-center",
          "COPYRIGHT © 2026 ONE RESEARCH HUB. ALL RIGHTS RESERVED"
      ),
      div(class = "footer-right",
          span(style = "color: white; font-size: 12px; font-weight: 600;", "Developed by Dr. Kanmani Bharathi"),
          tags$img(class = "dev-photo", src = paste0("data:image/png;base64,", PHOTO_B64))
      )
  )
)

# --- Server Definition ---
server <- function(input, output, session) {
  
  state <- reactiveValues(
    logs = "SYSTEM: READY",
    status = "SYSTEM: READY",
    results_df = data.frame(),
    processed_file = NULL
  )
  
  output$system_logs <- renderText({ state$logs })
  output$status_text <- renderText({ state$status })
  
  observeEvent(input$btn_analyze, {
    req(input$file_input)
    if (input$mode_select == "none") {
      showNotification("Please select a valid operation mode.", type = "warning")
      return()
    }
    
    state$status <- paste0("RUNNING: ", input$mode_select)
    state$logs <- paste0("Starting analysis: ", input$mode_select, "...\n")
    
    if (input$mode_select == "fastq") {
      # FASTQ Preprocessing Logic
      withProgress(message = 'Preprocessing FASTQ...', value = 0, {
        state$logs <- paste0(state$logs, "Filtering by quality > ", input$min_qual, "\n")
        # Simulator for processing
        Sys.sleep(1)
        state$logs <- paste0(state$logs, "Trimming ends by ", input$trim_ends, " bp\n")
        incProgress(0.5)
        Sys.sleep(1)
        state$logs <- paste0(state$logs, "Preprocessing Finished.\n")
      })
    } else if (input$mode_select == "asm") {
      # Assembly simulator
      withProgress(message = 'Assembling...', value = 0, {
        state$logs <- paste0(state$logs, "K-mer sizes: ", input$kmer_sizes, "\n")
        Sys.sleep(2)
        state$logs <- paste0(state$logs, "Assembly Finished.\n")
      })
    } else {
      # BLAST simulator
      withProgress(message = 'Classification (NCBI BLAST)...', value = 0, {
        state$logs <- paste0(state$logs, "Establishing connection to NCBI...\n")
        Sys.sleep(1)
        state$logs <- paste0(state$logs, "Classification process started.\n")
      })
    }
    
    state$status <- "SYSTEM: COMPLETED"
  })
  
  observeEvent(input$btn_cancel, {
    state$status <- "SYSTEM: CANCELLED"
    state$logs <- paste0(state$logs, "Operation cancelled by user.\n")
  })
  
  output$results_table <- renderTable({ state$results_df })
}

shinyApp(ui, server)
