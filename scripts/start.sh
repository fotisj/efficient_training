export CUDA_VISIBLE_DEVICES=0 &
python3 crossvalidation.py crossval.json &
export CUDA_VISIBLE_DEVICES=1 &
python3 crossvalidation.py crossval_1.json &
export CUDA_VISIBLE_DEVICES=2 &
python3 crossvalidation.py crossval_2.json 