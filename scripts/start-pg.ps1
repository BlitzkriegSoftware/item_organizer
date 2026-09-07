<#
    .SYNOPSIS
       Start PostgreSQL then Item-Organizer on Docker

    .DESCRIPTION
        See above
    
    .INPUTS
        none

    .OUTPUTS
        Sucess or failure 
#>

Import-Module Microsoft.PowerShell.Utility

<#
	Shared Variables
#>
[string]$SERVER = "localhost"
[string]$USERNAME = 'postgres'
[string]$PASSWORD = 'password123-'

<#
	POSTGRES Variables
#>
[int]$DB_PORT = 5432
[string]$CUSTOM_IMAGE = 'postgres_item_organizer'
[string]$NAME = 'postgressvr'
[string]$MASTERDB = 'postgres'
[string]$BIN = '/usr/lib/postgresql/16/bin'
[string]$VOL = "/var/lib/postgresql/data"
[string]$PGPASS_FILE = '/var/lib/postgresql/data/.pgpass'
[string]$IOR_SCHEMA = "myio" # default item-organizer

<#
	Application Variables
#>

[int]$APP_PORT = 8097 

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

function Get-PortBlocked {
	param (
		[Int32]$TEST_PORT 
	)

	[bool]$flag = $false;

	$inUse = Test-NetConnection localhost -Port $TEST_PORT

	if (($null -eq $inUse) -or (-not $inUse.TcpTestSucceeded)) {
		$flag = $true;
	}

	return $flag;
}

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

$GIT_ROOT = Find-GitRepositoryRoot -FilePath $PSScriptRoot
if ($null -eq $GIT_ROOT) {
	Write-Error "Not in GIT Repo"
	return 9;
}

[bool]$da = Get-DockerRunning
if (! $da) {
	Write-Error "docker must be running 1st"
	return 1;
}

# [bool]$isBlocked = Get-PortBlocked -TEST_PORTt $DB_PORT;
# if ($isBlocked) {
# 	Write-Error "DB_PORT ${DB_PORT} for postgres is in use! Stop local service before re-running."
# 	return 2;
# }

#
# Start processing
Push-Location $GIT_ROOT

# Dispose of any old running Postgres
$null = (docker stop "${NAME}") 2> $null
$null = (docker rm "${NAME}") 2> $null

# Set working variables in PS1
$null = (setx POSTGRES_USER "${USERNAME}") 2> $null
$null = (setx POSTGRES_PASSWORD "${PASSWORD}") 2> $null

# Volume mapping path
[string]$dbPath = Join-Path -Path $GIT_ROOT -ChildPath "data"
Write-Debug "Data Path: ${dbPath}"

# Working path
[string]$workPath = Join-Path -Path $GIT_ROOT -ChildPath ".working"
New-Item -ItemType Directory -Force -Path $workPath | Out-Null
Write-Debug "Working Path: ${workPath}"

# Create .pgpass file
$PGPASS_LINES = @(
	"# File: $HOME/.pgpass",
	"#       chmod 600 $HOME/.pgpass",
	"#       export PGPASSFILE=$HOME/.pgpass",
	"#",
	"# Configuration:",
	"#   hostname:port:database:username:password",
	"#",
	"${SERVER}:${DB_PORT}:${MASTERDB}:${USERNAME}:${PASSWORD}"
)

[string]$PGPASS_FILE = "./data/.pgpass" 
if (Test-Path $PGPASS_FILE) {
	Remove-Item $PGPASS_FILE -Force
}
foreach ($line in $PGPASS_LINES) {
	Write-Output $line >> $PGPASS_FILE
}

# Windows to linux file ending fixs
$FILES_TO_PATCH = @(
	"${PGPASS_FILE}",
	".\data\postgresql.conf.cron"
)

# Make Image Readme.md

$README_FILE = Join-Path -Path $workPath -ChildPath "README.md"
$README_LINES = @(
	"# ${CUSTOM_IMAGE}",
	"",
	"PostgreSQL 16 with Item-Organizer",
	
	"## Ports",
	"",
	"- DB_PORT: ${DB_PORT}",
	"- APP_PORT: ${APP_PORT}"
)
$README_LINES | Set-Content -Path $README_FILE -encoding UTF8 
Write-Output "Created ${README_FILE}"

$SQL_FILES = Get-ChildItem -Path "${dbpath}\*.sql" -File -Recurse
$SCRIPT_FILES = Get-ChildItem -Path "${dbpath}\*.sh" -File -Recurse
$WORKING_FILES = Get-ChildItem -Path "${workPath}\*.*" -File -Recurse

$FILES_TO_PATCH = $FILES_TO_PATCH + $SQL_FILES + $SCRIPT_FILES + $WORKING_FILES;
foreach ($FilePath in $FILES_TO_PATCH) {
	(Get-Content -Raw -Path $FilePath) -replace "`r`n", "`n" | Set-Content -Path $FilePath -NoNewline
}

# Force a clean start
$pgDir = Join-Path -Path $dbPath -ChildPath "pgdata"
$null = (Remove-Item -Path $pgDir -Recurse -Force) 2> $null

# Ensure clean pull of pinned image
#$null = (docker pull $IMAGE) 2> $null
docker build --progress=plain -t "${CUSTOM_IMAGE}" .

# Required encryption support variables
$IOR_SALT = $env:IOR_SALT
if ( [string]::IsNullOrEmpty("${IOR_SALT}") ) {
	$IOR_SALT = "JDJiJDEyJGU1QTV0Zzk1VGxxVmpBLjdsRERmRnU="
}

$IOR_FERMAT = $env:IOR_FERMAT
if ( [string]::IsNullOrEmpty("${IOR_FERMAT}") ) {
	$IOR_FERMAT = 'dENwNS1GVGdKZUhzdFdCcC1VMGtmNl9ZVTBpZWpWLWlhcHd1dUY1M0R2MD0='
}

$README_FILE_PATH = [System.IO.Path]::GetRelativePath("${GIT_ROOT}", "${README_FILE}")

# Start the container
docker run -d `
	-e "POSTGRES_USER=${USERNAME}" `
	-e "POSTGRES_PASSWORD=${PASSWORD}" `
	-e "PGPASSWORD=${PASSWORD}" `
	-e "PGPASSFILE=${PGPASS_FILE}" `
	-e PGDATA='/var/lib/postgresql/data/pgdata' `
	-e "IOR_SALT=${IOR_SALT}" `
	-e "IOR_FERMAT=${IOR_FERMAT}" `
	-e "IOR_DB_PORT=${DB_PORT}" `
	-e "IOR_SCHEMA=${IOR_SCHEMA}" `
	-e "README_FILE_PATH=${README_FILE_PATH}" `
	--name="${NAME}" `
	--restart always `
	-v "${dbPath}:${VOL}" `
	-p "${DB_PORT}:${DB_PORT}" `
	-p "${APP_PORT}:${APP_PORT}" `
	"${CUSTOM_IMAGE}"

# Wait for Startup
Write-Output "Waiting for container to start..."
Start-Sleep -Seconds 30

# Set up plugins
docker exec --workdir "${BIN}" "${NAME}" "/var/lib/postgresql/data/configure_pg.sh"

Write-Output "Waiting for container to start..."
Start-Sleep -Seconds 30

# Register cron
docker exec --workdir "${BIN}" "${NAME}" "/var/lib/postgresql/data/pg_cron_add.sh"

[string]$cs = "postgresql://${USERNAME}:${PASSWORD}@${SERVER}:${DB_PORT}/${MASTERDB}";

Write-Output "`n`n${cs}`n`n"