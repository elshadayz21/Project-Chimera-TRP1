param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Cmd
)

# Ensure running from repo root for relative paths
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

$message = "Command: $($Cmd -join ' ')"

# Call the local Python trigger logger (silent for passage)
python .\scripts\log_triggers.py --type passage --message $message 2>$null

# Execute the requested command
& $Cmd
