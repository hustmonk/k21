vw="/usr/local/bin/vw"
function run() {
    train=$1
    test=$2
    #$vw  -c -k -q cf -q ff  --cubic cff --learning_rate 0.01 --passes 3 $train -f ${train}.model.vw --invert_hash model.hash
    $vw  -c -k -q cf --learning_rate 0.01 --passes 300 --loss_function  logistic $train -f ${train}.model.vw --invert_hash model.hash
    $vw -t -i ${train}.model.vw --oaa 9 $test -p ${train}.pred -r ${train}.raw -a >xy
    #$vw -t -i ${train}.model.vw  $test -p ${test}.pred -r ${test}.raw
}
run train1.txt train2.txt
#run train.txt test.txt 
