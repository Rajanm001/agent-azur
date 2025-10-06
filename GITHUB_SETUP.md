# GitHub Repository Setup Guide

## Step-by-Step Instructions to Upload to GitHub

### Prerequisites
- Git installed on your system
- GitHub account created
- Repository created at: https://github.com/Rajanm001/agent-azur

### Method 1: Using Git Command Line (Recommended)

```bash
# Navigate to your project directory
cd "c:\Users\Rajan mishra Ji\assisngment 1"

# Configure Git (first time only)
git config --global user.name "Rajan Mishra"
git config --global user.email "your-email@example.com"

# Initialize repository (already done)
git init

# Add remote repository
git remote add origin https://github.com/Rajanm001/agent-azur.git

# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Complete Azure Agentic AI System - Production Ready"

# Push to GitHub
git push -u origin master

# If master branch not accepted, use main
git branch -M main
git push -u origin main
```

### Method 2: Using GitHub Desktop

1. Download and install GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. Click "File" → "Add Local Repository"
4. Browse to: `c:\Users\Rajan mishra Ji\assisngment 1`
5. Click "Publish repository"
6. Uncheck "Keep this code private" if you want it public
7. Click "Publish Repository"

### Method 3: Using VS Code

1. Open project in VS Code
2. Click on Source Control icon (left sidebar)
3. Click "Publish to GitHub"
4. Select "Public" or "Private"
5. Choose repository name: agent-azur
6. Click "Publish"

### Updating Repository After Changes

```bash
# Check what changed
git status

# Add specific files
git add README.md src/main.py

# Or add all changes
git add .

# Commit with message
git commit -m "Updated documentation and fixed bugs"

# Push to GitHub
git push
```

### Creating Releases

```bash
# Tag a version
git tag -a v1.0 -m "Version 1.0 - Production Release"

# Push tags
git push --tags
```

### Repository Structure on GitHub

After upload, your repository will have:

```
agent-azur/
├── .github/
│   └── workflows/
│       └── tests.yml           # Automated testing
├── docs/
│   └── SECURITY_GOVERNANCE.md
├── src/
│   ├── agents/
│   ├── services/
│   └── utils/
├── tests/
├── tools/
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── requirements.txt
├── .gitignore
└── [other files]
```

### Making Repository Professional

#### 1. Add Repository Description
- Go to https://github.com/Rajanm001/agent-azur
- Click "Edit" next to About
- Add: "Enterprise-grade AI agent for automated Azure VM RDP troubleshooting. 89.8% auto-resolution rate, 34-second average resolution time."

#### 2. Add Topics
Add these tags:
- azure
- artificial-intelligence
- automation
- devops
- troubleshooting
- python
- openai
- prometheus
- monitoring

#### 3. Enable GitHub Pages (Optional)
- Go to Settings → Pages
- Source: Deploy from branch
- Branch: main, folder: /docs
- Your docs will be at: https://rajanm001.github.io/agent-azur/

#### 4. Create Issues Template
Go to Settings → Features → Issues → Set up templates

#### 5. Add Repository Banner
Create a banner image and add to README.md:
```markdown
![Azure Agentic AI Banner](./docs/banner.png)
```

### Troubleshooting

#### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/Rajanm001/agent-azur.git
```

#### Error: "failed to push"
```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push origin main
```

#### Error: "Permission denied"
```bash
# Use personal access token instead of password
# Generate at: https://github.com/settings/tokens
# Use token as password when prompted
```

### Verification

After upload, verify:
- [ ] All files visible on GitHub
- [ ] README.md displays correctly
- [ ] Links in README work
- [ ] GitHub Actions running (if configured)
- [ ] Repository description set
- [ ] Topics added
- [ ] LICENSE file present

### Next Steps

1. Upload to GitHub using method above
2. Add repository description and topics
3. Create a release (v1.0)
4. Share repository link
5. Add to your resume/portfolio

---

Repository: https://github.com/Rajanm001/agent-azur
Author: Rajan Mishra
Date: October 6, 2025
