envexec() {
    PWD=`pwd`
    DIRNAME=`dirname $0`
    BASE=$DIRNAME/..
    cd $BASE
    $@
    cd $PWD
}