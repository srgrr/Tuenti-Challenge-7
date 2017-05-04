import socket
import random
import sys

IP_ADDRESS = '52.49.91.111'
PORT = 2121
BYTE_REQ = 100000

def get_line_where(x, p):
  ret = None
  for line in x.split('\n'):
    if p in line: ret = line
  if ret is None:
    raise Exception('No matching pattern found')
  return ret

def card2score(x):
  if x == '0' or x == 'J' or x == 'Q' or x == 'K': return [10]
  if x == 'A': return [1, 11]
  return [ord(x) - ord('0')]

def get_all_values(card_list, accumulated):
  if not card_list: return [accumulated]
  last_v = card2score(card_list[-1])
  ret = []
  for v in last_v:
    ret += get_all_values(card_list[:-1], accumulated+v)
  return ret

'''
    Lets approximate the probability to increase our score
    without being busted
'''
def prob_to_increase(card_log, card_values):
  print card_log, card_values
  all_values = [min(get_all_values(card_values, 0))]
  total_values = 1.0
  ret = 0.0
  for value in all_values:
      ret += _prob_to_increase(card_log, value) / float(total_values)
  return ret

# 0 1 2 3 4 5 6

def get_action(have_a, val, dealer_card):
    H = '+hit'
    S = '+stand'
    if have_a:
        if val < 8: return H
        else: return S
    if val < 12: return H
    if val > 16: return S
    if dealer_card >= '2' and dealer_card <= '9':
        dealer_card = ord(dealer_card) - ord('0')
    elif dealer_card in ['0', 'J', 'Q', 'K']:
        dealer_card = 8
    else:
        dealer_card = 9

    T = [
     [H, H, S, S, S, H, H, H, H, H],
     [S, S, S, S, S, H, H, H, H, H],
     [S, S, S, S, S, H, H, H, H, H],
     [S, S, S, S, S, H, H, H, H, H],
     [S, S, S, S, S, H, H, H, H, H]
    ]
    return T[val-12][dealer_val]

def main():
    whoami = int(sys.argv[1])
    last_message = 'z'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDRESS, PORT))
    last_cards = 'a'
    last_values = 'a'
    dealer_card = 'a'
    while not 'Room closed' in last_message:
        last_message = s.recv(BYTE_REQ)
        print last_message
        if 'Room closed' in last_message: exit(0)
        if '+bet' in last_message:
            if whoami >= 0 and whoami <= 3: exit(0)
            s.send('+bet10\n')
            it = 0
            while not 'You get' in last_message:
                last_message = s.recv(BYTE_REQ)
                print '[YOU GET]\n%s'%last_message
                it += 1
                if 'Room closed' in last_message: exit(0)
                if it == 20: exit(0)
            last_values = eval(get_line_where(last_message, 'You get').split(" ")[-1].replace('\n', ''))
            it = 0
            while not 'DEALER CARDS' in last_message:
                last_message = s.recv(BYTE_REQ)
                print '[DEALER CARDS]\n%s'%last_message
                it += 1
                if 'Room closed' in last_message: exit(0)
                if it == 20: exit(0)
            dealer_card = get_line_where(last_message, 'DEALER CARDS').split(' ')[3].replace('?', '').replace('\n', '')
        if '+hit' in last_message:
            if whoami == 6:
                have_a = len(last_values) > 1
                s.send(get_action(have_a, last_values, dealer_card)+'\n')
            else:
                s.send('+stand\n')







if __name__ == "__main__":
  main()
