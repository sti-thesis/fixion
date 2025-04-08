def center_window(window, width, height):
    """
    Centers a tkinter window on the screen

    Args:
        window: The tkinter window to center
        width: Window width
        height: Window height
    """
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position coordinates
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's position
    window.geometry(f"{width}x{height}+{x}+{y}")