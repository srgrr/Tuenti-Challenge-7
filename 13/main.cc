#include <bits/stdc++.h>
#include "omp.h"
using namespace std;

int64_t g(int64_t n, int64_t i) {
  if(i%2LL == 0LL) {
      return n*(n+1LL) / 2LL;
  }
  else {
    return (n+1LL) / 2LL;
  }
  int64_t a = 0;
  for (int64_t j = n; j >= 0; --j) {
      int64_t b = 0;
      int64_t t1 = (i & (n ^ j) & 1);
      for (int64_t k = 0; k <= i; ++k) {
          int64_t c = a ^ (t1 << k);
          a ^= (j & (1LL << k)) ^ b;
          b = (((c & j) | ((c ^ j) & b)) & (1LL << k)) << 1;
      }
      //cout << "   a = " << a << " | b = " << b << endl;
  }
  return a;
}

int64_t f(int64_t n) {
    int64_t r = 0;
    int64_t a_even = g(n, 62);
    int64_t a_odd = g(n, 63);
    for (int64_t i = 0; i < 64; ++i) {
      int64_t a = i%2LL ? a_odd : a_even;
      r |= (a & (1LL << i));
    }
    return r;
}

int main() {
  omp_set_num_threads(16);
  int T;
  cin >> T;
  unordered_map< int64_t, int64_t > lowest_found;
  vector< int64_t > queries(T);
  for(int tc=1; tc<=T; ++tc) {
    int64_t x;
    cin >> queries[tc-1];
    lowest_found[queries[tc-1]] = -1LL;
  }
  int64_t upper_limit = (1LL<<31LL);
  #pragma omp parallel for shared(lowest_found, upper_limit)
  for(int64_t i = 1; i<upper_limit; ++i) {
    int64_t fi = f(i);
    #pragma omp critical
    {
      if(lowest_found.count(fi)) {
        if(lowest_found[fi] == -1LL) lowest_found[fi] = i;
        else lowest_found[fi] = min(lowest_found[fi], i);
      }
    }
  }
  for(int tc=1; tc<=T; ++tc) {
    cout << "Case #" << tc << ": ";
    if(lowest_found[queries[tc-1]] == -1LL) cout << "IMPOSSIBLE" << endl;
    else cout << lowest_found[queries[tc-1]] << endl;
  }
}
