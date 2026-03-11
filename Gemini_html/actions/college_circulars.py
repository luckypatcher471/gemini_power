def circulars_action(parameters: dict, player=None) -> str:
    """
    Returns a simulated list of the latest college circulars for RIT Kottayam.
    """
    if player:
        player.write_log("SYS: Fetching latest notices and circulars...")

    import datetime
    today = datetime.date.today()
    
    circulars = [
        f"[{today.strftime('%d-%b-%Y')}] IMPORTANT: TechFest 'Ktu-Tarang' registration deadline extended.",
        f"[{(today - datetime.timedelta(days=2)).strftime('%d-%b-%Y')}] Academic Schedule for Even Semester 2026 published.",
        f"[{(today - datetime.timedelta(days=5)).strftime('%d-%b-%Y')}] Notice regarding Hostel fee payment for the upcoming semester.",
        f"[{(today - datetime.timedelta(days=7)).strftime('%d-%b-%Y')}] Call for applications: Student Senate Elections 2026."
    ]

    return "Here are the latest college circulars:\n" + "\n".join(circulars)
