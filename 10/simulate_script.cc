#include <bits/stdc++.h>
#include <openssl/md5.h>
#include <zlib.h>
using namespace std;
typedef long long int ll;

void print_md5_sum(unsigned char* md) {
    int i;
    for(i=0; i<MD5_DIGEST_LENGTH; i++) {
            printf("%02x",md[i]);
    }
}

ll fastpow(ll b, ll e, ll m) {
  if(e == 0ll) return 1ll;
  if(e == 1ll) return b;
  ll aux = fastpow((b*b)%m, e/2, m) % m;
  if(e%2ll == 1ll) {
    return (b*aux)%m;
  }
  return aux;
}

/*
unsigned char *MD5(const unsigned char *d,
                   unsigned long n,
                   unsigned char *md);
                   */

int main(int argc, char** argv) {
  ll secret1 = atoi(argv[1]);
  ll secret2 = atoi(argv[2]);
  ll secret3 = -1;
  if(argc < 5) {
    secret3 = crc32(0L, (const Bytef*)argv[3], strlen(argv[3]));
  }
  else {
    secret3 = crc32(0L, (const Bytef*)argv[4], strlen(argv[4]));
  }
  ll counter = secret3;

  counter = (counter * fastpow(secret1, 10000000, secret2))%secret2;

  string password = "";
  for(int i=0; i<10; ++i) {
    counter = (counter * secret1) % secret2;
    password += char(counter%94 + 33);
  }

  unsigned char result[MD5_DIGEST_LENGTH];

  MD5((unsigned char*)password.c_str(), password.size(), result);

  cout << password << " ";
  print_md5_sum(result);
  cout << endl;
}
