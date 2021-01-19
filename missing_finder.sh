#!/usr/bin/env bash

# Author: Charlie Kapsiak    
# Modified: 2021-01-19
# Description: Find missing students given a zoom attendance file and a canvas grade export (as the base list)

function getEmails() {
awk -v email="$1" -F "\"*,\"*" '
    NR==1 {
        for (i=1; i<=NF; i++) {
            gsub(/"/,"",$i)
            f[$i] = i
        }
    }
    NR > 1 { 
    x=$(f[email])
    sub(/"/,"",x)
    print(x)

}
' $2 | sort
}

#getEmails "Email" "$1"
#echo "--------------------"
#getEmails "User Email" "$2"


#diff --new-line-format="" --unchanged-line-format=""  <(getEmails "Email" "$1") <(getEmails "User Email" "$2")

missing=($(awk 'BEGIN { FS="" } # preserve whitespace
(NR==FNR) { ll1[FNR]=$0; nl1=FNR; }     # file1, index by lineno
(NR!=FNR) { ss2[$0]++; }                # file2, index by string
END {
    for (ll=1; ll<=nl1; ll++) if (!(ll1[ll] in ss2)) print ll1[ll]
    }' <(getEmails "Email" "$1") <(getEmails "User Email" "$2") ))

echo "Found ${#missing[@]} students!"
echo ${missing[@]}

for student in ${missing[@]}; do
    awk -v student="$student" -F "\"*,\"*" ' NR==1 {
        for (i=1; i<=NF; i++) {
            gsub(/"/,"",$i)
            f[$i] = i
        }}

    $(f["Email"]) ~ student { 
    x=$(f["Email"])
    sub(/"/,"",x)
    print $(f["First Name"]),$(f["Last Name"]) , "-----" , student }
  
' "$1"
done


