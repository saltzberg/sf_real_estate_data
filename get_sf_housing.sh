#!/bin/bash
#

i=1
outfile="sf_home_sales.csv"

echo "county; address; city; zip; sale_date; price" > $outfile


for i in {1..42351}
do
inpage="http://b2.caspio.com/dp.asp?appSession=58820846466662740484104412450424120100246027563912442952762160494542970225546961293444642650006444384105214656397364214164981454&RecordID=&PageID=2&PrevPageID=1&cpipage=$i&CPISortType=&CPIorderBy="

echo $inpage | wget -O- -i- | grep "San Francisco County" | sed $'s/><\/span>/\\\n/g' | tail -n+2 > temp

head -n1 temp | awk -F "</*td>|</*tr>" '/<\/*t[rd]>.*[A-Z][A-Z]/ {print $7 "; " $9 "; " $11"; " $13"; " $15 "; " $17 }'  >> $outfile
tail -n+2 temp | awk -F "</*td>|</*tr>" '/<\/*t[rd]>.*[A-Z][A-Z]/ {print $5 "; " $7 "; "$9"; " $11"; "$13 "; " $15 }'  >> $outfile
#>> $outfile

done

