#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;

ll highest_set_bit(ll x) {
  int ans = 0;
  for(int i=0; i<64; ++i) {
    if(x&(1ll<<ll(i))) ans = i+1;
  }
  return ans;
}

int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    ll n;
    cin >> n;
    cout << "Case #" << tc << ": " << highest_set_bit(n) << endl;
  }
}
