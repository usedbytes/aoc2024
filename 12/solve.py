import itertools
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

def count_horizontal_sides(blob):
    # Take the slices from this line and the previous line
    # Sort the start/end indices into a single list
    # Then, each pair represents a side along the boundary:
    # Consider:
    #   AAAAA
    #   AAOOO
    # Indices: (0, 5), (0, 2)
    # Sorted: 0, 0, 2, 5
    # Pairs: (0, 0), (2, 5)
    # (0, 0) has length 0, so doesn't count
    # (2, 5) is a horizontal side (above OOO)
    points = []
    sides = 0
    for s in blob.current_slices:
        points.append(s.start)
        points.append(s.end)
    for s in blob.next_slices:
        points.append(s.start)
        points.append(s.end)
    points.sort()

    for a, b in itertools.batched(points, n=2):
        if a != b:
            sides += 1

    return sides

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
            start_match = False
            end_match = False
            for blob in current_blobs:
                if blob.color != s.color:
                    continue

                for ps in blob.current_slices:
                    overlap = max(0, min(s.end, ps.end) - max(s.start, ps.start))
                    if overlap > 0:
                        if ps.start == s.start:
                            start_match = True
                        if ps.end == s.end:
                            end_match = True

                        if blob not in matching_blobs:
                            matching_blobs.append(blob)
                    total_overlap += overlap

            if len(matching_blobs) > 0:
                matched = matching_blobs[0]

                if not start_match:
                    # This slice's start doesn't line up with any blobs
                    # so it forms a new vertical side
                    matched.sides += 1
                if not end_match:
                    # The same, but for the end of the slice
                    matched.sides += 1

                # merge matching_blobs
                for blob in matching_blobs[1:]:
                    matched.area += blob.area
                    matched.perimeter += blob.perimeter
                    matched.sides += blob.sides
                    matched.current_slices.extend(blob.current_slices)
                    # We're working left-to-right in slices, so no need
                    # to extend next_slices

                    current_blobs.remove(blob)
                matched.perimeter += 2 + 2 * (s.end - s.start) - 2 * total_overlap
                matched.area += s.end - s.start
                matched.next_slices.append(s)
            else:
                # New blob
                matched = Blob(
                    color=s.color,
                    perimeter=2 + 2 * (s.end - s.start),
                    area=s.end-s.start,
                    sides=2,
                    next_slices=[s],
                )

            if matched not in next_blobs:
                next_blobs.append(matched)

        for blob in next_blobs:
            blob.sides += count_horizontal_sides(blob)

            blob.current_slices = blob.next_slices
            blob.next_slices = []

        for blob in current_blobs:
            if blob not in next_blobs:
                blob.sides += count_horizontal_sides(blob)
                p1 += blob.area * blob.perimeter
                p2 += blob.area * blob.sides
        current_blobs = next_blobs

    # All current blobs are now done
    for blob in current_blobs:
        blob.sides += count_horizontal_sides(blob)
        p1 += blob.area * blob.perimeter
        p2 += blob.area * blob.sides

print(p1)
print(p2)
