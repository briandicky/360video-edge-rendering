using CP;

// Datadeclarations
int N = ...;            // no. of HMD clients
range n = 1..N;

int T = ...;            // no. of tiles
int V[n] = ...;         // tiles fallen in viewport
range v = 1..T;

float B = ...;          // outbound bandwidth

float bh = ...;         // high bitrate 
float bl = ...;         // low bitrate
float qt[n] = ...;      // video quality with high bitrate
float qv[n] = ...;      // video quality with low bitrate
int E = ...;            // max no. of client that egde can serve

// Decision variables
dvar boolean x[n];

// Objective
maximize
   1/N*sum(nid in n) (x[nid]*(qv[nid] - qt[nid]));

// Constraints
subject to{
    ct1:{
        sum(nid in n) (x[nid]) <= E;
    }
    ct2:{
        sum(nid in n) (x[nid]*V[nid]*bh + (1-x[nid])*(V[nid]*bh + (T-V[nid]*bl))) <= B;
    }
}

// Execute
execute{
f = new IloOplOutputFile("plan.txt");
for (var nid in n){
    write("n:"+nid+": "+x[nid]+"\n");
}
}
