package hr.fer.rgkk.transactions;

import org.bitcoinj.core.ECKey;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.core.Utils;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import java.security.SecureRandom;

import static org.bitcoinj.script.ScriptOpCodes.*;

public class CoinToss extends ScriptTransaction {

    // Alice's private key
    private final ECKey aliceKey;
    // Alice's nonce
    private final byte[] aliceNonce;
    // Bob's private key
    private final ECKey bobKey;
    // Bob's nonce
    private final byte[] bobNonce;
    // Key used in unlocking script to select winning player.
    private final ECKey winningPlayerKey;

    private CoinToss(
            WalletKit walletKit, NetworkParameters parameters,
            ECKey aliceKey, byte[] aliceNonce,
            ECKey bobKey, byte[] bobNonce,
            ECKey winningPlayerKey
    ) {
        super(walletKit, parameters);
        this.aliceKey = aliceKey;
        this.aliceNonce = aliceNonce;
        this.bobKey = bobKey;
        this.bobNonce = bobNonce;
        this.winningPlayerKey = winningPlayerKey;
    }

    @Override
    public Script createLockingScript() {
        return new ScriptBuilder()
                .op(OP_DUP) // s, Ra, Rb, Rb
                .op(OP_HASH160) // s, Ra, Rb, Cb
                .data(bobNonce) // s, Ra, Rb, Cb, Rb
                .op(OP_HASH160) // s, Ra, Rb, Cb, Cb
                .op(OP_EQUALVERIFY) // s, Ra, Rb
                .op(OP_SWAP) // s, Rb, Ra
                .op(OP_DUP) // s, Rb, Ra, Ra
                .op(OP_HASH160) // s, Rb, Ca
                .data(aliceNonce) // s, Rb, Ca, Ra
                .op(OP_HASH160) // s, Rb, Ca, Ca
                .op(OP_EQUALVERIFY) // s, Rb, Ra

                .op(OP_SIZE) // s, Rb, Ra, aliceNonceSize
                .data(bobNonce) // s, Rb, Ra, aliceNonceSize, Rb
                .op(OP_SIZE) // s, Rb, Ra, aliceNonceSize, Rb, bobNonceSize
                .op(OP_NIP) // s, Rb, Ra, aliceNonceSize, bobNonceSize
                .number(16) // s, Rb, Ra, aliceNonceSize, bobNonceSize, 16
                .op(OP_SWAP) // s, Rb, Ra, aliceNonceSize, 16, bobNonceSize
                .op(OP_SUB) // s, Rb, Ra, aliceNonceSize, bobChoice
                .op(OP_SWAP) // s, Rb, Ra, bobChoice, aliceNonceSize
                .number(16) // s, Rb, Ra, bobChoice, aliceNonceSize, 16
                .op(OP_SWAP) // s, Rb, Ra, bobChoice, 16, aliceNonceSize
                .op(OP_SUB) // s, Rb, Ra, bobChoice, aliceChoice
                .op(OP_BOOLOR) // s, Rb, Ra, result
                .number(0) // s, Rb, Ra, result, 0
                .op(OP_EQUAL) // s, Rb, Ra, T/F

                .op(OP_NOTIF) // ako je result == 1; s, Rb, Ra
                    .op(OP_2DROP) // s
                    .data(bobKey.getPubKey()) // s, bobKey
                    .op(OP_CHECKSIG)
                .op(OP_ELSE) // ako je result == 0 (bob pobjedjuje); s, Rb, Ra
                    .op(OP_2DROP) // s
                    .data(aliceKey.getPubKey()) // s, bobKey
                    .op(OP_CHECKSIG)

                .op(OP_ENDIF)
                .build();

    }

    @Override
    public Script createUnlockingScript(Transaction unsignedTransaction) {
        TransactionSignature signature = sign(unsignedTransaction, winningPlayerKey);
        return new ScriptBuilder()
                .data(signature.encodeToBitcoin())
                .data(aliceNonce)
                .data(bobNonce)
                .build();
    }

    public static CoinToss of(
            WalletKit walletKit, NetworkParameters parameters,
            CoinTossChoice aliceChoice, CoinTossChoice bobChoice,
            WinningPlayer winningPlayer
    ) {
        byte[] aliceNonce = randomBytes(16 + aliceChoice.value);
        byte[] bobNonce = randomBytes(16 + bobChoice.value);

        ECKey aliceKey = randKey();
        ECKey bobKey = randKey();

        // Alice is TAIL, bob is HEAD
        ECKey winningPlayerKey = WinningPlayer.TAIL == winningPlayer ? aliceKey : bobKey;

        return new CoinToss(
                walletKit, parameters,
                aliceKey, aliceNonce,
                bobKey, bobNonce,
                winningPlayerKey
        );
    }

    private static byte[] randomBytes(int length) {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[length];
        random.nextBytes(bytes);
        return bytes;
    }

    public enum WinningPlayer {
        TAIL, HEAD
    }

    public enum CoinTossChoice {

        ZERO(0),
        ONE(1);

        public final int value;

        CoinTossChoice(int value) {
            this.value = value;
        }
    }
}

