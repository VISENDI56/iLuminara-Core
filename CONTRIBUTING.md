# Contributing to iLuminara

Thank you for your interest in contributing to iLuminara Sovereign Health Interface! This document provides guidelines and best practices for contributing to the project.

## 🌟 Ways to Contribute

- **Report Bugs**: Submit detailed bug reports via GitHub Issues
- **Suggest Features**: Propose new features or enhancements
- **Improve Documentation**: Fix typos, clarify instructions, add examples
- **Submit Code**: Fix bugs, implement features, improve performance
- **Write Tests**: Add test coverage for existing functionality
- **Review Pull Requests**: Help review and test community contributions

## 📋 Before You Start

1. **Read the Code of Conduct**: Please review our [Code of Conduct](./CODE_OF_CONDUCT.md)
2. **Check Existing Issues**: Search for existing issues before creating new ones
3. **Review Documentation**: Familiarize yourself with the [project documentation](https://visendi56.mintlify.app/)
4. **Understand the Architecture**: Read the [Nuclear IP Stack documentation](./NUCLEAR_IP_STACK.md)

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/iLuminara-Core.git
cd iLuminara-Core

# Add upstream remote
git remote add upstream https://github.com/VISENDI56/iLuminara-Core.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run verification tests
python scripts/verify_singularity.py
python scripts/verify_49_laws.py
python scripts/system_seal.py
```

### 3. Create a Branch

```bash
# Create a descriptive branch name
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

## 💻 Development Workflow

### Code Style

- **Python**: Follow [PEP 8](https://pep8.org/) style guide
- **Line Length**: Maximum 100 characters
- **Imports**: Group and sort imports (standard library, third-party, local)
- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Type Hints**: Use type hints for function signatures

Example:

```python
from typing import Dict, List, Optional

def calculate_compliance_score(
    frameworks: List[str],
    data_stream: Dict[str, float],
    threshold: Optional[float] = 0.70
) -> float:
    """Calculate overall compliance health score.
    
    Args:
        frameworks: List of regulatory framework IDs
        data_stream: Dictionary of operational metrics
        threshold: Minimum acceptable score (default: 0.70)
    
    Returns:
        Compliance health score between 0.0 and 1.0
    
    Raises:
        ValueError: If frameworks list is empty
    """
    # Implementation here
    pass
```

### Testing

- **Write Tests**: All new features must include tests
- **Run Tests Locally**: Ensure all tests pass before submitting PR

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=governance_kernel --cov-report=html
```

### Security

- **No Secrets**: Never commit API keys, passwords, or sensitive data
- **Validate Input**: Always validate and sanitize user input
- **Use Parameterized Queries**: Avoid SQL injection vulnerabilities
- **SSL/TLS**: Explicit certificate verification for all HTTP requests

```python
# Good: Explicit verification
response = requests.get(url, verify=True)

# Bad: Disabled verification
response = requests.get(url, verify=False)  # Never do this!
```

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**

```
feat(rco): add predictive amendment engine

Implements external signal analysis to forecast regulatory
changes before they occur. Uses Bayesian inference to
estimate probability of amendment within 90 days.

Closes #123
```

### Commit Best Practices

- **Atomic Commits**: One logical change per commit
- **Clear Messages**: Write descriptive commit messages
- **Reference Issues**: Link to relevant issue numbers
- **Sign Commits**: Use GPG signatures for verified commits (optional but recommended)

## 🔄 Pull Request Process

### 1. Update Your Branch

```bash
# Fetch latest changes from upstream
git fetch upstream
git rebase upstream/main
```

### 2. Run All Checks

```bash
# Format code (if using formatter)
black governance_kernel/ tests/

# Run linters
flake8 governance_kernel/ tests/

# Run all tests
pytest tests/ -v

# Run security checks
python scripts/verify_49_laws.py
python scripts/verify_singularity.py
```

### 3. Submit Pull Request

1. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### 4. PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged and published

## Testing
Describe the tests you ran and their results.

## Screenshots (if applicable)
Add screenshots showing UI changes.

## Related Issues
Closes #123
```

### 5. Review Process

- **Code Review**: Maintainers will review your PR
- **Address Feedback**: Respond to comments and make requested changes
- **CI Checks**: Ensure all automated checks pass
- **Approval**: At least one maintainer approval required
- **Merge**: Maintainer will merge your PR

## 🎯 Contribution Areas

### High-Priority Areas

1. **Edge Deployment**: NVIDIA Jetson, Raspberry Pi optimization
2. **Mobile Apps**: Flutter offline-first implementation
3. **Multi-Language**: Swahili, French, Arabic translations
4. **Performance**: Optimization for resource-constrained environments
5. **Testing**: Increase test coverage (target: 90%+)

### Good First Issues

Look for issues labeled `good first issue` or `help wanted` in the [issue tracker](https://github.com/VISENDI56/iLuminara-Core/issues).

## 📚 Resources

- **Documentation**: [visendi56.mintlify.app](https://visendi56.mintlify.app/)
- **Demo Guide**: [DEMO_README.md](./DEMO_README.md)
- **API Docs**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Security Policy**: [SECURITY.md](./SECURITY.md)
- **Code of Conduct**: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)

## 💬 Getting Help

- **GitHub Discussions**: Ask questions in [Discussions](https://github.com/VISENDI56/iLuminara-Core/discussions)
- **GitHub Issues**: Report bugs via [Issues](https://github.com/VISENDI56/iLuminara-Core/issues)
- **Email**: sovereign@iluminara.com

## 🙏 Recognition

Contributors will be recognized in:
- **README.md**: Contributors section
- **Release Notes**: Acknowledgment in changelogs
- **Contributors Graph**: Automatic GitHub recognition

## 📜 License

By contributing to iLuminara, you agree that your contributions will be licensed under the [Apache License 2.0](./LICENSE).

---

Thank you for contributing to iLuminara! Together, we're building a sovereign, compliant, and accessible health intelligence platform. 🏛️
