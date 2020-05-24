#!/bin/bash


# 1. parse parameters
# a) model name/path b) all/day/night "c") resolution (this is parsed from .log)
usage(){
    echo "Usage: sysinfo_page [[-n name of model ], [-t type of new dataset {all, day, night, voc, fold_<num>]]"
    exit
}


MODELS_ROOT_DIR="${PROJECT_ROOT}/training/output"
TYPE="all"

# 0. parse arguments
if [ "$1" = "" ]; then usage; fi
while [ "$1" != "" ]; do
    case $1 in
        -n | --name )           
            shift
            MODEL_NAME="$1"
            MODEL_DIR="../models/$1/model"
            if [ ! -d "${MODEL_DIR}" ]; then
                echo "Folder ${MODEL_DIR} doesn't exist."
                exit
            fi
            ;;
        # test type
        -t | --type ) 
            shift 
            DATASET_NAME="$1"
            if [ "$1" != "all" ] && [ "$1" != "day" ] && [ "$1" != "night" ] && [ "$1" != "voc" ] && [ "$1" != "detrac" ] && [ "$1" != "train" ] && [[ $1 != fold_* ]]; then
                usage
            fi  
            TYPE=$1
            ;;
        -h | --help )           
            usage
            ;;
        * )                     
            usage
    esac
    shift
done


# 1. set variables
ORIGIN=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "origin:" | sed "s/[a-z]*://g" | sed 's/ //g')
HEIGHT=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "height:" | sed "s/[a-z]*://g")
WIDTH=$(cat "${MODEL_DIR}/output_tflite_graph_edgetpu.log" | grep "width:" | sed "s/[a-z]*://g")


# Create testing directory path 
if [ "${TYPE}" == "voc" ]; then
    TESTING_DIR=$(echo "../datasets/voc_${WIDTH}x${HEIGHT}" | sed 's/ //g')
elif [ "${TYPE}" == "detrac" ]; then
    TESTING_DIR=$(echo "../datasets/detrac_${WIDTH}x${HEIGHT}" | sed 's/ //g')
# elif [ "${TYPE}" == "train" ]; then
#     TESTING_DIR=$(echo "${LOCAL_GIT}/testing/exported/train_${WIDTH}x${HEIGHT}" | sed 's/ //g')
#     #2. generate groung truth
#     if [ -d "${TESTING_DIR}" ]; then 
#         echo 'Ground truth already exist'
#     else
#         echo 'Generating new ground truth testing set'
#         python generate_ground_truth.py --type ${TYPE} --width ${WIDTH} --height ${HEIGHT}
#     fi
# elif [[ ${TYPE} == fold_* ]]; then
#     TESTING_DIR=$(echo "${LOCAL_GIT}/testing/exported/${TYPE}_${WIDTH}x${HEIGHT}" | sed 's/ //g')
#     #2. generate groung truth
#     if [ -d "${TESTING_DIR}" ]; then 
#         echo 'Ground truth already exist'
#     else
#         echo 'Generating new ground truth testing set'
#         python generate_ground_truth.py --type ${TYPE} --width ${WIDTH} --height ${HEIGHT} --fold ${TYPE}
#     fi
else
    TESTING_DIR=$(echo "../datasets/${TYPE}_${WIDTH}x${HEIGHT}" | sed 's/ //g')
fi


# 2. generate model results
echo "Generating results for model: ${MODEL_NAME} on dataset: ${DATASET_NAME}"
python generate_model_results.py \
    --model_path="${MODEL_DIR}/output_tflite_graph_edgetpu.tflite" \
    --testing_data="${TESTING_DIR}" \
    --origin="${ORIGIN}"



# 3. evaluate model results
python evaluate_results.py \
    --ground_truth="${TESTING_DIR}"


rm -rf "model_detection_txts"

rm -rf ".temp_files"
rm -rf "output"
rm -rf "results"




