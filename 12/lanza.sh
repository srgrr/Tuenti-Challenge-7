while true
do
  python interaction.py >> output.txt
  grep token output.txt
done
