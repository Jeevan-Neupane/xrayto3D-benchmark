python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name OneDConcat --ckpt_path runs/2d-3d-benchmark/hw4es5nw/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/hw4es5nw/checkpoints/../evaluation

python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name MultiScale2DPermuteConcat --ckpt_path runs/2d-3d-benchmark/dnnwydzk/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/dnnwydzk/checkpoints/../evaluation

python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name TwoDPermuteConcat --ckpt_path runs/2d-3d-benchmark/y8kln4px/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/y8kln4px/checkpoints/../evaluation

python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name AttentionUnet --ckpt_path runs/2d-3d-benchmark/yiw2kgep/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/yiw2kgep/checkpoints/../evaluation

python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name UNet --ckpt_path runs/2d-3d-benchmark/ktkdfd5v/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/ktkdfd5v/checkpoints/../evaluation

python evaluate.py  --testpaths configs/paths/totalsegmentator_hips/TotalSegmentor-hips-DRR-full_test.csv --gpu 0 --image_size 128 --batch_size 8 --accelerator gpu --res 2.25 --model_name UNETR --ckpt_path runs/2d-3d-benchmark/762ji1eb/checkpoints --gpu 0 --output_path runs/2d-3d-benchmark/762ji1eb/checkpoints/../evaluation

