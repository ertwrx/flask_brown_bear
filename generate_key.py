import secrets

def generate_secret_key():
    """
    Generates a cryptographically strong random string suitable for use as a Flask SECRET_KEY.

    Returns:
        str: A 64-character hexadecimal string.
    """
    return secrets.token_hex(32)  # 32 bytes * 2 characters per byte (hex) = 64 characters

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:")
    print(secret_key)

    #  Optionally, you can write it to a .env file (if you're using one)
    #  Make sure not to commit the .env file to your repository!
    # with open(".env", "a") as f:
    #     f.write(f"SECRET_KEY={secret_key}\n")
    # print("\nSecret key appended to .env (if it exists).  DO NOT COMMIT .env!")
