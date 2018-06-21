using CP;
//Datadeclarations
int Cmax= ...;
int R = ...;
range r = 1..R;
int M = ...;
range m = 1..M;
int D = ...;
range d = 1..D;

int RDmat [r][d] = ...;
int RMnum [r]= ...;

//Decision variables
dvar boolean x[r][m][d];

//Objectice
maximize
	sum(rid in r) (prod(mid in 1..RMnum[rid]) minl(sum(did in d)(x[rid][mid][did]*RDmat[rid][did]),1));
//Constrains
subject to{
	ct1:{
		forall(did in d){
			sum(rid in r)sum(mid in m) x[rid][mid][did] <= Cmax;
		}
	}
	
	ct2:{
		forall(rid in r){
			forall(mid in m){
				sum(did in d) x[rid][mid][did] <= 1;
			}
		}
	}
}
//Excute
execute{
f = new IloOplOutputFile("plan.txt");
for (var rid in r){
	for (var mid in m){
		for (var did in d){
			write("r:"+rid+",m:"+mid+",d:"+did+":"+x[rid][mid][did]+"\n")
		}
	}
}

}
