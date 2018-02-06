initilize() {
    PWD=`pwd`
    DIRNAME=`dirname $0`
    BASE=$DIRNAME/..
    cd $BASE
}

finalize() {
    cd $PWD
}

run() {
    pipenv run $@
}

run_su() {
    run sudo -u restrictsandbox $@
}