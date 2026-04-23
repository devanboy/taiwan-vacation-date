import urllib.request
import json
from datetime import datetime, timedelta


def taiwan_vacation_date(
    duration=365,
    extension_day=4,
    min_total_days=4,
    max_total_days=7
):
    """
    Generates an Nx3 matrix of vacation dates with leave day calculation.

    This function fetches Taiwan's official holiday calendar from ru.yu's
    open-source repository, identifies contiguous holiday blocks (連假), and
    generates all possible travel periods by extending before/after the block.
    For each period, it calculates the exact number of personal-leave days
    (working days) you would need to request.

    Parameters
    ----------
    duration : int, optional
        Search window in days from today. Default is 365.
    extension_day : int, optional
        Maximum total personal-leave days you are willing to extend
        (spread before + after the holiday block). Default is 4.
    min_total_days : int, optional
        Minimum trip length (inclusive). Default is 4.
    max_total_days : int, optional
        Maximum trip length (inclusive). Default is 7.

    Returns
    -------
    list[list[str, str, int]]
        Nx3 matrix where each row is::

            ["YYYY-MM-DD" (Departure), "YYYY-MM-DD" (Return), int (Leave Days)]

        Sorted chronologically by departure date.

    Examples
    --------
    >>> results = taiwan_vacation_date(duration=180, extension_day=2)
    >>> results[0]
    ['2026-02-14', '2026-02-22', 2]

    Notes
    -----
    - The calendar data is fetched from CDN (jsDelivr) backed by
      https://github.com/ruyut/TaiwanCalendar . A network connection is
      required for the first run of a new calendar year.
    - Weekend days (Sat/Sun) that are NOT marked as holidays in the calendar
      are treated as working days and therefore count toward leave days.
      This matches the strict interpretation of Taiwan labour law.
    - Duplicate (departure, return) pairs are automatically de-duplicated.
    """
    start_target = datetime.now()
    end_target = start_target + timedelta(days=duration)

    years = list({start_target.year, end_target.year})
    all_days_data = []

    # ── 1. Fetch calendar data ────────────────────────────────
    for y in sorted(years):
        url = (
            "https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/"
            f"{y}.json"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req) as response:
                all_days_data.extend(
                    json.loads(response.read().decode("utf-8"))
                )
        except Exception as e:
            print(
                f"Warning: Failed to fetch calendar data for {y}: {e}"
            )

    # ── 2. Build holiday set (isHoliday == True) ──────────────
    holiday_set = {
        day["date"]
        for day in all_days_data
        if day.get("isHoliday")
    }

    # ── 3. Identify holiday blocks (連假) ──────────────────────
    blocks = []
    current_block = []
    has_desc = False

    for day in all_days_data:
        day_date_obj = datetime.strptime(day["date"], "%Y%m%d")

        if day.get("isHoliday"):
            current_block.append(day_date_obj)
            if day.get("description"):
                has_desc = True
        else:
            if current_block and has_desc:
                if (
                    current_block[-1] >= start_target
                    and current_block[0] <= end_target
                ):
                    blocks.append(current_block)
            current_block = []
            has_desc = False

    # Trailing block
    if current_block and has_desc:
        if (
            current_block[-1] >= start_target
            and current_block[0] <= end_target
        ):
            blocks.append(current_block)

    # ── 4. Generate periods and calculate leave days ─────────
    valid_periods = []
    seen = set()

    for block in blocks:
        start_h = block[0]
        end_h = block[-1]

        for x in range(extension_day + 1):
            for y in range(extension_day + 1):
                if x + y <= extension_day:
                    dep_date = start_h - timedelta(days=x)
                    ret_date = end_h + timedelta(days=y)

                    total_days = (ret_date - dep_date).days + 1

                    if min_total_days <= total_days <= max_total_days:
                        dep_str = dep_date.strftime("%Y-%m-%d")
                        ret_str = ret_date.strftime("%Y-%m-%d")
                        identifier = f"{dep_str}_{ret_str}"

                        if identifier in seen:
                            continue

                        # Count working days (not in holiday_set)
                        leave_days = 0
                        curr = dep_date
                        while curr <= ret_date:
                            if curr.strftime("%Y%m%d") not in holiday_set:
                                leave_days += 1
                            curr += timedelta(days=1)

                        seen.add(identifier)
                        valid_periods.append([dep_str, ret_str, leave_days])

    # Sort by departure date for stable output
    valid_periods.sort(key=lambda r: r[0])
    return valid_periods


# ── Simple CLI when run directly ──────────────────────────────
if __name__ == "__main__":
    print("Taiwan Vacation Date Generator\n")
    print("Fetching calendar and computing optimal periods...\n")

    results = taiwan_vacation_date(
        duration=365,
        extension_day=4,
        min_total_days=4,
        max_total_days=7,
    )

    if not results:
        print("No vacation periods found for the given constraints.")
    else:
        print(f"{'Departure':<12} {'Return':<12} {'Leave Days':<12}")
        print("-" * 38)
        for dep, ret, leave in results:
            print(f"{dep:<12} {ret:<12} {leave:<12}")
