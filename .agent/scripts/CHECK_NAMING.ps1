param(
  [string]$RootPath
)

# Naming rule check (user/AI files must be UPPER_SNAKE_CASE)
$RootBase = if ($RootPath) { $RootPath } else { Join-Path $PSScriptRoot '..\\..' }
$Root = (Resolve-Path $RootBase).Path

$UpperSnakePattern = '^[A-Z0-9]+(_[A-Z0-9]+)*$'

$FixedNames = @(
  'README.md',
  'SKILL.md',
  'DESIGN.md',
  'LICENSE',
  'CHANGELOG.md',
  '__init__.py',
  'docker-compose.yml',
  'docker-compose.yaml',
  'package.json'
)

$AutoFiles = @(
  'pnpm-lock.yaml',
  'package-lock.json',
  'yarn.lock',
  'npm-shrinkwrap.json',
  'poetry.lock',
  'Pipfile.lock',
  'uv.lock',
  'composer.lock',
  'Cargo.lock',
  'go.mod',
  'go.sum'
)

$SkipDirs = @(
  '.git',
  '.github',
  '.venv',
  'node_modules',
  'dist',
  'build',
  'coverage',
  '__pycache__',
  '.pytest_cache',
  '.mypy_cache',
  '.ruff_cache',
  '.cache',
  '.next',
  '.nuxt',
  '.turbo',
  '.parcel-cache',
  '.svelte-kit',
  'out',
  'target',
  'bin',
  'obj',
  '.gradle',
  '.idea',
  '.vscode',
  '.devcontainer',
  'secure',
  'runs',
  'logs',
  'tmp',
  'temp'
)

$TargetExts = @(
  '.md', '.txt', '.ps1', '.py', '.js', '.ts', '.json', '.yaml', '.yml',
  '.toml', '.ini', '.cfg', '.sh', '.bat', '.cmd', '.html', '.css',
  '.mmd', '.drawio', '.svg'
)

$violations = New-Object System.Collections.Generic.List[string]
$checked = 0

Get-ChildItem -LiteralPath $Root -Recurse -File -Force | ForEach-Object {
  $rel = ($_.FullName.Substring($Root.Length)) -replace '^[\\/]+', ''
  $parts = $rel -split '[\\/]'
  if ($parts.Length -gt 1) {
    foreach ($dir in $parts[0..($parts.Length - 2)]) {
      if ($SkipDirs -contains $dir) {
        return
      }
    }
  }

  $name = $_.Name
  if ($FixedNames -contains $name) { return }
  if ($AutoFiles -contains $name) { return }

  $ext = $_.Extension.ToLowerInvariant()
  if (-not $TargetExts.Contains($ext)) { return }

  $base = [System.IO.Path]::GetFileNameWithoutExtension($name)
  $checked++
  if ($base -cnotmatch $UpperSnakePattern) {
    $violations.Add($rel) | Out-Null
  }
}

if ($violations.Count -eq 0) {
  Write-Output ("OK: COUNT={0}" -f $checked)
  exit 0
}

Write-Output ("NG: COUNT={0} NG_COUNT={1}" -f $checked, $violations.Count)
$violations | Sort-Object | ForEach-Object { Write-Output ("- {0}" -f $_) }
exit 1
