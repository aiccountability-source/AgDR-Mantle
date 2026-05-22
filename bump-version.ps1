param([string]$level = "patch")

$toml = Get-Content Cargo.toml -Raw
$version = [regex]::Match($toml, 'version = "(\d+)\.(\d+)\.(\d+)"').Groups
$major = [int]$version[1].Value
$minor = [int]$version[2].Value
$patch = [int]$version[3].Value

switch ($level) {
    "major" { $major++; $minor = 0; $patch = 0 }
    "minor" { $minor++; $patch = 0 }
    "patch" { $patch++ }
}

$newVersion = "$major.$minor.$patch"
$toml = $toml -replace 'version = "\d+\.\d+\.\d+"', "version = `"$newVersion`""
Set-Content Cargo.toml $toml -NoNewline

Write-Host "Bumped to $newVersion"