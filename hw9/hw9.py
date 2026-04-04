# the 7 coins in the assignment didnt have the api working (cardano/ada). So i found the top 7 coins currently
# that the api worked for and did those 7. 

import requests
import networkx as nx


def get_graph():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple,binancecoin,solana,bitcoin-cash,chainlink&vs_currencies=btc,eth,xrp,bnb,sol,bch,link"
    data = requests.get(url).json()

    coin_map = {
        "bitcoin": "btc",
        "ethereum": "eth",
        "ripple": "xrp",
        "binancecoin": "bnb",
        "solana": "sol",
        "bitcoin-cash": "bch",
        "chainlink": "link"
    }

    graph = nx.DiGraph()

    for coin_name in data:
        from_ticker = coin_map[coin_name]

        for to_ticker in data[coin_name]:
            weight = data[coin_name][to_ticker]

            if weight is not None:
                graph.add_edge(from_ticker, to_ticker, weight=weight)

    return graph


def get_path_weight(graph, path):
    weight = 1

    for i in range(len(path) - 1):
        weight *= graph[path[i]][path[i + 1]]["weight"]

    return weight


def main():
    graph = get_graph()
    coins = list(graph.nodes)

    smallest_factor = None
    greatest_factor = None
    smallest_paths = None
    greatest_paths = None

    for start_coin in coins:
        for end_coin in coins:
            if start_coin == end_coin:
                continue

            print(f"\npaths from {start_coin} to {end_coin} --------------------------")

            all_paths = list(nx.all_simple_paths(graph, start_coin, end_coin))

            if len(all_paths) == 0:
                print("No paths found.")
                continue

            for path in all_paths:
                reverse_path = list(reversed(path))

                valid_reverse = True
                for i in range(len(reverse_path) - 1):
                    if not graph.has_edge(reverse_path[i], reverse_path[i + 1]):
                        valid_reverse = False
                        break

                if not valid_reverse:
                    continue

                path_weight = get_path_weight(graph, path)
                reverse_weight = get_path_weight(graph, reverse_path)
                factor = path_weight * reverse_weight

                print(path, path_weight)
                print(reverse_path, reverse_weight)
                print(factor)
                print()

                if smallest_factor is None or factor < smallest_factor:
                    smallest_factor = factor
                    smallest_paths = (path, reverse_path)

                if greatest_factor is None or factor > greatest_factor:
                    greatest_factor = factor
                    greatest_paths = (path, reverse_path)

    print("Smallest Paths weight factor:", smallest_factor)
    print("Paths:", smallest_paths[0], smallest_paths[1])

    print("Greatest Paths weight factor:", greatest_factor)
    print("Paths:", greatest_paths[0], greatest_paths[1])


main()