import requests
import hashlib
import sys 


def requests_api_data(query):
	url = 'https://api.pwnedpasswords.com/range/'+ query
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f"Error fetching: {res.status_code}, check api and try again")
	return res	

def password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(":") for line in hashes.text.splitlines())
	for h , count in hashes:
		if h == hash_to_check:
			return count
	return 0
	

def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
	first5, tail = sha1password[:5], sha1password[5:]
	respond = requests_api_data(first5)
	print(respond)
	return password_leaks_count(respond, tail)
	

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f"{password} was found {count} times...you should change ")
		else:
			print(f"{password} was not found. Carry on !")
	return "done"

main(sys.argv[1:])