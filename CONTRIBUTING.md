# Contributing to Azure Agentic AI

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Describe the issue clearly with steps to reproduce
- Include system information (OS, Python version, etc.)

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Add docstrings to classes and methods
- Keep functions focused and small
- Write unit tests for new features

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run validation
python FINAL_VALIDATION.py
```

### Documentation
- Update README.md if adding new features
- Add docstrings to new functions
- Update architecture diagrams if needed

## Development Setup

```bash
# Clone repository
git clone https://github.com/Rajanm001/agent-azur.git
cd agent-azur

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Run in mock mode
python src/main.py
```

## Questions?

Open an issue or contact the maintainer.

---

Maintained by Rajan Mishra
