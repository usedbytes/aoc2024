import sys

with open(sys.argv[1]) as f:
    diskmap = f.read().strip()

checksum = 0
head_id = 0
n_files = (len(diskmap) + 1) // 2
tail_id = n_files
head_out_idx = 0
tail_cursor = n_files * 2

tail_remaining = 0

disk = []

for i, v in enumerate(diskmap):
    v = int(v)

    if i > tail_cursor:
        break

    if i % 2 == 0:
        # File

        # This file has already been partially moved, reduce size accordingly
        if head_id == tail_id:
            v = tail_remaining

        for j in range(v):
            checksum += head_out_idx * head_id
            head_out_idx += 1

        head_id += 1
    else:
        # Free space
        space_remaining = v

        while space_remaining > 0:
            if tail_remaining == 0:
                # No more file to move, get a new one
                tail_cursor -= 2
                tail_id -= 1

                # Tail reached head
                if tail_cursor <= i:
                    break

                tail_remaining = int(diskmap[tail_cursor])

            if tail_remaining == 0:
                break

            # Moving file to head_out_idx
            checksum += head_out_idx * tail_id
            head_out_idx += 1
            space_remaining -= 1
            tail_remaining -= 1

print(checksum)
