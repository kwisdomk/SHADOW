$word = New-Object -ComObject Word.Application
$word.Visible = $false

$files = @(
    "q:\0AMD_DEV_Hackathon\SHADOW\docs\high & low lvl.docx",
    "q:\0AMD_DEV_Hackathon\SHADOW\docs\Shadow Overview + Technical Architecture..docx",
    "q:\0AMD_DEV_Hackathon\SHADOW\docs\shortcomings & mitigations.docx"
)

foreach ($f in $files) {
    $doc = $word.Documents.Open($f)
    $txt = $doc.Content.Text
    $out = $f -replace "\.docx$", ".txt"
    [System.IO.File]::WriteAllText($out, $txt, [System.Text.Encoding]::UTF8)
    $doc.Close($false)
    Write-Host "Exported: $out"
}

$word.Quit()
Write-Host "Done."
