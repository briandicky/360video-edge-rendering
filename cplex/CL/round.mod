using CP;
//Datadeclarations
int T = ...;
int K = ...;
range t = 1..T;
range k = 1..K;
float d1 [t] = ...;
float d2 [t][k] = ...;
float r1 [t] = ...;
float r2 [t][k] = ...;

//Decision variables
dvar boolean y[t][k];

// Objective
minimize
	sum(tid in t, kid in k) (d2[tid][kid]*y[tid][kid]-d1[tid]);
// Constraints
subject to{
	ct1:{
		sum(tid in t, kid in k) (r2[tid][kid]-r1[tid])*y[tid][kid] <= 0;
	}
	ct2:{
		forall(tid in t){
			sum(kid in k) y[tid][kid] == 1;
		}
	}
}
// Execute
execute{
f = new IloOplOutputFile("plan.txt");
for (var tid in t){
	for (var kid in k){
		write("t:"+tid+",k:"+kid+":"+y[tid][kid]+"\n");
	}
}
}
