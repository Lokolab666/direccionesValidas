letters_s = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z"]
letters_s_upp = [letter.upper() for letter in letters_s]
numbers_s = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
specials_s = ["!", "#", "$", "%", "&", "'", "*", "+", "/", "=", "?", "ˆ", "_", "´", "{", "|", "}", "-", "[", "]"]
rule_dots = [".", "dot"]
rule_ats = ["@", "at"]
rule_line = ["-", "[", "]"]
last_message = []


def special_bracket(word):
    separate_bracket = word.split("[")
    separate_one = separate_bracket[1]
    separate_bracket_delimiter = separate_one.split("]")
    separate_two = separate_bracket_delimiter[0]
    for a, b in zip(rule_dots, rule_ats):
        if a == separate_two:
            return 1

        if b == separate_two:
            return 2

    return -1


def validate_character_local(v):
    for a, b in zip(letters_s, letters_s_upp):
        if a == v or b == v:
            return True

    for c in numbers_s:
        if c == v:
            return True

    for d in specials_s:
        if d == v:
            return True

    for a, b in zip(rule_dots, rule_ats):
        if a == v:
            return 3

        if b == v:
            return 4

    return False


def validate_character_domain(v):
    for a, b in zip(letters_s, letters_s_upp):
        if a == v or b == v:
            return True

    for c in numbers_s:
        if c == v:
            return True

    for a, b in zip(rule_dots, rule_ats):
        if a == v:
            return 3

        if b == v:
            return 4

    for a in rule_line:
        if a == v:
            return True

    return False


def validate_at(word):
    for i, mail in enumerate(word):
        if word[i] == "@":
            return True

    separate_bracket = word.split("[")
    delimiter_one = ''
    delimiter_two = ''
    delimiter_tree = ''
    delimiter_four = ''

    for i, characters in enumerate(separate_bracket):
        if i == 1:
            proof_one = separate_bracket[i]
            delimiter_one = proof_one.split("]")
        if i == 2:
            proof_two = separate_bracket[i]
            delimiter_two = proof_two.split("]")
        if i == 3:
            proof_tree = separate_bracket[i]
            delimiter_tree = proof_tree.split("]")
        if i == 4:
            proof_four = separate_bracket[i]
            delimiter_four = proof_four.split("]")

    for a, b in zip(rule_dots, rule_ats):
        if a == delimiter_two[0] and b == delimiter_one[0] or a == delimiter_tree or a == delimiter_four:
            separate_domain_var = word.split("[at]")
            separate_domain = separate_domain_var[1]
            last_message.append(separate_domain)
            return separate_domain


def validate_dot(word):
    separate_bracket = word.split("[")
    separate_one = separate_bracket[1]
    separate_bracket_delimiter = separate_one.split("]")
    separate_two = separate_bracket_delimiter[0]
    for a, b in zip(rule_dots, rule_ats):
        if a == separate_two:
            return 1

        if b == separate_two:
            return True

    pass


def validate_domain(word, k):
    if k == 1:
        separate_var = word.split("@")
        separate = separate_var[1]

        for i, v in enumerate(separate):
            if len(word) >= 63:
                last_message.append("Domain-part is longer than 63 characters")
                break
            else:
                if validate_character_domain(v) == 3:
                    if separate[i - 1] == separate[i]:
                        last_message.append("repeat character dot")
                        break
                if separate[i - 1] == '.' and separate[i] == '@':
                    last_message.append("repeat character continue -at")
                    break

                if validate_character_domain(v) == 4:
                    validate_domain(separate)
                    break

                if validate_character_domain(v):
                    last_message.append("OK 2")
                else:
                    last_message.append("Domain-part with an invalidate character")
                    break
    elif k == 2:
        for i, v in enumerate(word):
            if len(word) >= 63:
                last_message.append("Domain-part is longer than 63 characters")
                break
            else:
                if validate_character_domain(v) == 3:
                    if word[i - 1] == word[i]:
                        last_message.append("repeat character dot")
                        break
                if word[i - 1] == '.' and word[i] == '@':
                    last_message.append("repeat character continue -at")
                    break

                if validate_character_domain(v) == 4:
                    validate_domain(word)
                    break

                if validate_character_domain(v):
                    last_message.append("si cha dom")
                else:
                    last_message.append("Domain-part with an invalidate character")
                    break

    return -1


def validate(word):
    count_at = word.count('@')
    if count_at > 1 or word.find('@') == -1:
        last_message.append("Error. Ats is upper to 1")
    else:
        if validate_at(word):
            last_message.append("Yeah, this mail contains at")
            for i, v in enumerate(word):
                if len(word) >= 64:
                    last_message.append("Local-part is longer than 64 characters")
                    break
                else:
                    if validate_character_local(v) == 3:
                        if word[i - 1] == word[i]:
                            last_message.append("repeat character dot")
                            break
                    if word[i - 1] == '.' and word[i] == '@':
                        last_message.append("repeat character continue -at")
                        break

                    if validate_character_local(v) == 4:
                        last_message.append("at 1")
                        validate_domain(word, 1)
                        break

                    if word[i] == '[at':
                        if special_bracket(word) == 2:
                            last_message.append("zero")
                            validate_domain(validate_at(word), 2)
                        break

                    if validate_character_local(v):
                        last_message.append("OK")
                    else:
                        last_message.append("Local-part with an invalidate character")
                        break

        else:
            last_message.append('No, this mail no contains at')


def data_input():
    mail_val = input("Mail to validate: ")

    validate(mail_val)


def validate_mail():
    last = [last_message.pop(), last_message[-2]]
    # print(last)
    return last

