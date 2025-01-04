Pre Processing code

def preprocess_image(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize the frame to 64x64 if it's not already
    resized_frame = cv2.resize(gray_frame, (64, 64))
    
    # Normalize the frame (if required by the model)
    normalized_frame = resized_frame.astype(np.float32) / 255.0
    
    # Expand dimensions to add channel for grayscale (1 channel)
    expanded_frame = np.expand_dims(normalized_frame, axis=-1)
    
    # Convert grayscale to 3 channels by duplicating the grayscale channel
    rgb_frame = np.concatenate([expanded_frame] * 3, axis=-1)
    
    # Convert to 8-bit unsigned integer (0-255) format required by PIL
    rgb_frame = (rgb_frame * 255).astype(np.uint8)
    
    # Add batch dimension (if needed by the model)
    batch_frame = np.expand_dims(rgb_frame, axis=0)
    
    return batch_frame

    
