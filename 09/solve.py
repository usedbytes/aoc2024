import sys

with open(sys.argv[1]) as f:
    diskmap = f.read().strip()

checksum = 0
head_id = 0
n_files = (len(diskmap) + 1) // 2
tail_id = n_files
head_idx = 0
tail_idx = n_files * 2

print(f"{n_files=}, {tail_id=}, {tail_idx=}")

tail_remaining = 0

disk = []

for i, v in enumerate(diskmap):
    v = int(v)
    print(disk)
    if i % 2 == 0:
        # File
        print(f"file {head_idx=}, {head_id=}, size={v}")
        for j in range(int(v)):
            checksum += head_idx * head_id
            disk.append(head_id)
            head_idx += 1
        head_id += 1
    else:
        # Free space
        space_remaining = v
        print(f"space {space_remaining}, {tail_remaining=}, {tail_idx=}, {head_idx=}")
        while space_remaining > 0:
            if tail_remaining == 0:
                if head_idx >= tail_idx:
                    break
                tail_idx -= 2
                tail_id -= 1
                tail_remaining = int(diskmap[tail_idx])

                print(f"get tail file: {tail_idx=}, {tail_id=}, size={tail_remaining}")

            if tail_remaining == 0:
                break

            checksum += head_idx * tail_id
            disk.append(tail_id)
            head_idx += 1
            space_remaining -= 1
            tail_remaining -= 1

print(checksum)
print(disk)
