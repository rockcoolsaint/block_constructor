class MempoolTransaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = [] if parents == "" else parents.split(";")


def parse_mempool_csv():
    with open("mempool.csv") as f:
        return [
            MempoolTransaction(*line.strip('"').split(",")) for line in f.readlines()
        ]


def construct_block(transactions):
    block = []
    added_transactions = set()

    for tx in transactions:
        # if tx.txid not in added_transactions
        if sum(t.weight for t in block) + tx.weight <= 4000000:
            add_transaction_to_block(tx, block, added_transactions)

    return block


def add_transaction_to_block(transaction, block, added_transactions):
    for parent_txid in transaction.parents:
        parent_tx = next((tx for tx in block if tx.txid == parent_txid), None)
        if parent_tx:
            add_transaction_to_block(parent_tx, block, added_transactions)

    block.append(transaction)
    added_transactions.add(transaction.txid)


if __name__ == "__main__":
    transactions = parse_mempool_csv()
    block = construct_block(transactions)

    for tx in block:
        print(tx.txid)
    # print(len(block))
