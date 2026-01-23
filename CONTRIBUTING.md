# Contributing to TickZero

Thank you for your interest in contributing to this project! 🎉

## 🤝 How to Contribute

We welcome contributions from the community, including:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🌍 Translations
- ⚡ Performance optimizations
- 🧪 Test coverage

## 📋 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/TickZero.git
cd TickZero
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements

### 4. Set Up Development Environment

### 4. Set Up Development Environment

```bash
# Install Poetry (if not already installed)
pip install poetry

# Install dependencies and create environment
poetry install

# Activate shell
poetry shell
```

### 5. Make Your Changes

- Write clean, readable code
- Follow existing code style and conventions
- Add comments for complex logic
- Update documentation if needed

### 6. Test Your Changes

Before submitting:

```bash
# Test API connection
python examples/test_gemini_api.py

# Test the full pipeline (if possible)
python main.py live
# (play a short match)
python main.py process <video_path>
```

### 7. Commit Your Changes

```bash
git add .
git commit -m "Brief description of your changes"
```

**Commit message conventions:**
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Be concise but descriptive
- Reference issue numbers if applicable (#123)

**Examples:**
- `Fix: Resolve timestamp sync issue with OBS`
- `Add: Support for custom video resolution settings`
- `Docs: Update Italian translation for README`

### 8. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 9. Create a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

## 🎯 Contribution Guidelines

### Code Style

- **Python:** Follow PEP 8 guidelines
- **Naming:** Use descriptive variable/function names
- **Comments:** Explain *why*, not *what*
- **Line length:** Max 120 characters

### Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Include usage examples where helpful
- Translate important docs to other languages (optional but appreciated!)

### Testing

- Test your changes thoroughly before submitting
- Include steps to reproduce in PR description
- Report any edge cases or known limitations

### Commits

- Make atomic commits (one logical change per commit)
- Write clear commit messages
- Don't include unrelated changes

## 🌍 Translation Contributions

We welcome translations! To add a new language:

1. Create `docs/i18n/README.[lang].md` (e.g., `README.es.md` for Spanish)
2. Translate the main README.md
3. Add link to main README.md language selector
4. Optional: Translate QUICKSTART and SETUP_GEMINI guides

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Verify it's not a configuration issue

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots/Logs**
If applicable, add screenshots or error logs.

**Environment:**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.10.5]
- OBS version: [e.g., 29.1.3]

**Additional context**
Any other relevant information.
```

## 💡 Feature Requests

We love new ideas! To suggest a feature:

1. Check existing feature requests
2. Open a discussion (not an issue) to gather feedback
3. Explain the use case and benefits
4. Be open to alternative solutions

## 📞 Questions?

- 💬 Use [Discussions](https://github.com/MACULINX/TickZero/discussions) for questions
- 🐛 Use [Issues](https://github.com/MACULINX/TickZero/issues) for bugs
- 📧 Email maintainers for sensitive topics

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License with the same attribution requirements as the project.

## ✅ Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what's best for the project
- Accept constructive criticism gracefully

## 🙏 Recognition

All contributors will be recognized in our README.md! Your GitHub profile will be automatically added to the contributors section.

---

**Thank you for contributing! 🎮🚀**
