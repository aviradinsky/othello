function run(){
    for i in {1..100}; do
        while true;
            do echo $((1 + $RANDOM % 8))$((1 + $RANDOM % 8)); 
        done | python3.12 play.py | grep "Ha ha ha I won!" &
    done

    wait
}

run | wc -l