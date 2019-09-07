# Let's make some AADL/AGREE!

```agree/concurrency/``` - This is where we generate the concurrency check. Given n threads, generate the agree node
function which takes the times of n jobs and determines, from m=0 to n, if m workers can accomplish the tasks in
the given time t.

```agree/linearization/``` - This is where we generate the linearized version of (ideally) any function!
