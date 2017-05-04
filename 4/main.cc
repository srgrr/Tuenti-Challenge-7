#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
const ll inf = 10000000000000000ll;

/*
  a+b > x => x in [0, a+b-1]
  a+x > b => x in [b-a+1, inf)
  b+x > a => x in [a-b+1, inf)
  fix a,b to be contiguous in the sorted array of sides
  and find the minimal available side that satisfies these
  inequalities
*/

int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    int n;
    cin >> n;
    vector<ll> v(n);
    multiset<ll> S;
    for(ll& x : v) {
      cin >> x;
      S.insert(x);
    }
    sort(v.begin(), v.end());
    ll ans = inf;
    for(int i=0; i<n-1; ++i) {
      ll a = v[i], b = v[i+1];
      S.erase(S.find(a));
      S.erase(S.find(b));
      auto it = S.lower_bound(abs(a-b)+1);
      if(it != S.end() && *it < a+b) {
        ans = min(ans, a + b + *it);
      }
      S.insert(a);
      S.insert(b);
    }
    cout << "Case #" << tc << ": ";
    if(ans == inf) cout << "IMPOSSIBLE" << endl;
    else cout << ans << endl;
  }
}
