<#
.SYNOPSIS
    Run all tests and generate coverage report
#>    

param (
    [Parameter(Mandatory = $false)]
    [bool]$ShowOutPut = $False
)


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

if ($ShowOutPut) {
    Write-Host("=" * $Host.UI.RawUI.WindowSize.Width)
    # Write-Host("Running pytest with coverage (output will be shown)")
    . uv run coverage run -m pytest -s -v
    $ec = $?
    Write-Host("=" * $Host.UI.RawUI.WindowSize.Width)
}
else {
    Write-Host("Running pytest with coverage (output will be hidden)")
    . uv run coverage run -m pytest  *> $null
    $ec = $?
}

# Write-Host("`nExit Code: ${ec}`n")

if ($ec -eq $true) {
    Write-Host("-" * $Host.UI.RawUI.WindowSize.Width)
    uv run coverage report -m
    Write-Host("-" * $Host.UI.RawUI.WindowSize.Width)
}
else {
    Write-Host("No tests were run or all tests failed. use -ShowOutPut $True to see the output.")
}

Pop-Location