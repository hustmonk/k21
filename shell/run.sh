valid="0"
sub="1"

if [ $valid == "1" ];then
    echo "valid"
python features.py ../data/train2/log_train.csv ../data/train2/enrollment_train.csv train2.txt
python features.py ../data/train1/log_train.csv ../data/train1/enrollment_train.csv train1.txt
python learn.py train1.txt train2.txt valid.txt 1
fi
if [ $sub == "1" ];then
    echo "sub"
python features.py ../data/test/log_test.csv ../data/test/enrollment_test.csv test.txt
python features.py ../data/train/log_train.csv ../data/train/enrollment_train.csv train.txt
python learn.py train.txt test.txt sub.csv 0
fi
