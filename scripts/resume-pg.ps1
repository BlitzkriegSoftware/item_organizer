<#
    .SYNOPSIS
       Resume w/reset PostgreSQL on Docker

    .DESCRIPTION
        See above
    
    .INPUTS
        none

    .OUTPUTS
        Sucess or failure 
#>

Import-Module Microsoft.PowerShell.Utility

[int]$PORT = 5432
[string]$SERVER = "localhost"
[string]$CUSTOM_IMAGE = 'postgres_item_organizer'
[string]$NAME = 'postgressvr'
[string]$MASTERDB = 'postgres'
[string]$USERNAME = 'postgres'
[string]$PASSWORD = 'password123-'
[string]$VOL = "/var/lib/postgresql/data"
[string]$PGPASS_FILE = '/var/lib/postgresql/data/.pgpass'

function Get-DockerRunning {

	[bool]$DockerAlive = $false

	try {
		$null = Get-Process 'com.docker.backend' -ErrorAction Stop
		$DockerAlive = $true;
	}
 catch {
		$DockerAlive = $false;
	}

	return $DockerAlive
}

#
# Main
#
Set-StrictMode -Version 2.0
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12
Push-Location $PSScriptRoot

[bool]$da = Get-DockerRunning
if (! $da) {
	Write-Error "docker must be running 1st"
	return 1;
}

# Dispose of any old running Postgres
$null = (docker stop "${NAME}") 2> $null
$null = (docker rm "${NAME}") 2> $null

# Set working variables in PS1
$null = (setx POSTGRES_USER "${USERNAME}") 2> $null
$null = (setx POSTGRES_PASSWORD "${PASSWORD}") 2> $null

# Volume mapping path
[string]$dbPath = Join-Path -Path $PSScriptRoot -ChildPath "data"

# Start the container
docker run -d `
	-e "POSTGRES_USER=${USERNAME}" `
	-e "POSTGRES_PASSWORD=${PASSWORD}" `
	-e "PGPASSWORD=${PASSWORD}" `
	-e "PGPASSFILE=${PGPASS_FILE}" `
	-e PGDATA='/var/lib/postgresql/data/pgdata' `
	--name="${NAME}" `
	--restart always `
	-v "${dbPath}:${VOL}" `
	-p "${PORT}:${PORT}" "${CUSTOM_IMAGE}"

[string]$cs = "postgresql://${USERNAME}:${PASSWORD}@${SERVER}:${PORT}/${MASTERDB}";

Write-Output "`n`n${cs}`n`n"