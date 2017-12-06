#
# Do automated tests on models, iterating over different combinations of
# parameters.
#

import csv
import itertools
import numpy

try:
    # Python 2
    str_types = (str, numpy.unicode)
except NameError:
    # Python 3
    str_types = (bytes, str)


def get_measurement(model, attr):
    """Returns the value of a given measurement attribute for a given model.

    A measurement attribute can be one of the following things:
     * A string representing an attribute of the model, which can either be:
      - a variable (not callable)
      - a method (callable)
     * A function which is a method of the model (will be called without args)
     * A normal function (or lambda, any callable), which will receive the
       simulation instance as argument."""

    if callable(attr):
        # If the passed callable is a method of the model we
        # call it directly, otherwise we also pass the model as
        # argument to the function.
        if hasattr(model, attr.__name__) and \
                        getattr(model, attr.__name__) == attr:
            return attr()
        else:
            return attr(model)
    elif isinstance(attr, str_types):
        m = getattr(model, attr)
        if callable(m):
            m = m()
        return m


def param_sweep(model, repetitions, param_space, measure_attrs, max_iter=0, csv_base_filename=None, measure_interval=1):
    """Performs a parameter sweep over Model instance `model', setting the
    parameters defined in the dictionary `param_space', each combination
    `repetitions' times, and outputs all measurements as defined by
    `measure_attrs' to a csv file.

    Measurements are returned as an array with index 0 containing all
    measurements for measure_attrs[0], etc. Inside there is an array of runs.
    The number of items in this array will be equal to the number of different
    combinations for the param_space times the number of repetitions per set of
    params. Finally, every entry in this array is an array of the length of the
    number of iterations that specific executions ran for (with as value the
    measurement for that iterations).

    Optionally, the frequency of the measurements can be set using the
    `measure_interval' parameter.. By default this value is 1, and thus every
    iteration a measurement is made. For a value of 5, measurements are recorded
    iteration 0, 5, 10, etc. If this parameter is set to 0, a measurement will
    only be recorded at the end of a run.

    The way this is written to csv is similar: for every measurement a separate
    csv file is created (e.g. "%s_%d.csv" % (csv_base_filename, measurement) for
    every measurement). In this file every row contains a single executions (and
    thus per column the iterations). Note that the first columns will contain
    the parameter values and the repetition number.

        >>> from some_sim import Sim
        >>> mysim = Sim()
        >>> paramsweep(mysim, 3,
        ...     {'width': [50, 100],
        ...      'height': 60,
        ...      'turtles': range(10)},
        ...     ['iterations',
        ...      (lambda sim: sim.iterations / sim.turtle_count)])"""

    accepted_iterables = (list, tuple, numpy.ndarray)

    param_list = list(param_space.items())
    param_names = [i[0] for i in param_list]
    param_values = (i[1] if isinstance(i[1], accepted_iterables) else (i[1],)
                    for i in param_list)

    combinations = tuple(itertools.product(*param_values))
    measurements = [[] for a in measure_attrs]
    # Iterate over all combinations of parameter values
    for vals in combinations:
        # Set current parameter values to the model
        for pn, pv in zip(param_names, vals):
            if pn not in model.params:
                raise ValueError(("param '%s' not a parameter of model (known "
                                  "params: %s)") % (pn, ', '.join(model.params)))
            setattr(model, pn, pv)

        # Perform simulations requested amount of times with current params.
        for r in range(repetitions):
            model.reset()
            current_iter = 0
            if measure_interval:
                for m, attr in zip(measurements, measure_attrs):
                    m.append([get_measurement(model, attr)])
            # Run the model (recording measurements) until model indicates
            # simulation has finished or we reach the max number of iters.
            while model.step() is not True and \
                    (not max_iter or current_iter < max_iter):
                current_iter += 1
                if measure_interval and current_iter % measure_interval == 0:
                    for i, attr in enumerate(measure_attrs):
                        m = get_measurement(model, attr)
                        measurements[i][-1].append(m)
            if not measure_interval:
                for m, attr in zip(measurements, measure_attrs):
                    m.append([get_measurement(model, attr)])

    if csv_base_filename is not None:
        # Dump results to csv files: one per measurement, row per run
        for i, m in enumerate(measurements):
            with open('%s_%d.csv' % (csv_base_filename, i), 'w') as f:
                writer = csv.writer(f)
                writer.writerow(param_names + ["rep_num"])
                for j, n in enumerate(m):
                    params = combinations[j // repetitions]
                    rep = j % repetitions
                    writer.writerow(list(params) + [rep, None] + n)

    return measurements
