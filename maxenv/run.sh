set -e
command="1"

function valid() {
    echo "valid"
    python learn.py train1.txt.transfer train2.txt.transfer valid.txt 1
}
function sub() {
    echo "sub"
    python learn.py train.txt.transfer test.txt.transfer sub.csv 0
}

if [ $command == "1" ];then
    valid
elif [ $command == "2" ];then
    sub
elif [ $command == "3" ];then
    valid
    sub
fi
