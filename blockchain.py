import hashlib as hasher
import datetime as date
import pymongo
import time
client = pymongo.MongoClient("mongodb+srv://testuser750:mongoDb_750@ehrblock.nvomfgg.mongodb.net/?retryWrites=true&w=majority")
db = client.testuser750
mydb=client["bloodbank"]
myrow=mydb['patient_patient']
# mycol=mydb["Blockhead"]
mylist=myrow.find_one()
cursor = myrow.find().sort([('timestamp', -1)]).limit(1)
#cursor=mycol.find()
print("================")
for each_mylist in cursor:
    print(each_mylist)
#print(mylist)
# Define what a Snakecoin block is
start2 = time.time()
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  def __repr__(self):
    return "%04d: %s, %s : %s" % (self.index,str(self.timestamp),str(self.data),str(self.previous_hash))
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(repr(self).encode('ascii'))
    return sha.hexdigest()
# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", "0")
# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]
# Show the blockchain
print(blockchain)

# Generate all later blocks in the blockchain
message_str = list(str(each_mylist))
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = message_str
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)

# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 2

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  block_to_add = next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  print("Hash: {}\n".format(block_to_add.hash))

print(blockchain)

from warnings import warn
def validate_blockchain(in_blockchain):
    for current_position in range(1, len(in_blockchain)):
        previous_position = current_position - 1
        if in_blockchain[previous_position].hash_block() == in_blockchain[current_position].previous_hash:
            print('Block %d is valid' % current_position)
        else:
            warn('Block %d is invalid! (%s)' % (current_position, repr(in_blockchain[current_position])))
            break
validate_blockchain(blockchain)

end = time.time()
print(end - start2)

# old_block_10_data = blockchain[10].data
# new_block_10_data = "Hey I'm an invalid data"
# blockchain[10].data = new_block_10_data
# validate_blockchain(blockchain)
# # replace the original, so we can try something else
# blockchain[10].data = old_block_10_data


# remove the 5th item
# del blockchain[2]
# validate_blockchain(blockchain)