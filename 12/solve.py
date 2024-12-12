import sys

from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Slice:
    color: str
    start: int
    end: Optional[int] = 0

@dataclass
class Blob:
    color: str
    perimeter: int = 0
    area: int = 0
    sides: int = 0
    current_slices: List[Slice] = field(default_factory=list)
    next_slices: List[Slice] = field(default_factory=list)

p1 = 0
p2 = 0
with open(sys.argv[1]) as f:
    current_blobs = []
    for line in map(str.strip, f):
        slices = []
        current = None

        # Create slices
        for i, v in enumerate(line):
            if current is None or current.color != v:
                if current is not None:
                    current.end = i
                    slices.append(current)
                current = Slice(color=v, start=i)

        # Finish the last slice
        if current is not None:
            current.end = len(line)
            slices.append(current)

        # Match slices to blobs
        next_blobs = []
        for s in slices:
            matching_blobs = []
            total_overlap = 0
            new_sides = 0
            for blob in current_blobs:
                if blob.color != s.color:
                    continue

                for ps in blob.current_slices:
                    overlap = max(0, min(s.end, ps.end) - max(s.start, ps.start))
                    if overlap > 0:

                        # New vertical sides - easy
                        if ps.start != s.start:
                            new_sides += 1
                        if ps.end != s.end:
                            new_sides += 1

                        if blob not in matching_blobs:
                            matching_blobs.append(blob)
                    total_overlap += overlap

            if len(matching_blobs) > 0:
                matched = matching_blobs[0]

                # merge matching_blobs
                for blob in matching_blobs[1:]:
                    matched.area += blob.area
                    matched.perimeter += blob.perimeter
                    matched.sides += blob.sides - 1
                    matched.current_slices.extend(blob.current_slices)
                    # We're working left-to-right in slices, so no need
                    # to extend next_slices

                    current_blobs.remove(blob)
                matched.perimeter += 2 + 2 * (s.end - s.start) - 2 * total_overlap
                matched.area += s.end - s.start
                matched.sides += new_sides
                matched.next_slices.append(s)
            else:
                # New blob
                matched = Blob(
                    color=s.color,
                    perimeter=2 + 2 * (s.end - s.start),
                    area=s.end-s.start,
                    sides=4,
                    next_slices=[s],
                )

            if matched not in next_blobs:
                next_blobs.append(matched)

        for blob in next_blobs:
            # New horizontal sides = ????
            # Work out line segments from current_slices and next_slices?

            blob.current_slices = blob.next_slices
            blob.next_slices = []

        for blob in current_blobs:
            if blob not in next_blobs:
                print("Blob finished", blob)
                p1 += blob.area * blob.perimeter
                p2 += blob.area * blob.sides
        current_blobs = next_blobs

    # All current blobs are now done
    for blob in current_blobs:
        print("Blob finished", blob)
        p1 += blob.area * blob.perimeter
        p2 += blob.area * blob.sides

print(p1)
print(p2)
