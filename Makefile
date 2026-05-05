EXTERNAL_DIR=$(CURDIR)/external
BUILD_DIR=$(CURDIR)/build
REPORT_DIR=$(CURDIR)/reports
VENV_DIR=$(CURDIR)/venv

ANTLR_VERSION=4.13.2
ANTLR_JAR=antlr-$(ANTLR_VERSION)-complete.jar
ANTLR_URL=https://www.antlr.org/download/$(ANTLR_JAR)

PYTHON_VERSION=3.12

GRAMMAR_FILES=$(wildcard src/grammar/*.g4)

# Python executable paths
PYTHON_CANDIDATES=python$(PYTHON_VERSION) /usr/bin/python$(PYTHON_VERSION) /usr/local/bin/python$(PYTHON_VERSION) /opt/homebrew/bin/python$(PYTHON_VERSION)
VENV_PYTHON=$(VENV_DIR)/bin/python
VENV_PIP=$(VENV_DIR)/bin/pip

# Check if we're on Windows
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    VENV_PYTHON=$(VENV_DIR)/Scripts/python.exe
    VENV_PIP=$(VENV_DIR)/Scripts/pip.exe
    PYTHON_CANDIDATES=python$(PYTHON_VERSION) python py -$(PYTHON_VERSION)
    # Windows specific settings
    RM_CMD=if exist "$1" rmdir /s /q "$1"
    RMFILE_CMD=if exist "$1" del /f /q "$1"
    MKDIR_CMD=if not exist "$1" mkdir "$1"
    COPY_CMD=xcopy /y /e "$1" "$2"
    SEP=\\
    # Use powershell to download ANTLR
    DOWNLOAD_CMD=powershell -Command "Invoke-WebRequest -Uri $(ANTLR_URL) -OutFile $(EXTERNAL_DIR)/$(ANTLR_JAR)"
    # No colors on Windows CMD by default
    RED=
    GREEN=
    YELLOW=
    BLUE=
    RESET=
else
    DETECTED_OS := $(shell uname -s)
    VENV_PYTHON=$(VENV_DIR)/bin/python
    VENV_PIP=$(VENV_DIR)/bin/pip
    PYTHON_CANDIDATES=python$(PYTHON_VERSION) /usr/bin/python$(PYTHON_VERSION) /usr/local/bin/python$(PYTHON_VERSION) /opt/homebrew/bin/python$(PYTHON_VERSION)
    # Unix-like systems
    RM_CMD=rm -rf "$1"
    RMFILE_CMD=rm -f "$1"
    MKDIR_CMD=mkdir -p "$1"
    COPY_CMD=cp -r "$1" "$2"
    SEP=/
    # Use curl on Unix-like systems
    DOWNLOAD_CMD=curl -o $(EXTERNAL_DIR)/$(ANTLR_JAR) $(ANTLR_URL) || wget -O $(EXTERNAL_DIR)/$(ANTLR_JAR) $(ANTLR_URL)
    # ANSI color codes (only for Unix-like terminals)
    RED=\033[31m
    GREEN=\033[32m
    YELLOW=\033[33m
    BLUE=\033[34m
    RESET=\033[0m
endif

.PHONY: help check setup build clean clean-cache clean-reports test-lexer test-parser test-ast test-checker clean-venv

# Default target - show help
help:
	@echo "$(BLUE)TyC Project - Available Commands:$(RESET)"
	@echo ""
	@echo "$(GREEN)Setup & Build:$(RESET)"
	@echo "  $(YELLOW)make setup$(RESET)     - Install dependencies and set up environment"
	@echo "  $(YELLOW)make build$(RESET)     - Compile ANTLR grammar files"
	@echo "  $(YELLOW)make check$(RESET)     - Check if required tools are installed"
	@echo ""
	@echo "$(GREEN)Testing:$(RESET)"
	@echo "  $(YELLOW)make test-lexer$(RESET)  - Run lexer tests and generate reports"
	@echo "  $(YELLOW)make test-parser$(RESET) - Run parser tests and generate reports"
	@echo "  $(YELLOW)make test-ast$(RESET)      - Run AST generation tests and generate reports"
	@echo "  $(YELLOW)make test-checker$(RESET)  - Run semantic checker tests (Assignment 3)"
	@echo ""
	@echo "$(GREEN)Cleaning:$(RESET)"
	@echo "  $(YELLOW)make clean$(RESET)         - Clean build and external directories"
	@echo "  $(YELLOW)make clean-cache$(RESET)   - Clean Python cache files"
	@echo "  $(YELLOW)make clean-reports$(RESET) - Clean test reports directory"
	@echo "  $(YELLOW)make clean-venv$(RESET)    - Remove virtual environment"
	@echo ""
	@echo "$(GREEN)Environment:$(RESET)"
	@echo "  Virtual environment: $(VENV_DIR)"
	@echo "  Python version required: $(PYTHON_VERSION)"
	@echo "  ANTLR version: $(ANTLR_VERSION)"
	@echo ""
	@echo "$(BLUE)Quick start: make setup && make build$(RESET)"

check:
	@echo "$(BLUE)Checking required dependencies...$(RESET)"
	@echo ""
	@echo "$(YELLOW)Checking Java installation...$(RESET)"
ifeq ($(OS),Windows_NT)
	@java -version > nul 2>&1 && echo "$(GREEN)✓ Java is installed$(RESET)" || ( \
		echo "$(RED)✗ Java is not installed$(RESET)" && \
		echo "$(YELLOW)  Please install Java manually:$(RESET)" && \
		echo "$(YELLOW)    - Download from https://adoptium.net/ or https://www.oracle.com/java/technologies/downloads/$(RESET)" && \
		echo "$(YELLOW)    - Or use Chocolatey: choco install openjdk$(RESET)" && \
		echo "$(YELLOW)  Make sure Java is in your PATH$(RESET)" \
	)
else
	@java -version > /dev/null 2>&1 && echo "$(GREEN)✓ Java is installed$(RESET)" || ( \
		echo "$(RED)✗ Java is not installed$(RESET)" && \
		echo "$(YELLOW)  Please install Java manually:$(RESET)" && \
		echo "$(YELLOW)    - On macOS: brew install openjdk$(RESET)" && \
		echo "$(YELLOW)    - On Ubuntu/Debian: sudo apt install openjdk-17-jdk$(RESET)" && \
		echo "$(YELLOW)    - Or download from https://adoptium.net/$(RESET)" && \
		echo "$(YELLOW)  Make sure Java is in your PATH$(RESET)" \
	)
endif
	@echo ""
	@echo "$(YELLOW)Checking Python $(PYTHON_VERSION) installation...$(RESET)"
	@if [ -z "$(PYTHON_CMD)" ]; then \
		echo "$(RED)✗ Python $(PYTHON_VERSION) is not installed or not found$(RESET)"; \
		echo "$(YELLOW)  Please install Python $(PYTHON_VERSION) manually:$(RESET)"; \
		echo "$(YELLOW)    - On macOS: brew install python@$(PYTHON_VERSION)$(RESET)"; \
		echo "$(YELLOW)    - On Ubuntu/Debian: sudo apt install python$(PYTHON_VERSION) python$(PYTHON_VERSION)-venv python3-pip$(RESET)"; \
		echo "$(YELLOW)    - On Windows: Download from https://www.python.org/downloads/$(RESET)"; \
		echo "$(YELLOW)  Or make sure Python $(PYTHON_VERSION) is in your PATH$(RESET)"; \
	else \
		echo "$(GREEN)✓ Python $(PYTHON_VERSION) found at: $(PYTHON_CMD)$(RESET)"; \
	fi
	@echo ""
	@echo "$(BLUE)Dependency check completed.$(RESET)"

setup:
	$(call MKDIR_CMD,$(EXTERNAL_DIR))
	@echo "$(BLUE)Setting up project environment...$(RESET)"
	@echo "$(YELLOW)Checking if Java is installed...$(RESET)"
ifeq ($(OS),Windows_NT)
	@java -version > nul 2>&1 || (echo "$(RED)Error: Java is not installed. Please install Java and try again.$(RESET)" && exit 1)
else
	@java -version > /dev/null 2>&1 || (echo "$(RED)Error: Java is not installed. Please install Java and try again.$(RESET)" && exit 1)
endif
	@echo "$(GREEN)Java is installed.$(RESET)"
	@echo "$(YELLOW)Checking if Python $(PYTHON_VERSION) is installed...$(RESET)"
	@if [ -z "$(PYTHON_CMD)" ]; then \
		echo "$(RED)Error: Python $(PYTHON_VERSION) is not installed or not found.$(RESET)"; \
		echo "$(YELLOW)Please install Python $(PYTHON_VERSION) manually:$(RESET)"; \
		echo "$(YELLOW)  - On macOS: brew install python@$(PYTHON_VERSION)$(RESET)"; \
		echo "$(YELLOW)  - On Ubuntu/Debian: sudo apt install python$(PYTHON_VERSION) python$(PYTHON_VERSION)-venv$(RESET)"; \
		echo "$(YELLOW)  - On Windows: Download from https://www.python.org/downloads/$(RESET)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Python $(PYTHON_VERSION) found at: $(PYTHON_CMD)$(RESET)"
	@echo "$(YELLOW)Checking if pip is available...$(RESET)"
	@$(PYTHON_CMD) -m pip --version > /dev/null 2>&1 || (echo "$(RED)Error: pip is not available. Please install pip and try again.$(RESET)" && exit 1)
	@echo "$(GREEN)pip is available.$(RESET)"
	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON_CMD) -m venv $(VENV_DIR); \
		echo "$(GREEN)Virtual environment created at $(VENV_DIR)$(RESET)"; \
	else \
		echo "$(BLUE)Virtual environment already exists at $(VENV_DIR)$(RESET)"; \
	fi
	@echo "$(YELLOW)Downloading ANTLR version $(ANTLR_VERSION)...$(RESET)"
	@echo "$(BLUE)This may take a moment...$(RESET)"
	@$(DOWNLOAD_CMD)
	@echo "$(GREEN)ANTLR downloaded to $(EXTERNAL_DIR)/$(ANTLR_JAR)$(RESET)"
	@echo "$(YELLOW)Upgrading pip in virtual environment...$(RESET)"
	@$(VENV_PIP) install --upgrade pip
	@echo "$(GREEN)pip upgraded successfully.$(RESET)"
	@echo "$(YELLOW)Installing Python dependencies in virtual environment...$(RESET)"
	@$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)Python dependencies installed in virtual environment.$(RESET)"
	@echo "$(GREEN)Setup completed! Virtual environment is ready at $(VENV_DIR)$(RESET)"
	@echo "$(BLUE)To activate the virtual environment manually:$(RESET)"
ifeq ($(OS),Windows_NT)
	@echo "$(BLUE)  $(VENV_DIR)\\Scripts\\activate$(RESET)"
else
	@echo "$(BLUE)  source $(VENV_DIR)/bin/activate$(RESET)"
endif

build: $(GRAMMAR_FILES) $(EXTERNAL_DIR)/$(ANTLR_JAR)
	$(call MKDIR_CMD,$(BUILD_DIR))
	@echo "$(YELLOW)Compiling ANTLR grammar files...$(RESET)"
	@cd src/grammar && java -jar $(EXTERNAL_DIR)/$(ANTLR_JAR) -Dlanguage=Python3 -visitor -no-listener -o $(BUILD_DIR) *.g4
	@echo "$(YELLOW)Creating __init__.py file...$(RESET)"
ifeq ($(OS),Windows_NT)
	@type nul > "$(BUILD_DIR)/__init__.py"
else
	@touch "$(BUILD_DIR)/__init__.py"
endif
	@echo "$(YELLOW)Copying Python files from src/grammar/ to build/$(RESET)"
ifeq ($(OS),Windows_NT)
	@if exist "$(CURDIR)\src\grammar\lexererr.py" copy "$(CURDIR)\src\grammar\lexererr.py" "$(CURDIR)\build\" /Y
else
	@cp -f "$(CURDIR)/src/grammar/lexererr.py" "$(CURDIR)/build/" 2>/dev/null || :
endif
	@echo "$(GREEN)ANTLR grammar files compiled to build/$(RESET)"

clean-cache:
	@echo "$(YELLOW)Cleaning Python cache files...$(RESET)"
	find $(CURDIR) -type d -name "__pycache__" -exec rm -rf {} +
	find $(CURDIR) -type f -name "*.pyc" -exec rm -f {} +
	find $(CURDIR) -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "$(GREEN)Python cache files cleaned.$(RESET)"

clean-reports:
	@echo "$(YELLOW)Cleaning reports directory...$(RESET)"
	$(call RM_CMD,$(REPORT_DIR))
	@echo "$(GREEN)Reports directory cleaned.$(RESET)"

clean-venv:
	@echo "$(YELLOW)Cleaning virtual environment...$(RESET)"
	$(call RM_CMD,$(VENV_DIR))
	@echo "$(GREEN)Virtual environment cleaned.$(RESET)"

clean:
	$(call RM_CMD,$(BUILD_DIR))
	@echo "$(GREEN)Cleaned build directories.$(RESET)"
	@find $(CURDIR) -type d -name "__pycache__" -exec rm -rf {} +
	@find $(CURDIR) -type f -name "*.pyc" -exec rm -f {} +
	@find $(CURDIR) -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "$(GREEN)Cleaned Python cache files recursively.$(RESET)"

test-lexer: build
	@echo "$(YELLOW)Running lexer tests...$(RESET)"
	$(call RM_CMD,$(REPORT_DIR)/lexer)
	$(call MKDIR_CMD,$(REPORT_DIR))
	@PYTHONPATH=$(CURDIR) $(VENV_PYTHON) -m pytest tests/test_lexer.py --html=$(REPORT_DIR)/lexer/index.html --timeout=3 --self-contained-html || true
	@echo "$(GREEN)Lexer tests completed. Reports generated at $(REPORT_DIR)/lexer/index.html$(RESET)"
	@$(MAKE) clean-cache

test-parser: build
	@echo "$(YELLOW)Running parser tests...$(RESET)"
	$(call RM_CMD,$(REPORT_DIR)/parser)
	$(call MKDIR_CMD,$(REPORT_DIR))
	@PYTHONPATH=$(CURDIR) $(VENV_PYTHON) -m pytest tests/test_parser.py --html=$(REPORT_DIR)/parser/index.html --timeout=3 --self-contained-html || true
	@echo "$(GREEN)Parser tests completed. Reports generated at $(REPORT_DIR)/parser/index.html$(RESET)"
	@$(MAKE) clean-cache

test-ast: build
	@echo "$(YELLOW)Running AST generation tests...$(RESET)"
	$(call RM_CMD,$(REPORT_DIR)/ast)
	$(call MKDIR_CMD,$(REPORT_DIR))
	@PYTHONPATH=$(CURDIR) $(VENV_PYTHON) -m pytest tests/test_ast_gen.py --html=$(REPORT_DIR)/ast/index.html --timeout=5 --self-contained-html -v || true
	@echo "$(GREEN)AST generation tests completed. Reports generated at $(REPORT_DIR)/ast/index.html$(RESET)"
	@$(MAKE) clean-cache

test-checker: build
	@echo "$(YELLOW)Running semantic checker tests...$(RESET)"
	$(call RM_CMD,$(REPORT_DIR)/checker)
	$(call MKDIR_CMD,$(REPORT_DIR))
	@PYTHONPATH=$(CURDIR) $(VENV_PYTHON) -m pytest tests/test_checker.py --html=$(REPORT_DIR)/checker/index.html --timeout=10 --self-contained-html -v || true
	@echo "$(GREEN)Checker tests completed. Reports generated at $(REPORT_DIR)/checker/index.html$(RESET)"
	@$(MAKE) clean-cache

# Function to find Python version
define find_python
$(shell for python_cmd in $(PYTHON_CANDIDATES); do \
	if command -v $$python_cmd >/dev/null 2>&1; then \
		version=$$($$python_cmd --version 2>&1 | grep -o "$(PYTHON_VERSION)"); \
		if [ "$$version" = "$(PYTHON_VERSION)" ]; then \
			echo $$python_cmd; \
			break; \
		fi; \
	fi; \
done)
endef

PYTHON_CMD=$(call find_python)
