import json
import openproblems
import openproblems.test.utils


def evaluate_method(task, adata, method):
    output = openproblems.tools.decorators.profile(method)(adata)
    result = {
        "metrics": dict(),
    }
    for metric in task.METRICS:
        result["metrics"][metric.__name__] = metric(adata)

    del adata
    result["method"] = method.metadata["method_name"]
    result["paper_name"] = method.metadata["paper_name"]
    result["paper_url"] = method.metadata["paper_url"]
    result["paper_year"] = method.metadata["paper_year"]
    result["code_url"] = method.metadata["code_url"]
    result["memory_mb"] = output["memory_mb"]
    result["memory_leaked_mb"] = output["memory_leaked_mb"]
    result["runtime_s"] = output["runtime_s"]
    return result


def evaluate_dataset(task, dataset):
    adata = dataset(test=True)
    result = []
    for method in task.METHODS:
        r = evaluate_method(task, adata.copy(), method)
        with open(
            "../website/data/results/{}/{}.json".format(
                task.__name__.split(".")[-1], dataset.__name__
            ),
            "w",
        ) as handle:
            json.dump(r, handle)
        result.append(r)

    del adata
    return result


def evaluate_task(task):
    result = dict()
    for dataset in task.DATASETS:
        result[dataset.__name__] = evaluate_dataset(task, dataset)

    return result


def main():
    openproblems.test.utils.ignore_numba_warnings()

    results = dict()
    for task in openproblems.TASKS:
        task_name = task.__name__.split(".")[-1]
        result = evaluate_task(task).sort_values(["dataset", "metric", "value"])
        results[task_name] = result

    with open("../results.json", "w") as handle:
        json.dump(results, handle)
    return results


if __name__ == "__main__":
    main()
