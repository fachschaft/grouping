#! /usr/bin/env python3

import os
import sys
import random
import argparse
import itertools

from pymustache import mustache


def random_group_index_gen(group_count):
    while True:
        random_group_indices = random.sample(range(group_count), group_count)
        for ind in random_group_indices:
            yield ind

def random_group_indices(group_count, num, seed):
    random.seed(seed)
    return tuple(itertools.islice(random_group_index_gen(group_count), num))


def player_groups(player_names, group_counts, group_names, seed):
    n_players = len(player_names)
    games = [random_group_indices(count, n_players, seed+ind)
             for ind, count in enumerate(group_counts)]
    player_groups = [[group_names[groups[player_ind]]
                      for groups in games]
                     for player_ind in range(n_players)]
    return list(zip(player_names, player_groups))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group-count",
                        nargs="+",
                        type=int,
                        help="number of players in group. pass multiple for multiple games.")
    parser.add_argument("-p", "--player-name",
                        nargs="+",
                        help="name of players instead of read from stdin.")
    parser.add_argument("-n", "--player-count",
                        type=int,
                        help="number of players even without player names.")
    parser.add_argument("-l", "--group-name",
                        nargs="+",
                        help="name of groups.")
    parser.add_argument("-G", "--game-name",
                        nargs="+",
                        help="name of games.")
    parser.add_argument("--seed",
                        type=int,
                        default=210591,
                        help="seed for group shuffling.")
    parser.add_argument("-t", "--to",
                        default="plain",
                        help="export format. uses template <template>.<format>.")
    parser.add_argument("--template",
                        default="default",
                        help="template name. uses template <template>.<format>.")
    parser.add_argument("--template-dir",
                        help="directory of template files. defaults to 'templates' folder in project directory.")
    parser.add_argument("-o", "--output",
                        help="Write output to FILE instead of stdout.")
    return parser.parse_args()


def game_groups_from_players(players):
    assert len(players) > 0, "requires at least one player"

    games = [{} for i in players[0][1]]
    for game_index, game_groups in enumerate(games):
        for player_name, player_groups in players:
            group_name = player_groups[game_index]
            if group_name in game_groups.keys():
                game_groups[group_name].append(player_name)
            else:
                game_groups[group_name] = [player_name]
    return games


def render(template_path, player_groups, game_names):
    game_groups = game_groups_from_players(player_groups)
    context = {'player': [{'name': pname,
                           'group': [{'name': gname}
                                     for gname in groups]}
                          for pname, groups in player_groups],
               'game': [{'name': game_name,
                         'group': [{'name': group_name,
                                    'player': [{'name': player_name}
                                               for player_name in players]}
                                   for group_name, players in sorted(groups.items())]}
                        for game_name, groups in zip(game_names, game_groups)]}

    mustache.filters['len'] = lambda list_in: len(list_in)
    mustache.filters['addone'] = lambda x: x + 1
    with open(template_path, 'r') as f:
        template = f.read()
        out = mustache.render(template, context)
    return out


def main():
    args = parse_args()

    player_names = args.player_name
    player_count = args.player_count
    if player_names is None:
        player_names = []
    elif len(player_names) == 1 and '-' in player_names :
        player_names = [line.rstrip() for line in sys.stdin]
    if player_count is not None:
        player_names += ['' for i in range(len(player_names), max(len(player_names), player_count))]

    group_counts = args.group_count
    group_names = args.group_name
    if group_names is None:
        group_names = []
    group_names = ['Group {}'.format(i+1) for i in range(len(group_names), max(group_counts))]

    game_count = len(group_counts)
    game_names = args.game_name
    if game_names is None:
        game_names = []
    game_names += ['Game {}'.format(i+1) for i in range(len(game_names), game_count)]

    template_dir = args.template_dir
    if template_dir is None:
        template_dir = os.path.join(os.path.dirname(__file__),'templates')
    template_path = os.path.join(template_dir, '{}.{}'.format(args.template, args.to))

    player_group_list = player_groups(player_names, group_counts, group_names, args.seed)
    out = render(template_path, player_group_list, game_names)
    if args.output is None:
       print(out)
    else:
        with open(args.output, 'w') as f:
            f.write(out)


if __name__ == '__main__':
    main()
