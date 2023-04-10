import ping3
import requests
import datetime


SERVERS_LIST_URL = "https://api.mullvad.net/www/relays/all/"
results = []


def get_server_list():
    """Get the list of servers from the Mullvad API."""
    response = requests.get(SERVERS_LIST_URL)
    response.raise_for_status()
    return response.json()


def ping_server(server_json):
    """Ping a server and return the result."""
    ping_ms = ping3.ping(server_json["ipv4_addr_in"], unit="ms")

    if ping_ms is None:
        print(f"{server_json['hostname']}: timed out")
    elif ping_ms is False:
        print(f"{server_json['hostname']}: host unreachable")
    else:
        print(f"{server_json['hostname']}: {round(ping_ms)} ms")
        results.append((server_json, ping_ms))


def ping_servers(servers):
    """Ping all servers in the list."""
    for server in servers:
        ping_server(server)

    return results


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    servers_json = get_server_list()
    result = ping_servers(servers_json)
    # Print 10 fastest servers
    print("\n10 fastest servers:")
    for name, ping in result[:10]:
        print(f"{name['country_name']} - {name['city_name']} - {name['hostname']}: {round(ping)} ms")
    print(f"Time elapsed: {datetime.datetime.now() - start_time}")
