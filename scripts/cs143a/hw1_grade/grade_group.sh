#!/bin/bash

create_gradebook()
{
    touch ./group_grades.csv
    echo "Created new gradebook."
    echo "index,score,extra,comments,files" >> ./group_grades.csv
}

if [ -d "./submissions" ]; then
    echo "Submissions already exist, skip unzipping..."
    echo
else
    echo "Unzipping submissions..."
    mkdir submissions
    unzip ./submissions.zip -d ./submissions 1>/dev/null
    echo
fi

if [ -e "./group_grades.csv" ]; then
    read -p "Found an existing gradebook, do you want to overwrite or continue? [o/c]: " oc
    case $oc in
        [Oo]* ) rm -f ./group_grades.csv; create_gradebook; break;;
        [Cc]* ) break;;
        * ) echo "Bad input."; break;;
    esac
else
    create_gradebook
fi

group1=($(seq 1 53))
group2=($(seq 54 106))
group3=($(seq 107 159))

mkdir -p ./results

for i in ${group2[@]}
do
    line_num=$(($i+2))
    line=`sed -n "${line_num}p" ./cs143a_roster.csv`
    IFS=',' read -r -a ll <<< "$line"
    id=${ll[2]}
    name=${ll[1]}

    files=($(ls ./submissions | grep "[a-z]*_${id}_"))
    echo ">>>Now grading "$i", "$name", id "$id"..."
    echo "Submitted file(s): "${files[@]}
    
    rm -rf ./results/$i
    mkdir -p ./results/$i

    for f in ${files[@]}
    do
        cp ./submissions/$f ./results/$i/
    done

    cp ./tests/* ./results/$i
    cd ./results/$i

    ../../grade_one.py -i $i -f ${files[@]}
    echo "Done"
    echo 

    cd -
done
