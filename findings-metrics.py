# Parse JSON findings and output metrics
import os
import json

def severity_metrics(file_name):
    try:
        with open("results/" + file_name, "r") as f:
            existing_findings = json.load(f)
    except FileNotFoundError:
        existing_findings = []

    print(file_name)

    # initialize all finding severity counters
    informational_count = 0
    gas_count = 0
    low_count = 0
    medium_count = 0
    high_count = 0
    critical_count = 0
    undetermined_count = 0
    unknown_count = 0

    # Iterate through all findings to list high, medium, low
    for finding in existing_findings:
        labels = finding['labels']
        # Identify the finding severity information
        severity = ""
        for label in labels:
            if label.find("Severity: ") > -1:
                severity = label[label.find("Severity: ") + len("Severity: "):]
        match severity:
            case 'Informational':
                informational_count += 1
            case 'Gas':
                gas_count += 1
            case 'Low':
                low_count += 1
            case 'Medium':
                medium_count += 1
            case 'High':
                high_count += 1
            case 'Critical':
                critical_count += 1
            case 'Undetermined':
                undetermined_count += 1
            case _:
                unknown_count += 1

    print_severities(informational_count, gas_count, low_count, medium_count, high_count, critical_count, undetermined_count, unknown_count, len(existing_findings))

def print_severities(info, gas, low, med, high, crit, undetermined, unknown, total):
    print(str(info) + " Info findings or " + str(100 * info/total) + "%")
    print(str(gas) + " Gas findings or " + str(100 * gas/total) + "%")
    print(str(low) + " Low findings or " + str(100 * low/total) + "%")
    print(str(med) + " Medium findings or " + str(100 * med/total) + "%")
    print(str(high) + " High findings or " + str(100 * high/total) + "%")
    print(str(crit) + " Critical findings or " + str(100 * crit/total) + "%")
    print(str(undetermined) + " Undetermined findings or " + str(100 * undetermined/total) + "%")
    print(str(unknown) + " Unknown findings or " + str(100 * unknown/total) + "%")
    print(str(total) + " total findings")
    print()

if __name__ == "__main__":
    severity_metrics("codearena_findings.json")
    severity_metrics("gitbook_docs.json")
    severity_metrics("hacklabs_findings.json")
    severity_metrics("immunefi_findings.json")
    severity_metrics("tob_findings.json")
    severity_metrics("yaudit_findings.json")