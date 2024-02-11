#!/usr/bin/env python3

import pickle
import os

from os import urandom

from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.serialization import load_pem_public_key

salt = urandom(32)

class MessengerClient:
    """ Messenger client klasa

        Slobodno mijenjajte postojeće atribute i dodajte nove kako smatrate
        prikladnim.
    """

    def __init__(self, username, ca_pub_key):
        """ Inicijalizacija klijenta

        Argumenti:
        username (str) -- ime klijenta
        ca_pub_key     -- javni ključ od CA (certificate authority)

        """
        self.username = username
        self.ca_pub_key = ca_pub_key
        # Aktivne konekcije s drugim klijentima
        self.conns: dict[str, DoubleRatchet] = {}
        # Inicijalni Diffie-Hellman par ključeva iz metode `generate_certificate`
        self.dh_key_pair = ()

    def generate_certificate(self):
        """ Generira par Diffie-Hellman ključeva i vraća certifikacijski objekt

        Metoda generira inicijalni Diffie-Hellman par kljuceva; serijalizirani
        javni kljuc se zajedno s imenom klijenta postavlja u certifikacijski
        objekt kojeg metoda vraća. Certifikacijski objekt moze biti proizvoljan (npr.
        dict ili tuple). Za serijalizaciju kljuca mozete koristiti
        metodu `public_bytes`; format (PEM ili DER) je proizvoljan.

        Certifikacijski objekt koji metoda vrati bit će potpisan od strane CA te
        će tako dobiveni certifikat biti proslijeđen drugim klijentima.

        """
        private_key = X25519PrivateKey.generate()
        public_key = private_key.public_key()
        self.dh_key_pair = (public_key, private_key)

        pks = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return {
            'username': self.username,
            'pks': pks
        }

    def receive_certificate(self, cert, signature):
        """ Verificira certifikat klijenta i sprema informacije o klijentu (ime
            i javni ključ)

        Argumenti:
        cert      -- certifikacijski objekt
        signature -- digitalni potpis od `cert`

        Metoda prima certifikacijski objekt (koji sadrži inicijalni
        Diffie-Hellman javni ključ i ime klijenta) i njegov potpis kojeg
        verificira koristeći javni ključ od CA i, ako je verifikacija uspješna,
        sprema informacije o klijentu (ime i javni ključ). Javni ključ od CA je
        spremljen prilikom inicijalizacije objekta.

        """
        private_key, public_key = self.dh_key_pair[1], self.dh_key_pair[0]

        self.ca_pub_key.verify(signature, pickle.dumps(cert), ec.ECDSA(hashes.SHA256()))

        pks_raw = X25519PublicKey.from_public_bytes(cert['pks'])

        derived_public_key = private_key.exchange(pks_raw)

        shared_secret_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'Shared secret'
        ).derive(derived_public_key)

        self.conns[cert['username']] = DoubleRatchet(private_key=private_key, public_key=public_key, root_key=shared_secret_key, remote_public_key=pks_raw)


    def send_message(self, username, message):
        """ Slanje poruke klijentu

        Argumenti:
        message  -- poruka koju ćemo poslati
        username -- klijent kojem šaljemo poruku `message`

        Metoda šalje kriptiranu poruku sa zaglavljem klijentu s imenom `username`.
        Pretpostavite da već posjedujete certifikacijski objekt od klijenta
        (dobiven pomoću `receive_certificate`) i da klijent posjeduje vaš.
        Ako već prije niste komunicirali, uspostavite sesiju tako da generirate
        nužne `double ratchet` ključeve prema specifikaciji.

        Svaki put kada šaljete poruku napravite `ratchet` korak u `sending`
        lanacu (i `root` lanacu ako je potrebno prema specifikaciji).  S novim
        `sending` ključem kriptirajte poruku koristeći simetrični kriptosustav
        AES-GCM tako da zaglavlje poruke bude autentificirano.  Ovo znači da u
        zaglavlju poruke trebate proslijediti odgovarajući inicijalizacijski
        vektor.  Zaglavlje treba sadržavati podatke potrebne klijentu da
        derivira novi ključ i dekriptira poruku.  Svaka poruka mora biti
        kriptirana novim `sending` ključem.

        Metoda treba vratiti kriptiranu poruku zajedno sa zaglavljem.

        """
        return self.conns[username].DoubleRatchetEncrypt(str.encode(message));

    def receive_message(self, username, message):
        """ Primanje poruke od korisnika

        Argumenti:
        message  -- poruka koju smo primili
        username -- klijent koji je poslao poruku

        Metoda prima kriptiranu poruku od klijenta s imenom `username`.
        Pretpostavite da već posjedujete certifikacijski objekt od klijenta
        (dobiven pomoću `receive_certificate`) i da je klijent izračunao
        inicijalni `root` ključ uz pomoć javnog Diffie-Hellman ključa iz vašeg
        certifikata.  Ako već prije niste komunicirali, uspostavite sesiju tako
        da generirate nužne `double ratchet` ključeve prema specifikaciji.

        Svaki put kada primite poruku napravite `ratchet` korak u `receiving`
        lanacu (i `root` lanacu ako je potrebno prema specifikaciji) koristeći
        informacije dostupne u zaglavlju i dekriptirajte poruku uz pomoć novog
        `receiving` ključa. Ako detektirate da je integritet poruke narušen,
        zaustavite izvršavanje programa i generirajte iznimku.

        Metoda treba vratiti dekriptiranu poruku.

        """
        ciphertext, header = message
        return self.conns[username].DoubleRatchetDecrypt(ciphertext, header).decode()

@dataclass
class Header:
    message_number: int
    nonce: int
    public_key: bytes


@dataclass
class DoubleRatchet:
    private_key: X25519PrivateKey
    public_key: X25519PublicKey

    remote_public_key: X25519PublicKey

    root_key: bytes

    send_key: bytes = None
    receive_key: bytes = None


    sent_no: int = 0
    received_no: int = 0

    key_length: int = 32

    kdf_info: str = b"Ratchet v1.0"

    def DoubleRatchetEncrypt(self, plaintext: bytes):
        #sending first message
        if self.send_key is None:
            self._generate_DH()
            dh_out = self._DH()
            self.root_key, self.send_key = self._derive_keys(chain_key=None, dh_out=dh_out)

        self.send_key, message_key = self._derive_keys(self.send_key, dh_out=None)

        aesgcm = AESGCM(message_key)
        nonce = urandom(16)

        encrypted_message = aesgcm.encrypt(nonce, plaintext, None)

        header = Header(self.sent_no, nonce, self.public_key)
        self.sent_no += 1

        return encrypted_message, header

    def DoubleRatchetDecrypt(self, ciphertext: bytes, header: Header):
        if header.public_key != self.remote_public_key:
            self._DH_ratchet(header)

        self.receive_key, message_key = self._derive_keys(self.receive_key, dh_out=None)

        aesgcm = AESGCM(message_key)
        nonce = header.nonce

        original_message = aesgcm.decrypt(nonce, ciphertext, None)

        self.received_no += 1

        return original_message


    def _DH_ratchet(self, header: Header):
        self.sent_no = 0
        self.received_no = 0
        self.remote_public_key = header.public_key
        self.root_key, self.receive_key = self._derive_keys(chain_key=None, dh_out=self._DH())
        self._generate_DH()
        self.root_key, self.send_key = self._derive_keys(chain_key=None, dh_out=self._DH())

    def _generate_DH(self):
        private_key = X25519PrivateKey.generate()
        public_key = private_key.public_key()

        self.private_key = private_key
        self.public_key = public_key

    def _DH(self):
        return self.private_key.exchange(self.remote_public_key)

    def _derive_keys(self, chain_key, dh_out):
        hkdf_salt = salt
        hkdf_derive_key = chain_key

        if dh_out:
            hkdf_salt = dh_out
            hkdf_derive_key = self.root_key

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=2 * self.key_length,
            salt=hkdf_salt,
            info=self.kdf_info,
        )

        composite_key = hkdf.derive(hkdf_derive_key)

        first_key = composite_key[self.key_length:] # chain key ili root key
        second_key = composite_key[:self.key_length] # message key ili chain key

        return first_key, second_key
