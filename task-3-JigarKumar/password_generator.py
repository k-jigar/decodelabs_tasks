import secrets
import string
import math


def get_character_pool(use_letters: bool, use_digits: bool, use_symbols: bool) -> str:
    pool = ""
    if use_letters:
        pool += string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    return pool


def generate_password(length: int, pool: str) -> str:
    guaranteed = []

    if any(c in string.ascii_letters for c in pool):
        guaranteed.append(secrets.choice(string.ascii_letters))
    if any(c in string.digits for c in pool):
        guaranteed.append(secrets.choice(string.digits))
    if any(c in string.punctuation for c in pool):
        guaranteed.append(secrets.choice(string.punctuation))

    remaining_length = length - len(guaranteed)
    remaining = [secrets.choice(pool) for _ in range(remaining_length)]

    all_chars = guaranteed + remaining
    secrets.SystemRandom().shuffle(all_chars)

    return ''.join(all_chars)


def calculate_entropy(length: int, pool_size: int) -> float:
    if pool_size <= 0:
        return 0.0
    return round(length * math.log2(pool_size), 2)


def get_strength_label(entropy: float) -> str:
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


def get_crack_estimate(entropy: float) -> str:
    if entropy < 28:
        return "Instantly"
    elif entropy < 36:
        return "Minutes to hours"
    elif entropy < 60:
        return "Days to years"
    elif entropy < 100:
        return "Millions of years"
    else:
        return "Longer than the age of the universe"


def validate_length(raw: str) -> int:
    length = int(raw)
    if length < 4:
        raise ValueError("Minimum length is 4.")
    if length > 64:
        raise ValueError("Maximum length is 64 (NIST SP 800-63-4).")
    return length


def print_menu() -> None:
    print("\n+" + "-" * 40 + "+")
    print("|   DecodeLabs -- Password Generator    |")
    print("+" + "-" * 40 + "+")
    print("|  1. Generate a password               |")
    print("|  2. Generate multiple passwords       |")
    print("|  3. What makes a strong password?     |")
    print("|  4. Exit                              |")
    print("+" + "-" * 40 + "+")


def ask_options() -> tuple:
    print("\n  Character set options:")
    print("  [1] Letters + Digits (alphanumeric)")
    print("  [2] Letters + Digits + Symbols (maximum security)")
    print("  [3] Letters only")
    print("  [4] Digits only")

    choice = input("  Choose character set (1-4): ").strip()

    if choice == "1":
        return True, True, False
    elif choice == "2":
        return True, True, True
    elif choice == "3":
        return True, False, False
    elif choice == "4":
        return False, True, False
    else:
        print("  Invalid choice. Defaulting to Letters + Digits + Symbols.")
        return True, True, True


def display_password_report(password: str, pool: str) -> None:
    entropy = calculate_entropy(len(password), len(pool))
    strength = get_strength_label(entropy)
    crack_time = get_crack_estimate(entropy)

    print("\n" + "=" * 44)
    print("  GENERATED PASSWORD")
    print("=" * 44)
    print(f"  {password}")
    print("=" * 44)
    print(f"  Length      : {len(password)} characters")
    print(f"  Pool size   : {len(pool)} characters")
    print(f"  Entropy     : {entropy} bits  (E = L x log2(R))")
    print(f"  Strength    : {strength}")
    print(f"  Crack time  : {crack_time}")
    print(f"  Generator   : secrets.choice() [OS entropy]")

    if len(password) < 15:
        print(f"\n  WARNING: NIST SP 800-63-4 recommends minimum")
        print(f"  15 characters for high-security contexts.")
    print("=" * 44)


def show_education() -> None:
    print("\n" + "-" * 44)
    print("  WHAT MAKES A STRONG PASSWORD?")
    print("-" * 44)
    print("  Entropy formula: E = L x log2(R)")
    print("  L = password length")
    print("  R = character pool size")
    print()
    print(f"  {'LENGTH':<12} {'POOL':<10} {'ENTROPY':<12} {'CRACK TIME'}")
    print("-" * 44)

    examples = [
        (8,  62, "2 days"),
        (10, 62, "5 years"),
        (16, 62, "Millions of years"),
        (20, 95, "Age of universe"),
    ]

    for length, pool, crack in examples:
        entropy = round(length * math.log2(pool), 1)
        print(f"  {length:<12} {pool:<10} {entropy:<12} {crack}")

    print("-" * 44)
    print("  secrets module  : OS hardware entropy (secure)")
    print("  random module   : Mersenne Twister (NOT secure)")
    print("  ''.join(list)  : O(N) memory efficient")
    print("  password += c  : O(N^2) -- never do this")
    print("-" * 44)


def main() -> None:
    print("\n  DecodeLabs -- Password Generator v1.0")
    print("  Powered by: secrets module + OS entropy")
    print("  Standard  : NIST SP 800-63-4 (2024)")

    while True:
        print_menu()
        choice = input("  Enter choice (1-4): ").strip()

        if choice == "1":
            raw = input("  Password length (4-64): ").strip()
            try:
                length = validate_length(raw)
            except ValueError as e:
                print(f"\n  Error: {e}")
                continue

            use_letters, use_digits, use_symbols = ask_options()
            pool = get_character_pool(use_letters, use_digits, use_symbols)

            if not pool:
                print("\n  Error: No character set selected.")
                continue

            password = generate_password(length, pool)
            display_password_report(password, pool)

        elif choice == "2":
            raw_len = input("  Password length (4-64): ").strip()
            try:
                length = validate_length(raw_len)
            except ValueError as e:
                print(f"\n  Error: {e}")
                continue

            raw_count = input("  How many passwords? (1-20): ").strip()
            try:
                count = int(raw_count)
                if not 1 <= count <= 20:
                    raise ValueError
            except ValueError:
                print("\n  Invalid count. Please enter a number between 1 and 20.")
                continue

            use_letters, use_digits, use_symbols = ask_options()
            pool = get_character_pool(use_letters, use_digits, use_symbols)

            if not pool:
                print("\n  Error: No character set selected.")
                continue

            entropy = calculate_entropy(length, len(pool))
            strength = get_strength_label(entropy)

            print(f"\n  Generating {count} passwords | {strength} | {entropy} bits entropy\n")
            print("  " + "-" * 40)
            for i in range(count):
                pw = generate_password(length, pool)
                print(f"  {i + 1:>2}. {pw}")
            print("  " + "-" * 40)

        elif choice == "3":
            show_education()

        elif choice == "4":
            print("\n  Session closed. Stay secure.\n")
            break

        else:
            print("\n  Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()