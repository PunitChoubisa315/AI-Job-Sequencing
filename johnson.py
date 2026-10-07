def johnsons_rule(job_times):

    remaining = {job: times.copy() for job, times in job_times.items()}

    n = len(remaining)

    sequence = [None] * n

    front = 0
    back = n - 1

    while remaining:

        min_job = None
        min_machine = None
        min_value = None

        for job, times in remaining.items():

            for machine in ("M1", "M2"):

                value = times[machine]

                if min_value is None or value < min_value:
                    min_value = value
                    min_job = job
                    min_machine = machine

        if min_machine == "M1":
            sequence[front] = min_job
            front += 1
        else:
            sequence[back] = min_job
            back -= 1

        del remaining[min_job]

    return sequence


def calculate_schedule(sequence, job_times):

    rows = []

    m1_time = 0
    m2_time = 0

    for job in sequence:

        m1_start = m1_time
        m1_finish = m1_start + job_times[job]["M1"]

        m2_start = max(m1_finish, m2_time)
        m2_finish = m2_start + job_times[job]["M2"]

        rows.append({
            "Job": job,
            "M1 In": m1_start,
            "M1 Out": m1_finish,
            "M2 In": m2_start,
            "M2 Out": m2_finish
        })

        m1_time = m1_finish
        m2_time = m2_finish

    minimum_elapsed_time = m2_time

    # Machine 2 total available time - actual processing time
    total_m2_processing = sum(
        job_times[job]["M2"] for job in sequence
    )

    machine_2_idle = minimum_elapsed_time - total_m2_processing

    return rows, minimum_elapsed_time, machine_2_idle
