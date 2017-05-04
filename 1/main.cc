#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  int T;
  cin >> T;
  for(int tc=1; tc<=T; ++tc) {
    int n;
    cin >> n;
    int ans = 0;
    while(n--) {
      int x;
      cin >> x;
      ans += x;
    }
    cout << "Case #" << tc << ": " << (ans + 7) / 8 << endl;
  }
}
