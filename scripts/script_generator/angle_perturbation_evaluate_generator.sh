python scripts/generate_angle_perturbation_evaluation_script.py --testpaths configs/angle_perturbation/TotalSegmentor-hips-DRR-full_test.csv   --gpu 0 --batch_size 8 --img_size 128 --res 2.25 --tags dropout model-compare dropout> bash_scripts/evaluate/angle_perturbation/evaluate_hips.sh 