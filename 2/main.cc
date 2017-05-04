#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    cout << "Case #" << tc << ":";
    int n;
    cin >> n;
    vi v(n+4, 0), ans(14, 0);
    for(int i=0; i<n; ++i) cin >> v[i];
    int current_frame = 0, i = 0, frame_limit = 10;
    while(current_frame < frame_limit) {
      if(v[i] == 10) {
        ans[current_frame] = 10 + v[i+1] + v[i+2];
        ++i;
      }
      else {
        ans[current_frame] = v[i] + v[i+1] + v[i+2]*(v[i] + v[i+1] == 10);
        i += 2;
      }
      if(current_frame) ans[current_frame] += ans[current_frame-1];
      ++current_frame;
    }
    for(int i=0; i<frame_limit; ++i) cout << ' ' << ans[i];
    cout << endl;
  }
}
