# Grouping

## What to do with this

As a student association we organize several games for freshmen.
The students have to be grouped for each of the games, where the number of groups can differ.
Usually some students are late or games are added. Then the existing grouping shouldn't change.
This is all we want and can do with this script.

## Preparation

You need *python 3* (we used version *3.6.2*) to run the script.
All further requirements can be installed with *pip 3* via 
```
pip3 install -r requirements.txt --user
```

Check whether installation was successful by printing all available options of the script.
```
python3 grouping.py --help
```


## Examples

1. randomly assign some students to two groups of a game.
```
$ python3 grouping.py --group-count 2 --player-name Tick Trick Track Donald Gustav
```

2. randomly assign a lot of students from a list to the groups of three games.
```
$ cat example/students.txt | python3 grouping.py --group-count 6 3 4 --player-name -
```

3. save the list as a pretty html file with custom group names and add some empty rows for latecomers.
```
$ cat example/students.txt |\
  python3 grouping.py --group-count 6 3 4 --group-name A B C D E F --player-name - -n 50 --to html -o groups.html
```

4. only print the very first student's groups via custom template. 
   Try some random sorting starts until he is two times in group 1 and then save the whole list.
```
$ echo 'First student's groups: {{#player.0.group}} {{name}} {{/player.0.group}}' > templates/first.plain 
$ python3 grouping.py --group-count 2 3 --player-name Tick Trick Track Donald Gustav --template first --seed 40
First students groups:  Group 2  Group 2 
$ python3 grouping.py --group-count 2 3 --player-name Tick Trick Track Donald Gustav --template first --seed 41
First students groups:  Group 2  Group 3 
$ python3 grouping.py --group-count 2 3 --player-name Tick Trick Track Donald Gustav --template first --seed 42
First students groups:  Group 1  Group 1 
$ python3 grouping.py --group-count 2 3 --player-name Tick Trick Track Donald Gustav --template default --seed 42 -o groups.txt
```

## License

This tool is developed by [David-Elias Künstle](https://github.com/dekuenstle) for the [student association technical faculty (Uni Freiburg)](https://fachschaft.tf) and published under the [EUPL 1.2](https://joinup.ec.europa.eu/page/eupl-text-11-12).
Therefore you are free to use, modify and copy this work. 
However copies and modifications have to be licensed under a compatible license and contain source code.

