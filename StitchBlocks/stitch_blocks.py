import cv2
import os
import numpy as np
from numpy.lib.arraysetops import unique


def show_im(im, row, col):
  import matplotlib.pyplot as plt
  plt.figure()
  plt.imshow(im, cmap=plt.cm.gray)
  plt.title("row=%d, col=%d"%(row, col))
  plt.show()

def find_files_with_prefix_rec(root_path, prefix):
  file_path_list = []
  for dir_root, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
      if filename.startswith(prefix):
        file_path_list.append(os.path.join(dir_root, filename))
  return file_path_list

def get_row_col_idx(filepath, prefix):
  DELIMITER = '-'
  filename = os.path.basename(filepath)
  filename = os.path.splitext(filename)[0]
  assert prefix == filename[:len(prefix)]
  filename = filename[len(prefix):]
  col_idx, row_idx = filename.split(DELIMITER)
  return int(row_idx), int(col_idx)

def read_blocks_with_prefix(blocks_dir, prefix):
  file_path_list = find_files_with_prefix_rec(blocks_dir, prefix)
  blocks = []
  for file_path in file_path_list:
    row, col = get_row_col_idx(file_path, prefix)
    block = cv2.imread(file_path)
    # block = cv2.copyMakeBorder(block, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 255])
    blocks.append({"row_idx": row, "col_idx": col, "content": block})
    # show_im(block, row, col)
  return blocks

def stitch_blocks(blocks):
  # ims = sorted(ims, key=lambda x:(x["row"], x["col"]))

  # check if all blocks sizes are identical
  ref_block = blocks[0]["content"]
  block_height, block_width, num_channels = ref_block.shape
  assert all(block["content"].shape == ref_block.shape for block in blocks)

  # check if block indices are continuous
  unique_row_ids, row_unique_counts = unique([block["row_idx"] for block in blocks], return_counts=True)
  unique_col_ids, col_unique_counts = unique([block["col_idx"] for block in blocks], return_counts=True)
  num_block_rows = len(unique_row_ids)
  num_block_cols = len(unique_col_ids)
  assert all(x == row_unique_counts[0] for x in row_unique_counts)
  assert all(x == col_unique_counts[0] for x in col_unique_counts)
  assert num_block_rows == unique_row_ids[-1] + 1
  assert num_block_cols == unique_col_ids[-1] + 1

  # compute whole image size
  im_height = num_block_rows * block_height
  im_width = num_block_cols * block_width

  # allocate space for whole image
  whole_im = np.zeros((im_height, im_width, num_channels), dtype=ref_block.dtype)

  # stitch all blocks together
  for block in blocks:
    row_idx = block["row_idx"] * block_height
    col_idx = block["col_idx"] * block_width
    whole_im[row_idx:row_idx+block_height, col_idx:col_idx+block_width] = block["content"]

  return whole_im

def stitch_blocks_wrapper(blocks_dir, out_path):
  PREFIX = "7-"
  blocks = read_blocks_with_prefix(blocks_dir, PREFIX)
  whole_im = stitch_blocks(blocks)
  show_im(whole_im, 0, 0)
  cv2.imwrite(out_path, whole_im)

if __name__ == "__main__":
  blocks_dir = r"D:\TMP\Default"
  out_file_path = r"D:\TMP\2.jpeg"
  stitch_blocks_wrapper(blocks_dir, out_file_path)
