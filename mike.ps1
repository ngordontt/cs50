$fname = Get-Content C:\Scripts\firstname.csv
$CSV = Import-Csv C:\scripts\alpha.csv
$Score = 0

foreach ($name in $fname) {
    $array = $name.ToCharArray()
    Foreach ($charinst in $array) {
        ForEach ($row in $CSV) {
            if ($row.letter -eq $charinst) {
                $AdjacentCell = $row.value
            }
        } 
        $Score += $AdjacentCell

    }
    $Score
    $Score = 0    
} 
