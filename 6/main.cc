#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
typedef pair<pair<ll, ll>, ll> thing;
const int maxn = 3000;
const ll inf = (1ll<<62ll) + 1337ll;
vector< thing > intervals;
ll dp[maxn];
ll until, n;

ll f(ll x) {
  return x*(x+1ll) / 2ll;
}

ll partsum(ll l, ll r) {
  return f(r) - f(l-1ll);
}

ll calc(int pos) {
  if(pos == n+1) {
    return 0ll;
  }
  ll& ref = dp[pos];
  if(ref != -1ll) return ref;
  ll a = intervals[pos].first.first;
  ll b = intervals[pos].first.second;
  ll interval_cost = min(intervals[pos].second, partsum(a, b-1ll));
  ref = interval_cost + partsum(b, until-1ll);
  for(int i=pos+1; i<=n+1; ++i) {
    ll c = intervals[i].first.first;
    ll bc = max(0ll, partsum(b, c-1ll));
    ref = min(ref, interval_cost + bc + calc(i));
  }
  return ref;
}

int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    memset(dp, 0xff, sizeof(dp));
    cin >> until >> n;
    intervals = vector< thing >(n+2);
    intervals[0] = {{1, 1}, 0ll};
    intervals[n+1] = {{until, until}, 0ll};
    for(int i=1; i<=n; ++i) {
      thing& intv = intervals[i];
      cin >> intv.first.first >> intv.first.second >> intv.second;
    }
    sort(intervals.begin(), intervals.end());
    cout << "Case #" << tc << ": " << calc(0) << endl;
  }
}
