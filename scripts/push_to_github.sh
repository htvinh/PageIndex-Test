#!/bin/bash

# PageIndex Testing Application - GitHub Push Script
# This script safely pushes changes to GitHub with proper exclusions

set -e

echo "📤 PageIndex Testing Application - GitHub Push"
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    echo "Initialize with: git init"
    exit 1
fi

# Check if .gitignore exists, create if not
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Application specific
temp/
pdf_images/
*.log

# Exclude folders starting with underscore
_*/
EOF
    echo "✅ Created .gitignore"
fi

# Show current status
echo "📊 Current git status:"
git status --short
echo ""

# Get commit message
echo "💬 Enter commit message:"
read -r COMMIT_MESSAGE

if [ -z "$COMMIT_MESSAGE" ]; then
    echo "❌ Error: Commit message cannot be empty"
    exit 1
fi

# Add files (respecting .gitignore)
echo ""
echo "➕ Adding files..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short
echo ""

# Confirm before committing
read -p "Continue with commit? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Commit cancelled"
    exit 1
fi

# Commit changes
echo ""
echo "💾 Committing changes..."
if git commit -m "$COMMIT_MESSAGE"; then
    echo "✅ Changes committed successfully"
else
    echo "ℹ️  No changes to commit (working tree clean)"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No remote 'origin' found"
    echo ""
    echo "To push to GitHub:"
    echo "1. Create a repository on GitHub"
    echo "2. Run: git remote add origin <your-repo-url>"
    echo "3. Run: git push -u origin main"
    echo ""
    echo "Or run this script again after adding the remote."
    exit 0
fi

# Get current branch
BRANCH=$(git branch --show-current)

if [ -z "$BRANCH" ]; then
    echo "❌ Error: Could not determine current branch"
    exit 1
fi

echo ""
echo "🚀 Pushing to origin/$BRANCH..."

# Push to remote
if git push origin "$BRANCH" 2>&1; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📍 Branch: $BRANCH"
    echo "💬 Message: $COMMIT_MESSAGE"
else
    EXIT_CODE=$?
    echo ""
    if [ $EXIT_CODE -eq 128 ]; then
        echo "💡 First time pushing this branch?"
        echo "   Run: git push -u origin $BRANCH"
    else
        echo "❌ Push failed with exit code: $EXIT_CODE"
        echo "💡 Try: git push -u origin $BRANCH"
    fi
    exit 1
fi

echo ""
echo "✨ Done!"

# Made with Bob
