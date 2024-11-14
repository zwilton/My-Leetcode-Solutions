# Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
# The overall run time complexity should be O(log (m+n)).
#
# Run by calling findMedianSortedArrays of the Solution class.
#
# The Approach is to split each of the 2 sorted lists into 3rds. By comparing the smallest and largest of each third
# Against the 3rds in the other list, we can deduce that each of the 3rds has some x number of elements definately
# smaller and some y numebr of elements definately larger.
# If x or y is more than half of the current elements for a given 3rd, we know that we can throw out that entire
# segment of elements.
# We follow this process recursively.
# There is some bookeeping to do to keep track of the target element. We are looking for the median of the starting lists,
# but after removing elements, the target element will likely no longer be the median of what remains.

import math


class Solution:
    class Slice:
        def __init__(self, nums, list_num, start, end):
            self.nums = nums
            self.list_num = list_num
            self.start = start
            self.end = end
            self.num_elements = end - start
            self.num_elements_less_than = 0
            self.num_elements_greater_than = 0

        def compare_to_another_slice(self, other_slice):
            self_largest = self.nums[self.end - 1]
            self_smallest = self.nums[self.start]
            other_largest = other_slice.nums[other_slice.end - 1]
            other_smallest = other_slice.nums[other_slice.start]
            # If everything in our slice is smaller than everything in the other slice.
            if self_largest <= other_smallest:
                self.num_elements_greater_than += other_slice.num_elements
                other_slice.num_elements_less_than += self.num_elements
            # If everything in our silce is larger than everything in the other slice.
            elif self_smallest >= other_largest:
                self.num_elements_less_than += other_slice.num_elements
                other_slice.num_elements_greater_than += self.num_elements

        def __str__(self):
            return f"list: {self.nums}, list_num: {self.list_num}, start: {self.start}, end:{self.end}, slice{self.nums[self.start:self.end]} "

    def findMedianSortedArrays(self, nums1, nums2) -> float:
        if (len(nums1) + len(nums2)) % 2 == 0:
            even_num = 1
        else:
            even_num = 0
        return self._recursiveHelper(nums1, nums2, 0, len(nums1), 0, len(nums2), 0, even_num)

    def _recursiveHelper(self, nums1, nums2, start1: [int], end1: [int], start2: [int], end2: [int], offset: [float],
                         even_num: [int]):
        num_elements1 = end1 - start1
        num_elements2 = end2 - start2
        total_num_elements = num_elements1 + num_elements2
        # Base Case 1 is either of the lists is empty or has had all its elements eliminated as possibilities.
        if num_elements1 <= 0:
            return self._baseCase(nums2, start2, end2, offset, even_num)
        elif num_elements2 <= 0:
            return self._baseCase(nums1, start1, end1, offset, even_num)
        # Base Case 2 is that we started with an even number of elements and now have 1 left in each list. Both are needed to calculate the median.
        if even_num == 1 and num_elements1 == 1 and num_elements2 == 1:
            return (nums1[start1] + nums2[start2]) / 2
        # Recursive Case is to split each list in to 3 and see which sections can be eliminated as possibilities.
        # Split into 3 and count how many elements are greater than or less than the respcitive thirds.
        slices = self._createSlices(nums1, nums2, start1, end1, start2, end2)
        for i, slice1 in enumerate(slices):
            for slice2 in slices[i + 1:]:
                slice1.compare_to_another_slice(slice2)
        # Remove any slices that definately do not have the median.
        right_median_ind = math.floor(total_num_elements / 2) + math.floor(offset + .5 * even_num)
        # If there were an even number of elements to start out, we need to grab 2 numbers. Otherwise, its the same element.
        left_median_ind = right_median_ind - even_num

        for slice in slices:
            # Check if any of the slices are definately to the left of the left median.
            if slice.num_elements_greater_than >= total_num_elements - left_median_ind:
                offset -= .5 * slice.num_elements
                if slice.list_num == 1:
                    start1 = max(start1, slice.end)
                else:
                    start2 = max(start2, slice.end)
            # Check if any of the slices are definately to the right of the right median.
            if slice.num_elements_less_than >= right_median_ind + 1:
                offset += .5 * slice.num_elements
                if slice.list_num == 1:
                    end1 = min(end1, slice.start)
                else:
                    end2 = min(end2, slice.start)
        return self._recursiveHelper(nums1, nums2, start1, end1, start2, end2, offset, even_num)

    def _baseCase(self, nums, start: [int], end: [int], offset: [int], even_num: [int]):
        num_elements = end - start
        median_index = start + math.floor(num_elements / 2) + math.floor(offset + .5 * even_num)
        if even_num == 0:
            return nums[median_index]
        else:
            return (nums[median_index] + nums[median_index - 1]) / 2

    def _createSlices(self, nums1, nums2, start1, end1, start2, end2):
        # Calculate the indice locations to split the arrays into 3.
        nums1_split1, nums1_split2 = self._calculate_split_indices(start1, end1)
        nums2_split1, nums2_split2 = self._calculate_split_indices(start2, end2)
        slices = []
        slices.append(self.Slice(nums1, 1, start1, nums1_split1))
        slices.append(self.Slice(nums1, 1, nums1_split1, nums1_split2))
        slices.append(self.Slice(nums1, 1, nums1_split2, end1))
        slices.append(self.Slice(nums2, 2, start2, nums2_split1))
        slices.append(self.Slice(nums2, 2, nums2_split1, nums2_split2))
        slices.append(self.Slice(nums2, 2, nums2_split2, end2))
        # Remove any slices that do not have elements in them, ie. one list had < 3 elements to start.
        for slice in slices[:]:
            if slice.num_elements == 0:
                slices.remove(slice)
        return slices

    def _calculate_split_indices(self, start, end):
        num_elements = end - start
        split1 = start + math.floor(num_elements / 3)
        split2 = start + math.floor(2 * num_elements / 3)
        return split1, split2

