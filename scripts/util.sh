initilize() {
    PWD=`pwd`
    BASE=`dirname $0`/..

    set -e
    cd $BASE
}

finalize() {
    cd $PWD
}