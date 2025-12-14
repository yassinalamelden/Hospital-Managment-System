# standardize_project.ps1
# Script to enforce Industry Standard "Two Scoops" Layout

$BaseDir = Get-Location
Write-Host "Standardizing Project Structure in: $BaseDir"

# 1. Create _TRASH_BIN
$TrashDir = Join-Path $BaseDir "_TRASH_BIN"
if (-not (Test-Path $TrashDir)) { 
    New-Item -ItemType Directory -Path $TrashDir | Out-Null
    Write-Host "Created _TRASH_BIN."
}

# 2. Rename Old Archive if exists
$OldArchive = Join-Path $BaseDir "_ARCHIVE_TRASH"
if (Test-Path $OldArchive) {
    Get-ChildItem -Path $OldArchive | Move-Item -Destination $TrashDir -Force
    Remove-Item -Path $OldArchive -Force
    Write-Host "Merged _ARCHIVE_TRASH into _TRASH_BIN."
}

# 3. Handle 'hospital_system' -> 'config'
$ConfigDir = Join-Path $BaseDir "config"
$InnerProj = Join-Path $BaseDir "hospital_system"

if ((Test-Path $InnerProj) -and (-not (Test-Path $ConfigDir))) {
    Rename-Item -Path $InnerProj -NewName "config"
    Write-Host "Renamed 'hospital_system' to 'config'."
}
elseif ((Test-Path $InnerProj) -and (Test-Path $ConfigDir)) {
    # If both exist, move old to trash
    Move-Item -Path $InnerProj -Destination $TrashDir -Force -ErrorAction SilentlyContinue
    Write-Host "Moved redundant 'hospital_system' to Trash."
}

# 4. App Elevation & Asset Consolidation
$ItemsToRoot = @("accounts", "operations", "billing", "core", "templates", "static")
foreach ($Item in $ItemsToRoot) {
    $RootPath = Join-Path $BaseDir $Item
    if (-not (Test-Path $RootPath)) {
        # Check subfolders
        $Found = Get-ChildItem -Path $BaseDir -Recurse -Filter $Item -Directory -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "_TRASH_BIN" } | Select-Object -First 1
        if ($Found) {
            Move-Item -Path $Found.FullName -Destination $BaseDir -Force
            Write-Host "Moved $Item to Root."
        }
    }
}

# 5. Deep Clean specific items
$JunkItems = @("backend", "modules", "_legacy_backup", "final_cleanup.ps1")
foreach ($Junk in $JunkItems) {
    $Path = Join-Path $BaseDir $Junk
    if (Test-Path $Path) {
        Move-Item -Path $Path -Destination $TrashDir -Force
        Write-Host "Moved $Junk to Trash."
    }
}

# 6. Cleanup Pycache
Get-ChildItem -Path $BaseDir -Recurse -Filter "__pycache__" -Directory | Remove-Item -Recurse -Force
Write-Host "Cleaned __pycache__."

Write-Host "Standardization Complete."
