import heapq
import sys

with open(sys.argv[1]) as f:
    diskmap = f.read().strip()

blocks = []

# heaps of free blocks
spaces = [[] for i in range(10)]

total_size = 0

# Build a list of blocks
file_id = 0
start_idx = 0
for i, v in enumerate(diskmap):
    size = int(v)
    if i % 2 == 0:
        blocks.append((file_id, start_idx, size))
        file_id += 1
        total_size += size
    else:
        block = (None, start_idx, size)
        blocks.append(block)
        heapq.heappush(spaces[size], start_idx)
    start_idx += size

def calculate_checksum(blocks):
    checksum = 0
    for file_id, start_idx, size in blocks:
        n = size * (start_idx + start_idx + size - 1) // 2
        checksum += n * file_id
    return checksum

# Compact (Part 1)
out_blocks = []
move_candidates = filter(lambda b: b[0] is not None, reversed(blocks))
partial_block = None
last_move_id = None

for i, block in enumerate(blocks):
    file_id, start_idx, size = block
    if file_id is not None:
        if file_id == last_move_id:
            # Reached the last block
            break

        # Files always move over as-is
        out_blocks.append(block)
    else:
        # Space, fill it
        space_remaining = size
        while space_remaining > 0:
            # Find a block to move
            if partial_block is not None:
                to_move = partial_block
                partial_block = None
            else:
                to_move = next(move_candidates)

            move_id, move_start, move_size = to_move

            # Only move backwards
            if move_start <= start_idx:
                break

            last_move_id = move_id

            if space_remaining >= move_size:
                # Move whole block
                out_blocks.append((move_id, start_idx, move_size))
                space_remaining -= move_size
                start_idx += move_size
            else:
                # Need to split block
                out_blocks.append((move_id, start_idx, space_remaining))
                partial_block = (move_id, move_start, move_size - space_remaining)
                space_remaining = 0

if partial_block is not None and file_id == partial_block[0]:
    # Last block, is partial
    out_blocks.append(partial_block)

# Part 1 answer
print(calculate_checksum(out_blocks))

# Defragment - Part 2
out_blocks_p2 = []
move_candidates = filter(lambda b: b[0] is not None, reversed(blocks))
for block in move_candidates:
    file_id, start_idx, size = block

    # Look for *the first* free space, of any acceptable size
    first_space_idx = blocks[-1][1] + blocks[-1][2]
    first_space_size = None
    for i in range(size, 10):
        if len(spaces[i]) > 0:
            idx = spaces[i][0]
            if idx >= start_idx:
                # Only move left
                continue

            if idx < first_space_idx:
                first_space_idx = idx
                first_space_size = i

    if first_space_size is not None:
        # Consume the space
        space_idx = heapq.heappop(spaces[first_space_size])
        # Store to output
        out_blocks_p2.append((file_id, space_idx, size))
        # Record remaining space
        if size < first_space_size:
            heapq.heappush(spaces[first_space_size - size], space_idx + size)
    else:
        # Nowhere that fits, put directly in the output
        out_blocks_p2.append(block)

# out_blocks now contains the defragged disk. It's not sorted, but that
# doesn't actually matter
print(calculate_checksum(out_blocks_p2))
