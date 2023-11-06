function run(){
    for i in {1..100}; do
        badplayer | python3.12 play.py | grep "Ha ha ha I won!" &
    done

    wait
}

function badplayer(){
    var="bw"
    echo "${var:$(( RANDOM % ${#var} )):1}"
    while true; do
        echo $((1 + $RANDOM % 8))$((1 + $RANDOM % 8));
    done
}

run | wc -l
