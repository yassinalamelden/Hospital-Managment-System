# deep_clean.ps1
# PowerShell script to Deep Clean and restructure Django project

$BaseDir = Get-Location
Write-Host "Starting Deep Clean in: $BaseDir"

# 1. Create Directories
$ConfigDir = Join-Path $BaseDir "config"
if (-not (Test-Path $ConfigDir)) { New-Item -ItemType Directory -Path $ConfigDir | Out-Null; Write-Host "Created 'config' directory." }

$BackupDir = Join-Path $BaseDir "_legacy_backup"
if (-not (Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir | Out-Null; Write-Host "Created '_legacy_backup' directory." }

$InitFile = Join-Path $ConfigDir "__init__.py"
if (-not (Test-Path $InitFile)) { New-Item -ItemType File -Path $InitFile | Out-Null }

# 2. Move Configuration Files to Config
$FilesToMove = @("settings.py", "urls.py", "wsgi.py", "asgi.py")

foreach ($File in $FilesToMove) {
    $SourcePath = Join-Path $BaseDir $File
    $DestPath = Join-Path $ConfigDir $File
    
    if (Test-Path $SourcePath) {
        Move-Item -Path $SourcePath -Destination $DestPath -Force
        Write-Host "Moved $File to config/"
    }
    elseif (Test-Path (Join-Path $BaseDir "hospital_system" $File)) {
        # Handle case where they might be in inner folder
        Move-Item -Path (Join-Path $BaseDir "hospital_system" $File) -Destination $DestPath -Force
        Write-Host "Moved hospital_system/$File to config/"
    }
    else {
        Write-Host "WARNING: $File not found in root or hospital_system/."
    }
}

# 3. Handle Nested 'hospital_system' Folder
$InnerProjectDir = Join-Path $BaseDir "hospital_system"
if (Test-Path $InnerProjectDir) {
    Write-Host "Found nested 'hospital_system' directory. Moving contents to backup."
    Move-Item -Path $InnerProjectDir -Destination $BackupDir -Force
}

# 4. Handle Legacy 'modules' or 'backend' if they exist
$LegacyDirs = @("backend", "modules")
foreach ($Dir in $LegacyDirs) {
    $Path = Join-Path $BaseDir $Dir
    if (Test-Path $Path) {
        Move-Item -Path $Path -Destination $BackupDir -Force
        Write-Host "Moved legacy folder '$Dir' to backup."
    }
}

# 5. Ensure Manage.py is in Root
# If manage.py is not in current dir, try to copy from parent (common structure issue)
if (-not (Test-Path "manage.py")) {
    if (Test-Path "../manage.py") {
        Copy-Item -Path "../manage.py" -Destination "."
        Write-Host "Copied manage.py from parent directory."
    }
    else {
        Write-Host "WARNING: manage.py not found!"
    }
}

Write-Host "Deep Clean Complete. PLEASE UPDATE settings.py and manage.py!"
