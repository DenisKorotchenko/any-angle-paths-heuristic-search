# Any-angle path planning on grid graphs
## Description
This software project was made at St. Petersburg University during project working in Heuristic Algorithms course.

When speaking about path planning on grids, we usually want to simplify task with using some models: for example we can 
limit the number of directions of moves to 4 or 8 etc. and then use one of well-known approaches, for example A* algorithm.

However, when we simplify the model, we have to sacrifice something. In the example above we will find non-optimal
paths. But we can regulate suboptimality coefficient with the number of directions.

This approach is called 2^k A*. You can read more about it in [1]. You can find our implementation in ...

Other non-optimal but simple and quite effective algorithm is Theta*. 
It's based on the idea of smoothing paths during search.
In this algorithm we try to smooth path from current vertex to parent vertex of our parent and
reduce the path due to this. You can read more in [2].

But the most interesting of the implemented algorithms is ANYA. It is based on A* but it uses another type of nodes: here the node consists of root and an interval visible from it.
This algorithm is optimal and fast enough, but doesn't have such a simple implementation. 
You can read more about this algorithm in [3].


## Installing and guide for using
You can download this project with
```bash
git clone https://github.com/DenisKorotchenko/any-angle-paths-heuristic-search
```
Then you open ```example.ipynb``` to see examples with some maps from movingai. 

You can also find path for you personal map. For it you need to have a 

## Inputs and outputs
Our algorithm works with ```movingai``` format, you can read more about it here [].
The output can be represented in graphics or as a succession of vertexes from the start to the target. 

## Sources
[1] Rivera, N., Hernández, C., Hormazábal, N. and Baier, J.A., 2020. The 2^k Neighborhoods for Grid Path Planning. Journal of Artificial Intelligence Research, 67, pp.81-113.
[**Link**](https://www.jair.org/index.php/jair/article/view/11383)

[2] Daniel, K., Nash, A., Koenig, S. and Felner, A., 2010. Theta*: Any-angle path planning on grids. Journal of Artificial Intelligence Research, 39, pp.533-579.
[**Link**](https://www.jair.org/index.php/jair/article/view/10676)

[3] Harabor, D.D., Grastien, A., Öz, D. and Aksakalli, V., 2016. Optimal any-angle pathfinding in practice. Journal of Artificial Intelligence Research, 56, pp.89-118.
[**Link**](https://www.researchgate.net/publication/305175423_Optimal_Any-Angle_Pathfinding_In_Practice)
