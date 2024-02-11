from os import urandom

from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

salt = urandom(32)

class MessengerClient:
    """ Messenger client class

        Feel free to modify the attributes and add new ones as you
        see fit.

    """

    def __init__(self, username, max_skip=10):
        """ Initializes a client

        Arguments:
        username (str) -- client name
        max_skip (int) -- Maximum number of message keys that can be skipped in
                          a single chain

        """
        self.username = username
        # Data regarding active connections.
        # Object containing usernames and their Ratchet connection
        self.conn: dict[str, Ratchet] = {}
        # Maximum number of message keys that can be skipped in a single chain
        self.max_skip = max_skip

    def add_connection(self, username, chain_key_send, chain_key_recv):
        """ Add a new connection

        Arguments:
        username (str) -- user that we want to talk to
        chain_key_send -- sending chain key (CKs) of the username
        chain_key_recv -- receiving chain key (CKr) of the username

        """

        self.conn[username] = Ratchet(send_key=chain_key_send, receive_key=chain_key_recv, max_skip=self.max_skip)

    def send_message(self, username, message):
        """ Send a message to a user

        Get the current sending key of the username, perform a symmetric-ratchet
        step, encrypt the message, update the sending key, return a header and
        a ciphertext.

        Arguments:
        username (str) -- user we want to send a message to
        message (str)  -- plaintext we want to send

        Returns a ciphertext and a header data (you can use a tuple object)

        """

        return self.conn[username].RatchetEncrypt(str.encode(message))

    def receive_message(self, username, message):
        """ Receive a message from a user

        Get the username connection data, check if the message is out-of-order,
        perform necessary symmetric-ratchet steps, decrypt the message and
        return the plaintext.

        Arguments:
        username (str) -- user who sent the message
        message        -- a ciphertext and a header data

        Returns a plaintext (str)

        """

        encrypted_message, header = message
        return self.conn[username].RatchetDecrypt(encrypted_message, header).decode()


@dataclass
class Header:
    message_number: int
    nonce: int


@dataclass
class Ratchet:
    send_key: bytes
    receive_key: bytes
    max_skip: int

    sent_no: int = 0
    received_no: int = 0

    key_length: int = 32

    kdf_info: str = b"Ratchet v1.0"

    # Dict storing skipped message keys
    # key: message number
    # value: message key
    skipped_message_keys = {}

    def RatchetEncrypt(self, plaintext: bytes):
        self.send_key, message_key = self._derive_keys(self.send_key)

        aesgcm = AESGCM(message_key)
        nonce = urandom(16)

        encrypted_message = aesgcm.encrypt(nonce, plaintext, None)

        header = Header(self.sent_no, nonce)
        self.sent_no += 1

        return encrypted_message, header

    def RatchetDecrypt(self, ciphertext: bytes, header: Header):
        original_message = self.trySkippedMessageKeys(ciphertext, header)

        if original_message != None:
            return original_message

        self._skipMessageKeys(header.message_number)

        self.receive_key, message_key = self._derive_keys(self.receive_key)
        
        aesgcm = AESGCM(message_key)
        nonce = header.nonce

        original_message = aesgcm.decrypt(nonce, ciphertext, None)

        self.received_no += 1

        return original_message


    def _derive_keys(self, chain_key):
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=2 * self.key_length,
            salt=salt,
            info=self.kdf_info,
        )

        composite_key = hkdf.derive(chain_key)

        new_chain_key = composite_key[self.key_length:]
        message_key = composite_key[:self.key_length]

        return new_chain_key, message_key

    def trySkippedMessageKeys(self, ciphertext, header: Header):
        if header.message_number in self.skipped_message_keys:
            message_key = self.skipped_message_keys[header.message_number]
            del self.skipped_message_keys[header.message_number]

            aesgcm = AESGCM(message_key)
            nonce = header.nonce

            original_message = aesgcm.decrypt(nonce, ciphertext, None)
            return original_message

        return None

    def _skipMessageKeys(self, until):
        if self.received_no > self.max_skip:
            raise Exception()

        if self.receive_key != None:
            while self.received_no < until:
                self.receive_key, message_key = self._derive_keys(self.receive_key)
                self.skipped_message_keys[self.received_no] = message_key
                self.received_no += 1
