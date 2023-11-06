function run(){
    for i in {1..50}; do
        echo $i 1>&2
        badplayer | python3.12 play.py | grep "Ha ha ha I won!"&
        badplayer | python3.12 play.py | grep "Ha ha ha I won!"&
        wait
    done
}

function badplayer(){
    var="bw"
    echo "${var:$(( RANDOM % ${#var} )):1}"
    while true; do
        echo $((1 + $RANDOM % 8))$((1 + $RANDOM % 8));
    done
}

run | wc -l
