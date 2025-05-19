from router import Router
from link import Link
from lsa import RouterLSA

INIT_SEQ_NUM = 0x80000001

def parse_router_ids(topology):
    router_ids = set()
    for src, dst, _ in topology:
        router_ids.add(src)
        router_ids.add(dst)
    return sorted(list(router_ids))

def synchronize_routers(network_topology):
    router_ids = parse_router_ids(network_topology)
    routers = {rid: Router(rid) for rid in router_ids}

    # Step 1: Inject direct LSAs into each router
    for src, dst, cost in network_topology:
        lsa = RouterLSA(Link(src, dst), INIT_SEQ_NUM, cost)
        routers[src].receive_lsa(lsa)
        routers[dst].receive_lsa(lsa)

    # Step 2: Flood LSAs until synchronized or iteration limit is reached
    MAX_ITER = 100
    for iteration in range(MAX_ITER):
        converged = True

        for rid in router_ids:
            router = routers[rid]
            advertised = router.advertise_database()

            for neighbor_id in router.neighbors():
                if neighbor_id not in routers:
                    continue

                neighbor = routers[neighbor_id]
                before = set(neighbor.advertise_database())
                neighbor.update_database(advertised)
                after = set(neighbor.advertise_database())

                if before != after:
                    converged = False  # LSDB changed — need more flooding

        if converged:
            return [routers[r] for r in router_ids]

    raise RuntimeError("OSPF LSDB synchronization failed after 100 iterations.")
