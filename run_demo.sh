#!/bin/bash
#### Description: Generate accuracy graphs
#### Written by: Jakub Kopal email: kopal.jakub@gmail.com


usage(){
    echo "Usage: ./run_demo [-n test number]"
    echo "Generate comparision amoung: "
    echo "  n = 1: Original and retrained Mobilenets. "
    echo "  n = 2: Various number of frozen layers. "
    echo "  n = 3: Various input resolutions."
    echo "  n = 4: Various backbones (Mobilent V1, Mobilent V2, Inception)."
    echo "  n = 5: day-night-day_and_night models."
    echo "Example: ./run_demo -n 2"
    exit 1
}


# Parse arguments
if [ "$1" = "" ]; then usage; fi
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            GRAPH_NUM="$1"
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done



rm -f /tmp/results.txt
cd scripts

#Generate relults
case ${GRAPH_NUM} in
        1)
            declare -a arr=("voc" "detrac" "day")
            for i in "${arr[@]}"; do
                ./main.sh -n mobilenet_v1_origin -t "$i"
                ./main.sh -n mobilenet_v1_6_300 -t "$i"
                ./main.sh -n mobilenet_v2_origin -t "$i"
                ./main.sh -n mobilenet_v2_7_300 -t "$i"
            done
        ;;
        2)
            declare -a arr=("voc" "detrac" "day")
            for i in "${arr[@]}"; do
                ./main.sh -n mobilenet_v1_9_300 -t "$i"
                ./main.sh -n mobilenet_v1_6_300 -t "$i"
                ./main.sh -n mobilenet_v1_3_300 -t "$i"
                ./main.sh -n mobilenet_v1_0_300 -t "$i"
            done
        ;;
        3)
            declare -a arr=("detrac" "day")
            for i in "${arr[@]}"; do
                ./main.sh -n mobilenet_v2_7_300 -t "$i"
                ./main.sh -n mobilenet_v2_7_360 -t "$i"
                ./main.sh -n mobilenet_v2_7_420 -t "$i"
                ./main.sh -n mobilenet_v2_7_540 -t "$i"
            done
        ;;
        4)
            declare -a arr=("voc" "detrac" "day")
            for i in "${arr[@]}"; do
                ./main.sh -n mobilenet_v1_0_360 -t "$i"
                ./main.sh -n mobilenet_v2_0_360 -t "$i"
                ./main.sh -n inception_0_360 -t "$i"
            done
        ;;
        5)
            declare -a arr=("all" "day" "night")
            for i in "${arr[@]}"; do
                ./main.sh -n mobilenet_v1_6_300_all -t "$i"
                ./main.sh -n mobilenet_v1_6_300 -t "$i"
                ./main.sh -n mobilenet_v1_6_300_night -t "$i"
            done
        ;;
        *)
            usage
esac

# Draw Graph out of generated results
python draw_graph.py --graph_index ${GRAPH_NUM}
