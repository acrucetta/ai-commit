# AI Conventional Commit Generator

Generate conventional commit messages automatically using AI (Claude) to analyze your staged changes.

## Features

- 🤖 Uses Claude AI to analyze git diff and generate meaningful commit messages
- 📝 Follows [Conventional Commits](https://www.conventionalcommits.org/) specification
- 🚀 Easy to install and use
- 🔒 Secure API key management
- 🔄 Preview commits before applying

## Installation

### Using pipx (recommended)
[pipx](https://pypa.github.io/pipx/) lets you install and run Python CLI applications in isolated environments.

```bash
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath

# Install ai-commit
pipx install git+https://github.com/yourusername/ai-commit.git
```

### Using pip
```bash
pip install git+https://github.com/yourusername/ai-commit.git
```

### Development Installation
```bash
git clone https://github.com/yourusername/ai-commit.git
cd ai-commit
pip install -e .
```

## Configuration

Before using the tool, you need to configure your Anthropic API key. You can either:

1. Set it as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

2. Or configure it using the CLI:
```bash
ai-commit configure
```

## Usage

1. Stage your changes as usual:
```bash
git add .
# or
git add specific-file.txt
```

2. Preview the AI-generated commit message:
```bash
ai-commit commit --preview
```

3. If you're happy with the message, create the commit:
```bash
ai-commit commit
```

## Example

```bash
# Stage some changes
git add feature.py

# Preview the commit message
$ ai-commit commit --preview
Generating commit message... ⏳
Generated commit message:
feat(core): add user authentication functionality

# Create the commit
$ ai-commit commit
Successfully committed with message:
feat(core): add user authentication functionality
```

## Requirements

- Python 3.8 or higher
- Git
- Anthropic API key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using the tool itself! (`ai-commit commit`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Anthropic Claude](https://www.anthropic.com/claude)
- [Click](https://click.palletsprojects.com/)
