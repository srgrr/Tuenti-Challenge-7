import socket
import random

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

def _prob_to_increase(card_log, value):
  total_values = sum(card_log.values())
  ret = 0.0
  for (card, freq) in card_log.items():
    card_values = card2score(card)
    if any(int(value)+int(card_value) <= 21 for card_value in card_values):
      ret += float(freq) / float(total_values)
  return ret

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
  all_values = get_all_values(card_values, 0)
  total_values = len(all_values)
  ret = 0.0
  for value in all_values:
      ret += _prob_to_increase(card_log, value) / float(total_values)
  return ret

def main():
  s = [2]*7
  for i in range(7):
    s[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s[i].connect((IP_ADDRESS, PORT))

  alive = [True]*7

  card_log = {
        '2': 32,
        '3': 32,
        '4': 32,
        '5': 32,
        '6': 32,
        '7': 32,
        '8': 32,
        '9': 32,
        '0': 32,
        'A': 32,
        'J': 32,
        'Q': 32,
        'K': 32
    }


  current_cards = ('Z', 'Z')

  last_message = ['z']*7

  # welcome phase
  for i in range(7):
    it = 0
    while not 'Good luck!' in last_message[i]:
      last_message[i] = s[i].recv(BYTE_REQ)
      print 'PLAYER %i'%i
      print last_message[i]
      if 'Room closed' in last_message[i]: exit(0)
      it += 1;
      if it >= 10: exit(0)

  while any(alive):
    print 'ALIVE STATUS %s'%alive
    # betting phase, send the bets
    # for the snitchers
    for i in range(3, 7):
      it = 0
      while not '+bet' in last_message[i]:
        last_message[i] = s[i].recv(BYTE_REQ)
        print 'PLAYER %i BET SENDING'%i
        print last_message[i]
        if 'Room closed' in last_message[i]: exit(0)
        it += 1;
        if it >= 10: exit(0)
      print 'Sending bet for player %d'%i
      s[i].send('+bet10\n')
      print 'Bet for player %d sent'%i
    # betting phase, read the cards
    for i in range(3, 7):
      # read the cards
      it = 0
      while not 'You get' in last_message[i]:
        last_message[i] = s[i].recv(BYTE_REQ)
        print 'PLAYER %i CARD PARSING'%i
        print last_message[i]
        if 'Room closed' in last_message[i]: exit(0)
        it += 1;
        if it >= 10: exit(0)
      cards = get_line_where(last_message[i], 'You get').split(' ')[3].split(' ')[0]
      # register the cards to our log
      card_log[cards[0]] -= 1
      card_log[cards[1]] -= 1
      # only if we are the winner: register our cards and the dealer's
      if i == 6:
        current_cards = (cards[0], cards[1])
        it = 0
        while not 'DEALER CARDS' in last_message[i]:
          last_message[i] = s[i].recv(BYTE_REQ)
          print 'PLAYER %i DEALER REGISTER'%i
          print last_message[i]
          if 'Room closed' in last_message[i]: exit(0)
          it += 1;
          if it >= 10: exit(0)
        dealer_card = get_line_where(last_message[i], 'DEALER CARDS').split(' ')[3].replace('?', '').replace('\n', '')
        card_log[dealer_card] -= 1


    print 'HIT/STAND PHASE FOR SNITCHERS'

    # hit/ stand phase for snitchers
    for i in range(3, 6):
      it = 0
      while not '+hit' in last_message[i]:
        last_message[i] = s[i].recv(BYTE_REQ)
        print 'PLAYER %i SNITCH SEND'%i
        print last_message[i]
        if 'Room closed' in last_message[i]: exit(0)
        it += 1;
        if it >= 10: exit(0)

      print 'Sending stand for player %d'%i
      s[i].send('+stand\n')
      print 'Stand for player %d sent'%i


    print 'HIT/STAND PHASE FOR WINNER'

    # hit/ stand phase for winner
    i = 6
    it = 0
    while not '+hit' in last_message[i]:
      last_message[i] = s[i].recv(BYTE_REQ)
      print 'PLAYER %i SNITCH SEND'%i
      print last_message[i]
      if 'Room closed' in last_message[i]: exit(0)
      it += 1;
      if it >= 10: exit(0)

    converged = False
    while not converged:
      pr_a = prob_to_increase(card_log, current_cards)
      pr_b = prob_to_increase(card_log, [dealer_card, 'Q'])
      print 'Probability to not liarla is %.08f vs %.08f'%(pr_a, pr_b)
      if pr_a > 0.65:
        s[i].send('+hit\n')
        # lets get our new card and register it
        it = 0
        while 'You get' not in last_message[i]:
          last_message[i] = s[i].recv(BYTE_REQ)
          print 'PLAYER %i HIT'%i
          print last_message[i]
          if 'Room closed' in last_message[i]: exit(0)
          it += 1;
          if it >= 10: exit(0)
        card = get_line_where(last_message[i], 'You get').split(' ')[3].split(' ')[0]
        current_cards = list(current_cards) + [card]
        card_log[card] -= 1
        vals = get_all_values(current_cards, 0)
        if min(vals) > 21:
          converged = True
        else:
          it = 0
          while '+hit' not in last_message[i]:
            last_message[i] = s[i].recv(BYTE_REQ)
            print 'PLAYER %d NEWREQ'%i
            print last_message[i]
      else:
        s[i].send('+stand\n')
        converged = True
    # get the whole dealer's hand
    it = 0
    while not 'DEALER CARDS' in last_message[i]:
        last_message[i] = s[i].recv(BYTE_REQ)
        print 'PLAYER %i DEALER RECV'%i
        print last_message[i]
        if 'Room closed' in last_message[i]: exit(0)
        it += 1;
        if it >= 10: exit(0)
    dealer_cards = get_line_where(last_message[i], 'DEALER CARDS').split(' ')[3].replace('?', '').replace('\n', '')
    for card in dealer_cards[:-1]:
      card_log[card] -= 1

    # lets register the whole dealer's hand


if __name__ == "__main__":
  main()
