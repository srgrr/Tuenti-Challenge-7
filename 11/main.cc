#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
const ll inf = 10000000000000000LL;


struct edge {
  int adj;
  string color;
};

struct vertex {
  map< string, int > energies;
  vector< edge > edges;
};



// debug
void print_colors(map< string, vector<string> >& colors) {
  for(auto kv : colors) {
    cout << kv.first << ":";
    for(string color : kv.second) cout << " " << color;
    cout << endl;
  }
  cout << "-----------------------" << endl;
}

vector< string > resolve_color(string color, map< string, vector<string> >& colors) {
  vector< string > ret;
  if(colors[color].empty()) return {color};
  for(string adj_color : colors[color]) {
    vector< string > recursive = resolve_color(adj_color, colors);
    for(string rec_obtained : recursive) {
      ret.push_back(rec_obtained);
    }
  }
  /*
    With this step we will guarantee that all vectors will have sizes of at
    most 10
  */
  sort(ret.begin(), ret.end());
  vector< string > ans = {ret[0]};
  for(int i=1; i<int(ret.size()); ++i) {
    if(ret[i] != ans.back()) {
      ans.push_back(ret[i]);
    }
  }
  return colors[color] = ans;
}

void resolve_colors(map< string, vector< string> >& colors) {
  for(auto kv : colors) {
    resolve_color(kv.first, colors);
  }
}



int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    /*
      Parse colors and express them as a combination of
      primary colors
    */
    map<string, int> primary2int;
    map<int, string> int2primary;
    int primary_count = 0;
    map<string, vector< string > > colors;
    int C;
    cin >> C;
    for(int i=0; i<C; ++i) {
      string x;
      cin >> x;
      int k;
      cin >> k;
      for(int j=0; j<k; ++j) {
        string y;
        cin >> y;
        colors[x].push_back(y);
      }
      if(k == 0) {
        colors[x] = {};
        int2primary[primary_count] = primary_count;
        primary2int[x] = primary_count;
        ++primary_count;
      }
    }
    //*
    for(int i=0; i<4*C; ++i)
    //*/
      resolve_colors(colors);
    cerr << "[ DEBUG ] : color resolution done!" << endl;
    /*
      Parse the graph
    */
    // Vertices
    int G;
    cin >> G;
    vector< vertex > g(G);
    for(int i=0; i<G; ++i) {
      int E;
      cin >> E;
      for(int j=0; j<E; ++j) {
        string energy_type;
        int amount;
        cin >> energy_type >> amount;
        g[i].energies[energy_type] = amount;
      }
    }
    cerr << "[ DEBUG ] : energies properly parsed!" << endl;
    // Edges
    int W;
    cin >> W;
    for(int i=0; i<W; ++i) {
      string color;
      int u, v;
      cin >> color >> u >> v;
      g[u].edges.push_back({v, color});
    }
    /*
      Now, let's apply a Dijkstra over the graph with vertices V x M,
      where M is the set of all binary strings of length primary_count
      (i.e: a bitmask that tells us what primary colors do we have on
      each vertex).
      We will start at vertex (0, 000...).

      Also, on each vertex we must explore all the possibilities about
      taking a given color or not (and its cost).
      We can implement this as weighted edges between the same vertex
      but with different masks
    */
    //*
    vector< vector<ll> > dist(G, vector<ll>(1<<primary_count, inf));
    cerr << "[ DEBUG ] : dist properly alloc'd!" << endl;
    dist[0][0] = 0;
    typedef pair<ll, pair<int, int> > thing;
    priority_queue<thing, vector<thing>, greater<thing> > Q;
    Q.push({0, {0, 0}});
    while(!Q.empty()) {
      int v = Q.top().second.first;
      int mask = Q.top().second.second;
      Q.pop();
      /*
        First, explore all "self-edges"
      */
      for(auto kv : g[v].energies) {
        int new_mask = mask;
        string energy_color = kv.first;
        int energy_cost = kv.second;
        // is our energy primary?
        if(colors[energy_color].empty()) new_mask |= 1<<primary2int[energy_color];
        else {
          // these colors are guaranteed to be primary due to the previous
          // preprocess step resolve_colors
          for(string adj_color : colors[energy_color]) {
            new_mask |= 1<<primary2int[adj_color];
          }
        }
        // did this energy give us new colors?
        // if yes, let's go to the vertex with this alternative mask
        if(mask != new_mask) {
          ll transition_cost = dist[v][mask] + energy_cost;
          if(transition_cost < dist[v][new_mask]) {
            dist[v][new_mask] = transition_cost;
            Q.push({dist[v][new_mask], {v, new_mask}});
          }
        }
      }
      /*
        Now, let's explore the "authentic" edges (if possible) and give
        them a zero weight
      */
      for(edge e : g[v].edges) {
        int required_mask = 0;
        int adj_vertex = e.adj;
        string energy = e.color;
        // again, let's handle the primary case apart
        if(colors[energy].empty()) required_mask |= 1<<primary2int[energy];
        else {
          for(string adj_color : colors[energy]) {
            required_mask |= 1<<primary2int[adj_color];
          }
        }
        // compare masks (i prefer to do this step by step to have easier dbg time!)
        bool can_jump = true;
        int new_mask = 0;
        for(int i=0; i<primary_count && can_jump; ++i) {
          if(required_mask & (1<<i)) {
            // we need a color that we do not have, we cannot jump :(
            if(!(mask & (1<<i))) can_jump = false;
          }
          else {
            // the edge does not ask us for this color, so we can carry it!
            new_mask |= (mask & (1<<i));
          }
        }
        if(can_jump) {
          int cur_dist = dist[v][mask];
          int adj_dist = dist[adj_vertex][new_mask];
          if(cur_dist < adj_dist) {
            dist[adj_vertex][new_mask] = dist[v][mask];
            Q.push({dist[v][mask], {adj_vertex, new_mask}});
          }
        }
      }
    }
    //*/
    //cout << "Case #" << tc << ": " << "NOT IMPLEMENTED" << endl;
    cout << "Case #" << tc << ":";
    /*
      Finally, compute the answer!
      For each vertex, get the minimum distance from all possible masks
    */
    vector< ll > ans(G, inf);
    for(int i=0; i<G; ++i) {
      for(int j=0; j<(1<<primary_count); ++j) ans[i] = min(ans[i], dist[i][j]);
    }
    for(int i=0; i<G; ++i) {
      cout << " ";
      if(ans[i] >= inf) cout << -1;
      else cout << ans[i];
    }
    cout << endl;
  }
}
