# 🤝 Contributing to OMI Twitter Integration

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 🎨 Improve UI/UX

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/twitter.git
cd twitter
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your credentials
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 style guide for Python code:

```bash
# Install development tools
pip install black flake8 mypy

# Format code
black .

# Check style
flake8 .

# Type checking
mypy .
```

### Code Structure

```
twitter/
├── main.py              # FastAPI application and routes
├── models.py            # Database models
├── twitter_client.py    # Twitter API client
├── tweet_detector.py    # AI-powered tweet detection
├── requirements.txt     # Python dependencies
└── tests/              # Test files (create this)
```

### Adding New Features

1. **Plan**: Open an issue to discuss your idea
2. **Implement**: Write clean, documented code
3. **Test**: Add tests for new functionality
4. **Document**: Update README if needed

### Example: Adding a New Trigger Phrase

```python
# In tweet_detector.py
TRIGGER_PHRASES = [
    "tweet now",
    "post tweet",
    "send tweet",
    "your new phrase"  # Add here
]
```

## 🧪 Testing

### Run Manual Tests

```bash
# Start the server
python main.py

# In another terminal, run tests
python test_endpoints.py
```

### Write Unit Tests

Create tests in `tests/` directory:

```python
# tests/test_tweet_detector.py
import pytest
from tweet_detector import TweetDetector

def test_detect_trigger():
    assert TweetDetector.detect_trigger("tweet now hello")
    assert not TweetDetector.detect_trigger("hello world")

def test_extract_content():
    content = TweetDetector.extract_tweet_content("tweet now hello world")
    assert content == "hello world"
```

Run tests:
```bash
pytest tests/
```

## 📚 Documentation

### Code Comments

```python
def process_segments(session: Session, segments: List[Dict]) -> str:
    """
    Process transcript segments and handle tweet commands.
    
    Args:
        session: Current user session
        segments: List of transcript segment dicts
        
    Returns:
        Status message string
    """
    # Implementation...
```

### README Updates

If your change affects usage:
- Update README.md
- Update SETUP_INSTRUCTIONS.md if setup changes
- Update DEPLOYMENT.md if deployment changes

## 🔍 Code Review Process

1. **Self Review**: Review your own code first
2. **Tests Pass**: Ensure all tests pass
3. **Documentation**: Update relevant docs
4. **Submit PR**: Create a pull request
5. **Address Feedback**: Respond to review comments

## 🐛 Bug Reports

When reporting bugs, include:

```markdown
**Describe the bug**
Clear description of what happened

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Say '...'
3. See error

**Expected behavior**
What you expected to happen

**Environment:**
- OS: [e.g. macOS 13.0]
- Python version: [e.g. 3.11]
- Deployment: [e.g. Railway, local]

**Logs**
```
Paste relevant error logs here
```

**Additional context**
Any other information
```

## 💡 Feature Requests

When suggesting features:

```markdown
**Problem**
What problem does this solve?

**Solution**
Your proposed solution

**Alternatives**
Other solutions you've considered

**Additional context**
Examples, mockups, etc.
```

## 🔒 Security Issues

**Do not open public issues for security vulnerabilities!**

Instead:
1. Email security@yourproject.com (if you have one)
2. Or open a private security advisory on GitHub

## 📜 Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add support for custom trigger phrases"
git commit -m "Fix OAuth redirect on mobile devices"
git commit -m "Update deployment docs for Railway"

# Bad
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

### Commit Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat: Add support for Twitter Spaces detection

- Add new trigger phrase "join space"
- Implement space URL extraction
- Update documentation

Closes #123
```

## 🔀 Pull Request Process

1. **Update Dependencies**
   ```bash
   pip freeze > requirements.txt
   ```

2. **Run Tests**
   ```bash
   python test_endpoints.py
   ```

3. **Create PR**
   - Clear title describing the change
   - Detailed description
   - Link related issues
   - Add screenshots if UI changes

4. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   How was this tested?
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-reviewed code
   - [ ] Commented complex code
   - [ ] Updated documentation
   - [ ] No new warnings
   - [ ] Added tests
   - [ ] Tests pass locally
   ```

5. **After Submission**
   - Respond to review comments
   - Make requested changes
   - Keep PR up to date with main branch

## 🎨 UI/UX Improvements

For UI changes (auth success page, etc.):
- Keep it clean and minimal
- Mobile-responsive
- Follow modern design principles
- Test on multiple devices

## 🌍 Internationalization

If adding language support:
- Use language files for strings
- Test with different languages
- Update documentation

## 📊 Performance

When optimizing:
- Benchmark before and after
- Document performance improvements
- Consider edge cases
- Test with production-like data

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Getting Help

- 💬 Join our Discord/Slack (if applicable)
- 📧 Email: your-email@example.com
- 🐛 Open an issue for bugs
- 💡 Discussion board for questions

## 📖 Additional Resources

- [OMI Documentation](https://docs.omi.me)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [Python Best Practices](https://docs.python-guide.org)

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉 Every contribution, no matter how small, makes a difference!

