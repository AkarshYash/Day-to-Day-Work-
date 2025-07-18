import re

def check_password_strength(password):
    strength = 0
    remarks = ""

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        remarks += "- Password should be at least 8 characters long.\n"

    # Check lowercase
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        remarks += "- Add lowercase letters.\n"

    # Check uppercase
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        remarks += "- Add uppercase letters.\n"

    # Check digits
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        remarks += "- Add numbers.\n"

    # Check special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    else:
        remarks += "- Add special characters like !, @, #, etc.\n"

    # Output result
    if strength == 5:
        return "🟢 Strong Password!", remarks
    elif 3 <= strength < 5:
        return "🟡 Moderate Password.", remarks
    else:
        return "🔴 Weak Password!", remarks

if __name__ == "__main__":
    print("🔒 Password Strength Checker")
    user_pass = input("Enter your password: ")
    status, tips = check_password_strength(user_pass)
    print("\nResult:", status)
    if tips:
        print("Suggestions:\n" + tips)
