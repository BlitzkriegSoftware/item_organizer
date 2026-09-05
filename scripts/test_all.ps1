#    Run all pytests with coverage

function Find-GitRepositoryRoot {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath
    )

    [string]$herePath = $FilePath
    [bool]$isFile = Test-Path -Path $herePath -PathType Leaf
    # Write-Output "${herePath}: Is Leaf: $isFile"
    if ($isFile) {
        $herePath = (Get-Item $FilePath).DirectoryName
    }
    
    while (($null -ne $herePath) -and ($herePath.Length -gt 0)) {
        [string]$lookFor = Join-Path -Path $herePath -ChildPath ".git"
        # Write-Output "HP: ${herePath}, LF: ${lookFor}"
        if (Test-Path $lookFor -PathType Container) {
            return $herePath
        }
        $herePath = (Get-Item $herePath).Parent.FullName
    }

    Write-Warning "${FilePath}: No Git repository found in the path or its parent directories."
    return $null
}

Set-StrictMode -Version 2.0
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12
Push-Location $PSScriptRoot

$GIT_ROOT = Find-GitRepositoryRoot -FilePath $PSScriptRoot
if ($null -eq $GIT_ROOT) {
    Write-Error "Not in GIT Repo"
    return 9;
}

# Start processing
Push-Location $GIT_ROOT

uv run coverage run -m pytest -s
uv run coverage report -m