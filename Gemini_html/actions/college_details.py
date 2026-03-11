def college_action(parameters: dict, player=None) -> str:
    """
    Returns hardcoded information about Rajiv Gandhi Institute of Technology (RIT), Kottayam.
    """
    if player:
        player.write_log("SYS: Accessing RIT Kottayam campus database...")

    info = parameters.get("info_type", "general").lower()

    if "course" in info or "department" in info:
        return (
            "RIT Kottayam offers B.Tech programs in Civil, Mechanical, Electrical & Electronics, "
            "Electronics & Communication, and Computer Science Engineering. It also offers B.Arch, "
            "various M.Tech programs, and MCA."
        )
    elif "history" in info or "about" in info:
        return (
            "Rajiv Gandhi Institute of Technology (RIT) is one of the premier engineering colleges in Kerala, "
            "established in 1991 by the Government of Kerala. It is affiliated with APJ Abdul Kalam Technological University."
        )
    elif "facility" in info or "facilities" in info:
        return (
            "The RIT campus spans over 87 acres and features advanced laboratories, a central library, "
            "hostels for boys and girls, sports facilities including a stadium, and a serene, green campus environment."
        )
    else:
        return (
            "Rajiv Gandhi Institute of Technology (RIT), Kottayam, is a premier government engineering college "
            "in Kerala offering B.Tech, M.Tech, MCA, and B.Arch programs. Let me know if you need details on "
            "courses, history, or facilities."
        )
