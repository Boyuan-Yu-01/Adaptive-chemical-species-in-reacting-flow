## Graph Type##

- __Heterogeneous Graphs__: nods are also imbued with types.
![het](heterogeneous.jpg)
			*example of heterogeneous graph: nodes have different entities*
			
- __Multiplex Graphs__: graph can be decomposed  in a  set of k layers, and each layer corresponds  to a unique relation.
![mult](multiplex.jpg)
	*example of multiplex graph: take plane from $\alpha$ to $\beta$, then take train  from  $\beta$ to $\gamma$*

##  What Can  We  Do  With  GNN?
__In machine learning,  supervised machine learning in GNN  has examples  such as predict target output given input; unsupervised machine  learning  in  GNN  has example  of inferring patterns.__
- ==Node classification==
	- difficult:  nodes in a graph  are  not  independent  and  identically distributed (i.i.d)
	- key insights:  homophily,  structural equivalence, and heterophily
- ==Relation  Prediction==
	- infer the edges between  nodes in  a graph
![relation](relationPredict.png)
- ==Clustering and  Community Detection==
- ==Graph  Classification, Regression , and Clustering==

##  Graph  Statistics ##
###  Node-Level Statistics ###
- Node Degree: $d_u = \sum_{v \in V} A[u, v]$
- Node centrality: e_u = $\frac{1}{\lambda} \sum_{v \in V} A[u, v] e_v, \quad \forall u \in V$
- Clustering Coefficient: 

where $A$ is the adjacency matrix, $e_v$ is eigenvectors  of the matrix, $\lambda$ is the eigenvalue 
