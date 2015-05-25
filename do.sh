mkdir all
mkdir all-utf
cp *.csv all/
cp *.csv all-utf/
nkf -w --overwrite all-utf/*
python eval.py
