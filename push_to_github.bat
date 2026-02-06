@echo off
REM Push to GitHub. Usage: push_to_github.bat YOUR_GITHUB_USERNAME YOUR_REPO_NAME
REM Example: push_to_github.bat johndoe quantum-fi
cd /d "%~dp0"
if "%~1"=="" (
    echo Usage: push_to_github.bat YOUR_GITHUB_USERNAME YOUR_REPO_NAME
    echo Example: push_to_github.bat johndoe quantum-fi
    echo.
    echo Or do it manually - see GITHUB_PUSH.md
    pause
    exit /b 1
)
if "%~2"=="" (
    echo Usage: push_to_github.bat YOUR_GITHUB_USERNAME YOUR_REPO_NAME
    echo Example: push_to_github.bat johndoe quantum-fi
    pause
    exit /b 1
)
set USER=%~1
set REPO=%~2
git remote remove origin 2>nul
git remote add origin https://github.com/%USER%/%REPO%.git
echo Pushing to https://github.com/%USER%/%REPO%.git
git push -u origin main
pause
