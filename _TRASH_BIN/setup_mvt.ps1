# setup_mvt.ps1
# PowerShell script to restructure Django project for MVT pattern

$BaseDir = Get-Location
Write-Host "Setting up MVT Structure in: $BaseDir"

# 1. Templates Layer
$TemplatesDir = Join-Path $BaseDir "templates"
$Apps = @("accounts", "operations", "billing")

# Create root templates dir
if (-not (Test-Path $TemplatesDir)) {
    New-Item -ItemType Directory -Path $TemplatesDir | Out-Null
    Write-Host "Created templates directory"
}

# Create app subfolders in templates
foreach ($App in $Apps) {
    $AppTemplateDir = Join-Path $TemplatesDir $App
    if (-not (Test-Path $AppTemplateDir)) {
        New-Item -ItemType Directory -Path $AppTemplateDir | Out-Null
        Write-Host "Created templates/$App"
    }
}

# Create partials folder
$PartialsDir = Join-Path $TemplatesDir "partials"
if (-not (Test-Path $PartialsDir)) {
    New-Item -ItemType Directory -Path $PartialsDir | Out-Null
    Write-Host "Created templates/partials"
}

# Ensure base.html exists (if not, creating a placeholder is handled by previous steps, but we check)
$BaseHtml = Join-Path $TemplatesDir "base.html"
if (-not (Test-Path $BaseHtml)) {
    Write-Host "WARNING: base.html missing in templates root."
}

# 2. Static Layer
$StaticDir = Join-Path $BaseDir "static"
if (-not (Test-Path $StaticDir)) {
    New-Item -ItemType Directory -Path $StaticDir | Out-Null
    Write-Host "Created static directory"
}

$StaticSubFolders = @("css", "js", "images")
foreach ($Sub in $StaticSubFolders) {
    $SubDir = Join-Path $StaticDir $Sub
    if (-not (Test-Path $SubDir)) {
        New-Item -ItemType Directory -Path $SubDir | Out-Null
        Write-Host "Created static/$Sub"
    }
}

# 3. Forms Layer
# Create forms.py in each app if it doesn't exist
foreach ($App in $Apps) {
    $AppDir = Join-Path $BaseDir $App
    $FormsFile = Join-Path $AppDir "forms.py"
    
    if (-not (Test-Path $FormsFile)) {
        New-Item -ItemType File -Path $FormsFile | Out-Null
        Set-Content -Path $FormsFile -Value "from django import forms`n# Create your forms here"
        Write-Host "Created $App/forms.py"
    } else {
        Write-Host "$App/forms.py already exists. Skipping."
    }
}

Write-Host "MVT Restructuring Complete!"
