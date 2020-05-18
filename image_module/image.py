def show_information(frame):
    """Prints in console some information about the file

        Parameters:
          frame: Data of the file as numpy array

    """

    rows = frame.shape[0]
    cols = frame.shape[1]

    total_pixels = rows * cols

    total_byte = total_pixels // 3

    print(f'Rows: {rows}')
    print(f'Columns: {cols}')
    print(f'Total of pixels: {total_pixels}')
    print(f'Number of bytes that can be hidden: {total_byte}')
