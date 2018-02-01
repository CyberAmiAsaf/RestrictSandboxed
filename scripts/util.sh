initilize() {
    PWD=`pwd`
    DIRNAME=`dirname $0`
    BASE=$DIRNAME/..
    cd $BASE
}

finalize() {
    cd $PWD
}