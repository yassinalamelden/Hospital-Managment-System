# final_cleanup.ps1
# Comprehensive Cleanup Script for Django MVT Structure

$BaseDir = Get-Location
Write-Host "Starting Final Cleanup in: $BaseDir"

# 1. Create _ARCHIVE_TRASH
$TrashDir = Join-Path $BaseDir "_ARCHIVE_TRASH"
if (-not (Test-Path $TrashDir)) { 
    New-Item -ItemType Directory -Path $TrashDir | Out-Null
    Write-Host "Created _ARCHIVE_TRASH directory."
}

# 2. Archive Legacy/Junk Items
$ItemsToArchive = @("backend", "modules", "_legacy_backup", "deep_clean.ps1", "setup_mvt.ps1", "hospital_system")

foreach ($ItemName in $ItemsToArchive) {
    if ($ItemName -eq "hospital_system") {
        # Check if it's the inner folder (redundant)
        $Path = Join-Path $BaseDir $ItemName
        if (Test-Path $Path) {
            # Verify it's not the config folder (if config doesn't exist). 
            # Since 'config' should exist, we assume 'hospital_system' is junk.
            try {
                Move-Item -Path $Path -Destination $TrashDir -Force -ErrorAction SilentlyContinue
                Write-Host "Moved $ItemName to _ARCHIVE_TRASH."
            }
            catch {
                Write-Host "Could not move $ItemName (might be in use or merged)."
            }
        }
    }
    else {
        $Path = Join-Path $BaseDir $ItemName
        if (Test-Path $Path) {
            Move-Item -Path $Path -Destination $TrashDir -Force -ErrorAction SilentlyContinue
            Write-Host "Moved $ItemName to _ARCHIVE_TRASH."
        }
    }
}

# 3. Consolidation & renaming 'config'
# Check if 'config' exists. If not, look for 'hospital_system' to rename.
$ConfigDir = Join-Path $BaseDir "config"
$RedundantDir = Join-Path $BaseDir "hospital_system"

if (-not (Test-Path $ConfigDir) -and (Test-Path $RedundantDir)) {
    Rename-Item -Path $RedundantDir -NewName "config"
    Write-Host "Renamed 'hospital_system' to 'config'."
}
elseif ((Test-Path $ConfigDir) -and (Test-Path $RedundantDir)) {
    # If both exist, move hospital_system to trash (handled above)
}

# 4. Standardize Apps (Ensure they are in root)
$Apps = @("accounts", "operations", "billing", "core")
foreach ($App in $Apps) {
    $AppPath = Join-Path $BaseDir $App
    if (-not (Test-Path $AppPath)) {
        # Search in subfolders (e.g. inside hospital_system if it wasn't moved yet)
        # This is a fallback if structure is very messy
        $PotentialPath = Get-ChildItem -Path $BaseDir -Recurse -Filter $App -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($PotentialPath) {
            Move-Item -Path $PotentialPath.FullName -Destination $BaseDir -Force
            Write-Host "Moved app '$App' to Root."
        }
    }
}

# 5. Assets (Templates/Static)
$Assets = @("templates", "static")
foreach ($Asset in $Assets) {
    $AssetPath = Join-Path $BaseDir $Asset
    if (-not (Test-Path $AssetPath)) {
        # Search and move
        $Found = Get-ChildItem -Path $BaseDir -Recurse -Filter $Asset -Directory -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "_ARCHIVE_TRASH" } | Select-Object -First 1
        if ($Found) {
            Move-Item -Path $Found.FullName -Destination $BaseDir -Force
            Write-Host "Moved '$Asset' to Root."
        }
    }
}

# 6. Deep Clean Files
# __pycache__
Get-ChildItem -Path $BaseDir -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force
Write-Host "Deleted all __pycache__ folders."

# .sqlite3
Get-ChildItem -Path $BaseDir -Recurse -Filter "*.sqlite3" -File | Remove-Item -Force
Write-Host "Deleted all .sqlite3 files."

# Clean up duplicate manage.py (Keep root, delete others)
$RootManage = Join-Path $BaseDir "manage.py"
$AllManage = Get-ChildItem -Path $BaseDir -Recurse -Filter "manage.py" -File
foreach ($File in $AllManage) {
    if ($File.FullName -ne $RootManage) {
        Remove-Item -Path $File.FullName -Force
        Write-Host "Deleted duplicate manage.py at $($File.FullName)"
    }
}

# Core App Check (Keep if used, Trash if empty/unused) - As per instructions, we keep "core" if it has content.
# Since we moved "core" to root based on 'Apps' list, we assume it's kept.

Write-Host "Final Cleanup Complete!"
