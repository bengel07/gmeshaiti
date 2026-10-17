<#
  Compare les fichiers .py et .html du projet (Windows) avec ceux d'Ubuntu,
  puis rend Ubuntu identique. Les autres types de fichiers ne sont jamais touches.

  Rapport seulement :  powershell -ExecutionPolicy Bypass -File .\synchroniser_ubuntu.ps1
  Appliquer         :  powershell -ExecutionPolicy Bypass -File .\synchroniser_ubuntu.ps1 -Appliquer
#>
param([switch]$Appliquer)

# ================== A ADAPTER SI BESOIN ==================
$Local   = "C:\Users\conta\Desktop\GMEShaiti"
$Serveur = "gmes@10.0.0.77"
$Dossier = "/home/gmes/gmeshaiti"
$Service = "gmes.service"

# Seuls ces types de fichiers sont compares et envoyes
$Extensions = @("py", "html")

# Dossiers ignores (environnements Python, fichiers generes, donnees)
$DossiersExclus = @(".git", ".venv", "venv", "env", "__pycache__", "node_modules", "instance",
                    "static/uploads", ".idea", ".vscode", ".pytest_cache", "build", "dist")

# Fichiers .py ou .html a ne jamais envoyer (scripts utilises seulement sur ton PC)
$FichiersExclus = @("appliquer_correctifs.py", "creer_tables_investisseurs.py", "investisseurs_patch.py")
# =========================================================

$latin1 = [System.Text.Encoding]::GetEncoding(28591)
$sha    = [System.Security.Cryptography.SHA256]::Create()

function Est-Exclu([string]$rel) {
    foreach ($d in $DossiersExclus) {
        if ($rel -eq $d -or $rel.StartsWith("$d/") -or $rel.Contains("/$d/") -or $rel.EndsWith("/$d")) { return $true }
    }
    $nom = $rel.Substring($rel.LastIndexOf("/") + 1)
    foreach ($f in $FichiersExclus) { if ($nom -like $f) { return $true } }
    return $false
}

function Est-Inclus([string]$rel) {
    $ext = [System.IO.Path]::GetExtension($rel).TrimStart(".").ToLower()
    return ($Extensions -contains $ext)
}

# Hash du contenu en ignorant les fins de ligne Windows (CRLF) / Linux (LF)
function Hash-Fichier([string]$chemin) {
    $octets = [System.IO.File]::ReadAllBytes($chemin)
    $s = $latin1.GetString($octets).Replace("`r", "")
    return ([BitConverter]::ToString($sha.ComputeHash($latin1.GetBytes($s)))).Replace("-", "").ToLower()
}

function Parcourir([string]$dir, [string]$racine, [hashtable]$res) {
    foreach ($e in (Get-ChildItem -LiteralPath $dir -Force)) {
        $rel = $e.FullName.Substring($racine.Length + 1).Replace("\", "/")
        if ($e.PSIsContainer) {
            if ($e.Attributes -band [System.IO.FileAttributes]::ReparsePoint) { continue }
            if (-not (Est-Exclu $rel)) { Parcourir $e.FullName $racine $res }
        }
        else {
            if ((Est-Exclu $rel) -or (-not (Est-Inclus $rel))) { continue }
            $res[$rel] = Hash-Fichier $e.FullName
        }
    }
}

function Manifeste-Local {
    $res = @{}
    $racine = (Resolve-Path -LiteralPath $Local).Path.TrimEnd("\")
    Parcourir $racine $racine $res
    return $res
}

function Manifeste-Serveur {
    $cases = @()
    foreach ($d in $DossiersExclus) { $cases += "$d/*"; $cases += "*/$d/*" }
    foreach ($f in $FichiersExclus) { $cases += $f;     $cases += "*/$f" }
    $excl = $cases -join "|"
    $noms = (($Extensions | ForEach-Object { "-name '*.$_'" }) -join " -o ")

    $modele = @'
cd "__DOSSIER__" || exit 1
find . \( -name .git -o -name .venv -o -name venv -o -name node_modules -o -name __pycache__ -o -path ./static/uploads -o -path ./instance \) -prune -o -type f \( __NOMS__ \) -print | sed 's|^\./||' | while IFS= read -r f; do
  case "$f" in
    __EXCL__) continue ;;
  esac
  h=$(tr -d '\r' < "$f" | sha256sum | cut -d' ' -f1)
  printf '%s\t%s\n' "$h" "$f"
done
'@
    $script = $modele.Replace("__DOSSIER__", $Dossier).Replace("__NOMS__", $noms).Replace("__EXCL__", $excl).Replace("`r`n", "`n")
    $b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($script))

    $lignes = & ssh $Serveur "echo $b64 | base64 -d > /tmp/gmes_manifeste.sh; bash /tmp/gmes_manifeste.sh; r=`$?; rm -f /tmp/gmes_manifeste.sh; exit `$r"
    if ($LASTEXITCODE -ne 0) { throw "Echec de la connexion SSH ou de l'analyse du serveur." }

    $res = @{}
    foreach ($l in $lignes) {
        if ($l -match '^([0-9a-f]{64})\t(.+)$') { $res[$Matches[2]] = $Matches[1] }
    }
    return $res
}

function Comparer($loc, $srv) {
    $diff = @(); $manquants = @(); $enTrop = @()
    foreach ($k in ($loc.Keys | Sort-Object)) {
        if (-not $srv.ContainsKey($k)) { $manquants += $k }
        elseif ($srv[$k] -ne $loc[$k]) { $diff += $k }
    }
    foreach ($k in ($srv.Keys | Sort-Object)) {
        if (-not $loc.ContainsKey($k)) { $enTrop += $k }
    }
    return @{ Diff = $diff; Manquants = $manquants; EnTrop = $enTrop }
}

function Afficher($titre, $liste, $couleur) {
    Write-Host ""
    Write-Host "$titre : $($liste.Count)" -ForegroundColor $couleur
    $liste | Select-Object -First 100 | ForEach-Object { Write-Host "   $_" }
    if ($liste.Count -gt 100) { Write-Host "   ... et $($liste.Count - 100) autres" }
}

# ----------------------------------------------------------
Write-Host "========================================"
Write-Host "  COMPARAISON WINDOWS / UBUNTU  (.py et .html)"
Write-Host "========================================"
Write-Host "Analyse du dossier local..."
$loc = Manifeste-Local
Write-Host "  $($loc.Count) fichiers .py/.html locaux analyses"

Write-Host "Analyse d'Ubuntu (le mot de passe SSH est demande)..."
$srv = Manifeste-Serveur
Write-Host "  $($srv.Count) fichiers .py/.html analyses sur Ubuntu"

$r = Comparer $loc $srv
Afficher "DIFFERENTS (le contenu n'est pas le meme)" $r.Diff "Yellow"
Afficher "ABSENTS d'Ubuntu (existent sur ton PC)" $r.Manquants "Cyan"
Afficher "SEULEMENT sur Ubuntu (jamais supprimes par ce script)" $r.EnTrop "Gray"

$aEnvoyer = @($r.Diff) + @($r.Manquants)
if ($aEnvoyer.Count -eq 0) {
    Write-Host ""
    Write-Host "Les fichiers .py et .html sont IDENTIQUES." -ForegroundColor Green
    exit 0
}

if (-not $Appliquer) {
    Write-Host ""
    Write-Host "Rien n'a ete modifie. Pour rendre Ubuntu identique a ton PC :"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\synchroniser_ubuntu.ps1 -Appliquer"
    exit 0
}

Write-Host ""
Write-Host "ATTENTION : la version de ton PC va remplacer celle d'Ubuntu pour $($aEnvoyer.Count) fichier(s)." -ForegroundColor Yellow
Write-Host "Verifie surtout les fichiers de configuration (adresses, URL, mots de passe) dans la liste ci-dessus."
$rep = Read-Host "Taper OUI pour continuer"
if ($rep -ne "OUI") { Write-Host "Annule."; exit 1 }

$date = Get-Date -Format "yyyy-MM-dd_HHmmss"

if ($r.Diff.Count -gt 0) {
    Write-Host "Sauvegarde sur Ubuntu des versions remplacees..."
    ($r.Diff -join "`n") | & ssh $Serveur "cd $Dossier && mkdir -p ~/sauvegarde_serveur && tr -d '\r' | tar -czf ~/sauvegarde_serveur/avant_sync_$date.tgz -T -"
    if ($LASTEXITCODE -ne 0) { Write-Host "Echec de la sauvegarde : rien n'a ete modifie." -ForegroundColor Red; exit 1 }
}

$liste = Join-Path $env:TEMP "gmes_sync_liste.txt"
$tar   = Join-Path $env:TEMP "gmes_sync.tar"
[System.IO.File]::WriteAllText($liste, (($aEnvoyer -join "`n") + "`n"), (New-Object System.Text.UTF8Encoding($false)))

& tar -cf $tar -C $Local -T $liste
if ($LASTEXITCODE -ne 0) { Write-Host "Echec de la preparation de l'archive." -ForegroundColor Red; exit 1 }

Write-Host "Envoi des fichiers..."
& scp $tar "${Serveur}:/tmp/gmes_sync.tar"
if ($LASTEXITCODE -ne 0) { Write-Host "Echec de l'envoi." -ForegroundColor Red; exit 1 }

Write-Host "Mise en place et redemarrage du service..."
& ssh $Serveur "cd $Dossier && tar -xf /tmp/gmes_sync.tar && rm -f /tmp/gmes_sync.tar && .venv/bin/python -m py_compile app.py models.py database.py && sudo systemctl restart $Service && sleep 3 && sudo systemctl is-active $Service"
$etat = $LASTEXITCODE
Remove-Item $liste, $tar -ErrorAction SilentlyContinue
if ($etat -ne 0) {
    Write-Host "Les fichiers sont copies mais le controle ou le redemarrage a echoue." -ForegroundColor Red
    Write-Host "Anciennes versions : ~/sauvegarde_serveur/avant_sync_$date.tgz sur Ubuntu."
    exit 1
}

Write-Host "Verification finale..."
$srv2 = Manifeste-Serveur
$r2 = Comparer $loc $srv2
if (($r2.Diff.Count + $r2.Manquants.Count) -eq 0) {
    Write-Host ""
    Write-Host "TERMINE : les fichiers .py et .html d'Ubuntu sont IDENTIQUES a ceux de ton PC." -ForegroundColor Green
    Write-Host "Fais Ctrl+F5 dans le navigateur."
} else {
    Afficher "TOUJOURS DIFFERENTS" $r2.Diff "Red"
    Afficher "TOUJOURS ABSENTS" $r2.Manquants "Red"
}