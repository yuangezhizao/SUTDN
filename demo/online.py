from SUTDN import *

if __name__ == '__main__':
	a = SUTDN('<username>', '<password>')
	if a.login() != 0:
		query_state('<username>', '<password>')
