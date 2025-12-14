# refactor_packages.ps1
# Script to convert monolithic apps to package-based apps

$BaseDir = Get-Location
Write-Host "Refactoring Apps to Packages in: $BaseDir"

$Apps = @("accounts", "operations", "billing")
$TrashDir = Join-Path $BaseDir "_TRASH_BIN"
$BackupDir = Join-Path $TrashDir "original_files_backup"

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Created backup directory."
}

foreach ($App in $Apps) {
    $AppDir = Join-Path $BaseDir $App
    
    # Define new directories
    $ModelsDir = Join-Path $AppDir "models"
    $ViewsDir = Join-Path $AppDir "views"
    
    # Create new directories
    if (-not (Test-Path $ModelsDir)) { New-Item -ItemType Directory -Path $ModelsDir | Out-Null }
    if (-not (Test-Path $ViewsDir)) { New-Item -ItemType Directory -Path $ViewsDir | Out-Null }
    
    # Move old files
    $OldModels = Join-Path $AppDir "models.py"
    $OldViews = Join-Path $AppDir "views.py"
    
    if (Test-Path $OldModels) {
        $Dest = Join-Path $BackupDir "${App}_models.py"
        Move-Item -Path $OldModels -Destination $Dest -Force
        Write-Host "Moved $App/models.py to backup."
    }
    
    if (Test-Path $OldViews) {
        $Dest = Join-Path $BackupDir "${App}_views.py"
        Move-Item -Path $OldViews -Destination $Dest -Force
        Write-Host "Moved $App/views.py to backup."
    }
    
    # Create __init__.py files
    New-Item -ItemType File -Path (Join-Path $ModelsDir "__init__.py") -Force | Out-Null
    New-Item -ItemType File -Path (Join-Path $ViewsDir "__init__.py") -Force | Out-Null
}

Write-Host "Folder structure created. Ready for code generation."
