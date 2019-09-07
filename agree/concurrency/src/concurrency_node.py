from lib.partition import partition


# todo encapsulate these functions in a class, use member vars instead of passing args
def get_concurrency_tests(num, args_list, output_prefix, total_time_name):
    all_arrangements = arg_arrangements(num, args_list)

    arrangements_for_workers_required = dict()

    for arr in all_arrangements:
        size = len(arr)
        if size in arrangements_for_workers_required:
            arrangements_for_workers_required[size].append(arr)
        else:
            arrangements_for_workers_required[size] = [arr]

    result = ""

    for num_workers, arrangements_for_num_workers in arrangements_for_workers_required.items():
        result += "\t" + output_prefix + str(num_workers) + " = "
        check_time_all_arrangements = []
        for workers_tasks in arrangements_for_num_workers:
            check_time_all_workers = []
            for tasks_for_single_worker in workers_tasks:
                check_time_single_worker = "(" + " + ".join(tasks_for_single_worker) + ") < " + total_time_name
                check_time_all_workers.append(check_time_single_worker)
            single_dist_of_tasks = "(" + " and ".join(check_time_all_workers) + ")"
            check_time_all_arrangements.append(single_dist_of_tasks)
        result += "\n\t or ".join(check_time_all_arrangements)
        result += ";\n"

    return result


def arg_arrangements(num, args_list):
    arrangements = list(partition(list(range(num))))

    for arr in arrangements:
        for part in arr:
            for index, num in enumerate(part):
                if type(num) is int:  # should always happen but oh well
                    part[index] = args_list[num]

    return arrangements


def main(num):
    output_prefix = "can_use_"
    args_list = [f"t{x}" for x in range(num)]
    returns_list = [f"{output_prefix}{x}" for x in range(1, num + 1)]
    total_time_name = "totalTime"

    string_args = ", ".join([f"{x}: real" for x in args_list]) + f", {total_time_name}: real"
    string_returns = ", ".join([f"{x}: bool" for x in returns_list])

    string_equations = get_concurrency_tests(num, args_list, output_prefix, total_time_name)

    print(f"""
node concurrencyFactor({string_args})
\treturns({string_returns});
let
{string_equations}
tel;
""")


if __name__ == "__main__":
    main(3)
