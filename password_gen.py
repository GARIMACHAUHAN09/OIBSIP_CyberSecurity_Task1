# password_gen.py
import string
import secrets

def ask_int(prompt, min_value=1, max_value=128):
    while True:
        try:
            n = int(input(prompt))
            if not (min_value <= n <= max_value):
                print(f"Enter a number between {min_value} and {max_value}.")
                continue
            return n
        except ValueError:
            print("Please enter a valid integer.")

def ask_yn(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer with y or n.")

def generate_password(length, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=False,
                      exclude_similar=True, ensure_each=True):
    # Character sets
    sets = []
    if use_lower:  sets.append(string.ascii_lowercase)
    if use_upper:  sets.append(string.ascii_uppercase)
    if use_digits: sets.append(string.digits)
    if use_symbols: sets.append("!@#$%^&*()-_=+[]{};:,.?/\\|`~")

    if not sets:
        raise ValueError("No character types selected.")

    # Optional: remove easily-confused chars
    if exclude_similar:
        confusing = set("Il1O0S5B8")
        sets = ["".join(ch for ch in s if ch not in confusing) for s in sets]

    pool = "".join(sets)
    if ensure_each and length < len(sets):
        raise ValueError(f"Length must be at least {len(sets)} to include each selected type.")

    # Guarantee at least one from each selected set
    password_chars = []
    if ensure_each:
        for s in sets:
            password_chars.append(secrets.choice(s))
        length -= len(sets)

    # Fill remaining
    for _ in range(length):
        password_chars.append(secrets.choice(pool))

    # Shuffle securely
    rng = secrets.SystemRandom()
    rng.shuffle(password_chars)
    return "".join(password_chars)

def main():
    print("=== Random Password Generator ===")
    length = ask_int("Enter password length (8-64): ", 8, 64)

    use_lower  = ask_yn("Include lowercase letters?")
    use_upper  = ask_yn("Include uppercase letters?")
    use_digits = ask_yn("Include digits?")
    use_symbols= ask_yn("Include symbols?")
    exclude    = ask_yn("Exclude look-alike characters (Il1O0S5B8)?")
    ensure     = ask_yn("Ensure at least one of each selected type?")

    try:
        pwd = generate_password(length, use_lower, use_upper, use_digits,
                                use_symbols, exclude_similar=exclude,
                                ensure_each=ensure)
        print("\nGenerated Password:\n", pwd)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
