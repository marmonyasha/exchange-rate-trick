import random
import copy
import argparse

NAMES = list(
    ("золотых колец", "мандаринов", "стульев", "книг", "пачек жвачки", "самокатов"))
NAME_FOR_RINA = "золотого кольца"
# harcoded graph1
ADJACENCY_LISTS = {
    0: {2, 3, 4, 5},
    1: {2, 4, 5},
    2: {0, 1, 3},
    3: {0, 2},
    4: {0, 1},
    5: {0, 1}
}
PAIRS_LIST = [(0, 3), (1, 4), (2, 3), (0, 5), (1, 2), (0, 4), (1, 5), (0, 2)]
DEBUG_HEADER = "\n~~~~~~~~~~DEBUG~MODE~~~~~~~~~~"
DEBUG_FOOTER = "~~~~~~~~~~END~DEBUG~MODE~~~~~~~~~~"
RESULT_HEADER = "\n============RESULTS============"

assert (len(NAMES) == len(ADJACENCY_LISTS.keys()))


def get_pairs():
    pairs_set = set()
    for item_from in ADJACENCY_LISTS:
        for item_to in ADJACENCY_LISTS[item_from]:
            pairs_set.add(
                tuple((min(item_from, item_to), max(item_from, item_to))))
    return pairs_set


def get_pairs_list(pairs_set):
    return random.sample(list(pairs_set), len(pairs_set))


def ask_next_rate(pair):
    print("Сколько {} будем менять на сколько {}: ".format(NAMES[pair[0]].upper(),
                                                           NAMES[pair[1]].upper()),
          end='')
    while True:
        try:
            rate_0, rate_1 = [int(i) for i in input().split(' ')]
            assert ((rate_0 > 0) and (rate_1 > 0))
            break
        except (AssertionError, ValueError):
            print("Что-то пошло не так, пожалуйста, снова введите два "
                  "целых числа через пробел: ", end='')

    return rate_0, rate_1


def get_rates(dest, curr, prev, exchange_rates, curr_rate, rate_list, route):
    for item_to in ADJACENCY_LISTS[curr]:
        if curr in exchange_rates:
            if item_to in exchange_rates[curr]:
                rate = exchange_rates[curr][item_to]
            else:
                rate = 1 / exchange_rates[item_to][curr]
        else:
            rate = 1 / exchange_rates[item_to][curr]

        if item_to == dest:
            local_route = copy.deepcopy(route)
            local_route.append(curr)
            local_route.append(dest)
            rate_list.append(tuple((
                local_route,
                curr_rate * rate)))
        elif item_to == prev:
            continue
        else:
            local_route = copy.deepcopy(route)
            local_route.append(curr)
            get_rates(dest,
                      item_to,
                      curr,
                      exchange_rates,
                      curr_rate * rate,
                      rate_list,
                      local_route)


def print_debug_backtrace(rate_list):
    print(DEBUG_HEADER)
    for i in rate_list:
        print("{}\t{}".format(i[0], i[1]))
    print(DEBUG_FOOTER)


def print_result(rate_list):
    print(RESULT_HEADER)
    rates = [i[1] for i in rate_list]
    print("Меняясь по таким курсам, компьютер получил из 1 {0} "
          "{1} {2}".format(NAME_FOR_RINA, round(max(rates), 2), NAMES[0]))


def game(debug=False):
    # pairs_set = get_pairs()
    # pairs_list = get_pairs_list(pairs_set)

    pairs_list = PAIRS_LIST
    exchange_rates = dict()

    for pair in pairs_list:
        rate_0, rate_1 = ask_next_rate(pair)
        if pair[0] not in exchange_rates:
            exchange_rates[pair[0]] = dict()
        exchange_rates[pair[0]][pair[1]] = rate_1 / rate_0

    rate_list = list()
    route = list()
    get_rates(0, 0, 0, exchange_rates, 1, rate_list, route)

    if debug:
        print_debug_backtrace(rate_list)

    print_result(rate_list)


def main():
    parser = argparse.ArgumentParser(description='Make trick with user-given '
                                                 'exchange rates for '
                                                 'some things')
    parser.add_argument('-d', '--debug',
                        action="store_true",
                        help="add debug backtrace output")
    args = parser.parse_args()

    game(args.debug)


if __name__ == "__main__":
    main()
