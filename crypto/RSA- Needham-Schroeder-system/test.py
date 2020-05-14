from NeedhamSchroeder import *
import textwrap

def test():
    print("\nКриптографические протоколы, лабораторная работа 1")
    print("Асимметричный протокол Нидхема—Шрёдера с генерацией ключей с помощью RSA\n")

    # открытые ключи Алисы
    alice_public_key_pair = generate_public_keypair()
    alice_public_key = alice_public_key_pair[0]
    alice_private_key = alice_public_key_pair[1]
    alice_key_e = alice_public_key[0]
    alice_key_n = alice_public_key[1]
    alice_key_d = alice_private_key[0]

    # открытые ключи Боба
    bob_public_key_pair = generate_public_keypair()
    bob_public_key = bob_public_key_pair[0]
    bob_private_key = bob_public_key_pair[1]
    bob_key_e = bob_public_key[0]
    bob_key_n = bob_public_key[1]
    bob_key_d = bob_private_key[0]

    # открытые ключи Трента
    trent_public_key_pair = generate_public_keypair()
    trent_public_key = trent_public_key_pair[0]
    trent_private_key = trent_public_key_pair[1]
    trent_key_e = trent_public_key[0]
    trent_key_n = trent_public_key[1]
    trent_key_d = trent_private_key[0]

    # сертификаты Алисы и Боба {имя: открытый ключ}
    certificate = {}
    certificate['Alice'] = alice_public_key
    certificate['Bob'] = bob_public_key

    # hash map ---> string
    alice_certificate = "Alice," + str(certificate['Alice'][0]) + "," + str(certificate['Alice'][1])
    bob_certificate = "Bob," + str(certificate['Bob'][0]) + "," + str(certificate['Bob'][1])

    print("Трент: получены сертификаты Алисы и Боба - ", certificate)
    print("Трент: мой открытый ключ - ", trent_public_key, "\n")
    print("(1) Алиса: Трент, запрашиваю открытый ключ Боба.")
    # Трент отправляет Алисе зашифрованное своим секретным ключом сообщение с открытым ключом Боба
    rsa_encryption = RSAEncryption()
    bob_signed_certificate = [rsa_encryption.encrypt(ord(c), trent_key_d, trent_key_n) for c in bob_certificate]
    print("(2) Трент: Алиса, отправляю открытый ключ Боба. Сообщение зашифрованно с помощью моего ключа. ", bob_signed_certificate)
    # Алиса расшифровывает сообщение
    rsa_decryption = RSADecryption()
    decrypted_bob_certificate = "".join(str(x) for x in [chr(rsa_decryption.decrypt(c, trent_key_e, trent_key_n)) for c in bob_signed_certificate])
    decrypted_bob_certificate = decrypted_bob_certificate.split(',')
    # Алиса генерирует случайное число
    alice_nonce = generateNonce()
    # Алиса шифрует число с помощью открытого ключа Боба
    alice_nonce_encrypted_with_bob_public_key = rsa_encryption.encrypt(int(alice_nonce), int(decrypted_bob_certificate[1]), int(decrypted_bob_certificate[2]))
    # Алиса отправляет зашифрованное число Бобу со своим именем
    print("(3) Алиса: Боб, отправляю тебе свое случайное число, щашифрованное твоим ключом.")
    print("---------> Открытый текст: ", alice_nonce)
    print("---------> Текст, зашифрованный RSA с помощью ключа Боба: ", alice_nonce_encrypted_with_bob_public_key)
    print("(4) Боб: Трент, запрашиваю открытый ключ Алисы.")
    # Трент отправляет Бобу зашифрованное своим секретным ключом сообщение с открытым ключом Алисы
    alice_signed_certificate = [rsa_encryption.encrypt(ord(c), trent_key_d, trent_key_n) for c in alice_certificate]
    print("(5) Трент: Боб, отправляю открытый ключ Алисы. Сообщение зашифрованно с помощью моего ключа. " , alice_signed_certificate)
    # Боб расшифровывает сообщение
    decrypted_alice_certificate = "".join(str(x) for x in [chr(rsa_decryption.decrypt(c, trent_key_e, trent_key_n)) for c in alice_signed_certificate])
    decrypted_alice_certificate = decrypted_alice_certificate.split(',')
    # Боб расшифровывает число Алисы
    decrypted_alice_nonce = rsa_decryption.decrypt(alice_nonce_encrypted_with_bob_public_key, bob_key_d, bob_key_n)
    print("(6) Боб: Я расшифровал сообщение Алисы. ", decrypted_alice_nonce)
    # Боб генерирует случайное число
    bob_nonce = generateNonce()
    alice_nonce_with_bob_nonce = str(decrypted_alice_nonce) + "," + str(bob_nonce)
    # Боб шифрует свое случайное число + случайное число АЛисы с помощью открытого ключа Алисы
    bob_nonce_encrypted_with_alice_public_key = [rsa_encryption.encrypt(ord(c), int(decrypted_alice_certificate[1]), int(decrypted_alice_certificate[2])) for c in alice_nonce_with_bob_nonce]
    # Боб отправляет сообщение Алисе
    print("(6) Боб: Алиса, отправляю тебе сумму наших чисел. ", bob_nonce_encrypted_with_alice_public_key)
    # Алиса расшифровывает сообщение боба
    decrypted_alice_nonce_from_bob = "".join(str(x) for x in [chr(rsa_decryption.decrypt(c, alice_key_d, alice_key_n)) for c in bob_nonce_encrypted_with_alice_public_key])
    decrypted_alice_nonce_from_bob = decrypted_alice_nonce_from_bob.split(",")
    print("(7) Алиса: Я расшифровала сообщение Боба: ", decrypted_alice_nonce_from_bob)

    # Верификация
    if decrypted_alice_nonce_from_bob[0] == str(alice_nonce):
        print("Верификация прошла успешно")
    else:
        print("\nОШИБКА ВЕРИФИКАЦИИ\n")
        sys.exit(1)

    # Алиса вычисляет число Боба
    encrypt_bob_nonce_to_send_back = [rsa_encryption.encrypt(ord(c), bob_key_e, bob_key_n) for c in decrypted_alice_nonce_from_bob[1]]
    # Алиса отправляет Бобу его число
    print("(8) Алиса: Боб, отправляю тебе твое число. ", encrypt_bob_nonce_to_send_back)
    final_bob_nonce_from_alice = "".join(str(x) for x in [chr(rsa_decryption.decrypt(c, bob_key_d, bob_key_n)) for c in encrypt_bob_nonce_to_send_back])
    print("(9) Боб: Я расшифровал сообщение Алисы: ", final_bob_nonce_from_alice)

    # Верификация
    if final_bob_nonce_from_alice == str(bob_nonce):
        print("Верификация прошла успешно")
    else:
        print("\nОШИБКА ВЕРИФИКАЦИИ\n")
        sys.exit(1)

    del alice_nonce, bob_nonce
    sys.exit(0)


test()
