from ospf import synchronize_routers

def get_topology_from_user():
    print("Enter the network topology as a list of [src, dst, cost] links:")
    print("Example: [[1, 2, 1], [2, 3, 2], [3, 4, 1], [1, 4, 4]]")

    try:
        user_input = input("Enter topology: ")
        topology = eval(user_input)
        if not isinstance(topology, list) or not all(isinstance(link, list) and len(link) == 3 for link in topology):
            raise ValueError("Invalid format")
        return topology
    except Exception as e:
        print(f"Invalid input: {e}")
        exit(1)

def main():
    topology = get_topology_from_user()
    routers = synchronize_routers(topology)

    for router in routers:
        router.calculate_dijkstras()

    print("\n==== Forwarding Tables ====")
    for router in routers:
        print(f"\nRouter {router.router_id} Forwarding Table:")
        table = router.generate_forwarding_table()
        for dest, next_hop, cost in table:
            print(f"  Dest: {dest}, Next Hop: {next_hop}, Cost: {cost}")

if __name__ == "__main__":
    main()
