import sys

with open(sys.argv[1]) as f:
    diskmap = f.read().strip()

blocks = []

# Build a list of blocks
file_id = 0
start_idx = 0
for i, v in enumerate(diskmap):
    size = int(v)
    if i % 2 == 0:
        blocks.append([file_id, start_idx, size])
        file_id += 1
    else:
        blocks.append([None, start_idx, size])
    start_idx += size

# Compact
out_blocks = []
for i, block in enumerate(blocks):
    file_id, start_idx, size = block
    if file_id is not None:
        # Files always move over as-is
        out_blocks.append(block)
    else:
        # Space, fill it
        space_remaining = size
        while space_remaining > 0:
            # Find a block to move
            to_move = next(filter(lambda b: b[0] is not None, reversed(blocks)))
            move_id, move_start, move_size = to_move

            # Only move backwards
            if move_start <= start_idx:
                break

            if space_remaining >= move_size:
                # Move whole block
                out_blocks.append([move_id, start_idx, move_size])
                space_remaining -= move_size
                start_idx += move_size

                # Now this block is a space
                to_move[0] = None
            else:
                # Need to split block
                out_blocks.append([move_id, start_idx, space_remaining])
                to_move[2] -= space_remaining
                space_remaining = 0

checksum = 0
for file_id, start_idx, size in out_blocks:
    n = size * (start_idx + start_idx + size - 1) // 2
    checksum += n * file_id
print(checksum)
