from .kem import mceliece6960119

if __name__ == '__main__':
	public_key, secret_key = mceliece6960119.kem_keypair()
	test_key, test_ciphertext = mceliece6960119.kem_enc(public_key)
	test_decrypted = mceliece6960119.kem_dec(test_ciphertext, secret_key)

	if test_key != test_decrypted:
		raise AssertionError('fail :(')
	print('OK')
