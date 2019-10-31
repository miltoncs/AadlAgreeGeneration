from lib.partition import partition

class ConcurrencyFactorNode:
    def __init__(self, num):

        output_prefix = "can_use_"
        args_list = [f"t{x}" for x in range(num)]
        returns_list = [f"{output_prefix}{x}" for x in range(1, num + 1)]
        total_time_name = "totalTime"

        string_args = ", ".join([f"{x}: real" for x in args_list]) + f", {total_time_name}: real"
        string_returns = ", ".join([f"{x}: bool" for x in returns_list])

        self.num = num
        self.output_prefix = output_prefix
        self.args_list = args_list
        self.total_time_name = total_time_name
        self.string_args = string_args
        self.string_returns = string_returns
        self.string_equations = self.get_concurrency_tests()

    def __str__(self):
        return f"""
node concurrencyFactor({self.string_args})
\treturns({self.string_returns});
let
{self.string_equations}
tel;
"""

    def get_concurrency_tests(self):
        all_arrangements = self.arg_arrangements()

        arrangements_for_workers_required = dict()

        for arr in all_arrangements:
            size = len(arr)
            if size in arrangements_for_workers_required:
                arrangements_for_workers_required[size].append(arr)
            else:
                arrangements_for_workers_required[size] = [arr]

        result = ""

        for num_workers, arrangements_for_num_workers in arrangements_for_workers_required.items():
            result += "\t" + self.output_prefix + str(num_workers) + " = "
            check_time_all_arrangements = []
            for workers_tasks in arrangements_for_num_workers:
                check_time_all_workers = []
                for tasks_for_single_worker in workers_tasks:
                    check_time_single_worker = "(" + " + ".join(tasks_for_single_worker) + ") < " + self.total_time_name
                    check_time_all_workers.append(check_time_single_worker)
                single_dist_of_tasks = "(" + " and ".join(check_time_all_workers) + ")"
                check_time_all_arrangements.append(single_dist_of_tasks)
            result += "\n\t or ".join(check_time_all_arrangements)
            result += ";\n"
        return result
        

    def arg_arrangements(self):
        arrangements = list(partition(list(range(self.num))))

        for arr in arrangements:
            for part in arr:
                for index, num in enumerate(part):
                    if type(num) is int:
                        part[index] = self.args_list[num]

        return arrangements

if __name__ == "__main__":
    agreeNode = ConcurrencyFactorNode(3)
    print(agreeNode)
