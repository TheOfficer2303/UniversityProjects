package hr.fer.rgkk.transactions;

import org.bitcoinj.core.ECKey;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.core.Utils;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import java.time.Instant;

import static org.bitcoinj.script.ScriptOpCodes.*;

public class TimeLock extends ScriptTransaction {

    private final ECKey aliceSecretKey = new ECKey();
    private final ECKey bobSecretKey = new ECKey();
    private final ECKey eveSecretKey = new ECKey();

    public enum ScriptSigType {
        ALICE_AND_EVE, BOB_AND_EVE, ALICE_AND_BOB
    }

    ScriptSigType scriptSigType;

    public TimeLock(WalletKit walletKit, NetworkParameters parameters, ScriptSigType scriptSigType) {
        super(walletKit, parameters);
        this.scriptSigType = scriptSigType;
    }

    @Override
    public Script createLockingScript() {
        long time = Instant.parse("2014-10-01T00:00:00Z").getEpochSecond();
        return new ScriptBuilder() // 0, aliceSign, bobSign, 0
                .op(OP_NOTIF) // na vrhu stoga je 0, trebaju nam oba potpisa

                    .smallNum(1) // 0, aliceSign, bobSign, 1
                    .data(aliceSecretKey.getPubKey()) // 0, aliceSign, bobSign, 1, alicePubKey
                    .data(bobSecretKey.getPubKey()) // 0, aliceSign, bobSign, 1, alicePubKey, bobPubKey
                    .smallNum(2) // 0, aliceSign, bobSign, 1, alicePubKey, bobPubKey, 2
                    .op(OP_CHECKMULTISIG)

                .op(OP_ELSE) // na vrhu stoga je 1, treba nam Evin i Alice/Bob potpis

                    .number(time) // 0, aliceSign, eveSign, evePubKey, time
                    .op(OP_CHECKLOCKTIMEVERIFY) // 0, aliceSign, eveSign, evePubKey, time
                    .op(OP_DROP) // 0, aliceSign, eveSign, evePubKey
                    .op(OP_DUP) // 0, aliceSign, eveSign, evePubKey, evePubKey
                    .op(OP_HASH160) // 0, aliceSign, eveSign, evePubKey, evePubKeyHash
                    .data(eveSecretKey.getPubKeyHash()) // 0, aliceSign, eveSign, evePubKey, evePubKeyHash, evePubKeyHash
                    .op(OP_EQUALVERIFY) // 0, aliceSign, eveSign, evePubKey
                    .op(OP_CHECKSIGVERIFY) // 0, aliceSign
                    .smallNum(1) // 0, aliceSign, 1
                    .data(aliceSecretKey.getPubKey()) // 0, aliceSign, 1, alicePubKey
                    .data(bobSecretKey.getPubKey()) // 0, aliceSign, 1, alicePubKey, bobPubKey
                    .smallNum(2) // 0, aliceSign, 1, alicePubKey, bobPubKey, 2
                    .op(OP_CHECKMULTISIG)

                .op(OP_ENDIF)

                .build();

    }

    @Override
    public Script createUnlockingScript(Transaction unsignedScript) {
        ScriptBuilder scriptBuilder = new ScriptBuilder();
        switch (this.scriptSigType) {
            case ALICE_AND_BOB:
                scriptBuilder
                        .smallNum(0)
                        .data(sign(unsignedScript, aliceSecretKey).encodeToBitcoin())
                        .data(sign(unsignedScript, bobSecretKey).encodeToBitcoin())
                        .smallNum(0);
                break;
            case ALICE_AND_EVE:
                scriptBuilder
                        .smallNum(0)
                        .data(sign(unsignedScript, aliceSecretKey).encodeToBitcoin())
                        .data(sign(unsignedScript, eveSecretKey).encodeToBitcoin())
                        .data(eveSecretKey.getPubKey())
                        .smallNum(1);
                break;
            case BOB_AND_EVE:
                scriptBuilder
                        .smallNum(0)
                        .data(sign(unsignedScript, bobSecretKey).encodeToBitcoin())
                        .data(sign(unsignedScript, eveSecretKey).encodeToBitcoin())
                        .data(eveSecretKey.getPubKey())
                        .smallNum(1);
        }
        return scriptBuilder.build();
    }
}
