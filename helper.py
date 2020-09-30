from constants.toxic_mapping import VIOLATION_MAPPING


def handleViolations(violations=[]):
    if len(violations) == 0:
        return ""
    if len(violations) == 1:
        return VIOLATION_MAPPING[violations[0]]
    if len(violations) == 2 and (0 in violations and 1 in violations):
        return VIOLATION_MAPPING[1]
    else:
        response = ""
        for violation in violations[:-1]:
            if violation == 0 and 1 in violations:
                continue  # No need to have toxic and severely toxic
            response += VIOLATION_MAPPING[violation] + ", "
        response += "and " + VIOLATION_MAPPING[violations[-1]]
        return response
