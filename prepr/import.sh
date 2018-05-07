# students productivity csv is already well formatted, I can simply import it
mongoimport -d exams -c rawStudentsPr1013 --type csv --file ../raw/prod_stud_10-11-12-13.csv --headerline

# didactic evaluation is a bit more tricky
# need to manipulate a bit the cvs before feeding it to mongoimort

< ../raw/val_didattica_10-11.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1011 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_11-12.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1112 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_12-13.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1213 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_13-14.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1314 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_14-15.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1415 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_15-16.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1516 --type csv --headerline --file temp
rm temp

< ../raw/val_didattica_16-17.csv tr "\"" " " | tr "," "." | tr ";" "," > temp
mongoimport -d exams -c rawTeachingsEv1617 --type csv --headerline --file temp
rm temp
