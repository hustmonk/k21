vw="/usr/local/bin/vw"
function run() {
    train=$1
    test=$2
    $vw  -c -k -q ff --learning_rate 0.01 --passes 300 $train -f ${train}.model.vw
    #$vw -t -i ${train}.model.vw --oaa 9 $test -p ${train}.pred -r ${train}.raw -a >xy
    $vw -t -i ${train}.model.vw  $test -p ${test}.pred -r ${test}.raw
}
run train1.txt train2.txt
#run train.txt test.txt 
