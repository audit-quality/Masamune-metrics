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
    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    gas_count = 0
    informational_count = 0
    undetermined_count = 0
    unknown_count = 0
    codearena_labels = ['QA (Quality Assurance)', 'G (Gas Optimization)', '0 (Non-critical)', '1 (Low Risk)', '2 (Med Risk)', '3 (High Risk)']

    # Iterate through all findings to list high, medium, low
    for finding in existing_findings:
        labels = finding['labels']
        # Identify the finding severity information
        severity = ""
        for label in labels:
            if label.find("Severity: ") > -1: # for tob and yaudit and spearbit data
                severity = label[label.find("Severity: ") + len("Severity: "):]
                severity = severity.split(" ")[0] # only take the first word
            elif label in codearena_labels: # for tob and yaudit data
                severity = label
        match severity:
            case 'Critical':
                critical_count += 1
            case '3 (High Risk)':
                high_count += 1
            case 'High':
                high_count += 1
            case '2 (Med Risk)':
                medium_count += 1
            case 'Medium':
                medium_count += 1
            case '1 (Low Risk)':
                low_count += 1
            case 'Low':
                low_count += 1
            case 'G (Gas Optimization)':
                gas_count += 1
            case 'Gas':
                gas_count += 1
            case 'QA (Quality Assurance)':
                informational_count += 1
            case 'Informational':
                informational_count += 1
            case 'Undetermined':
                undetermined_count += 1
            case '0 (Non-critical)':
                undetermined_count += 1
            case _:
                # print(labels) # print unknown severity for debugging
                unknown_count += 1

    # Some reports don't use critical rating, so combine high and crit findings count
    critical_and_high_count = critical_count + high_count

    # Store other data of auditor totals
    audit_name = file_name.split("_")[0]
    total_count = len(existing_findings)
    unique_audits = count_audits(file_name)

    # Calculate the average findings per report
    crit_high_avg = critical_and_high_count/unique_audits
    crit_avg = critical_count/unique_audits
    high_avg = high_count/unique_audits
    med_avg = medium_count/unique_audits
    low_avg = low_count/unique_audits
    gas_avg = gas_count/unique_audits
    info_avg = informational_count/unique_audits
    undet_avg = undetermined_count/unique_audits
    unk_avg = unknown_count/unique_audits
    total_avg = total_count/unique_audits

    # Print data
    print_severities(critical_and_high_count, critical_count, high_count, medium_count, low_count, gas_count, informational_count, undetermined_count, unknown_count, total_count)
    print(">>>" + audit_name + " has " + str(unique_audits) + " unique audits")
    print_averages(crit_high_avg, crit_avg, high_avg, med_avg, low_avg, gas_avg, info_avg, undet_avg, unk_avg, total_avg)

    # Finally, write all data to CSV
    all_stats = [audit_name, str(critical_and_high_count), str(critical_count), str(high_count), str(medium_count), str(low_count), str(gas_count), str(informational_count), str(undetermined_count), str(unknown_count), str(total_count), str(unique_audits)]
    avg_stats = [str(crit_high_avg), str(crit_avg), str(high_avg), str(med_avg), str(low_avg), str(gas_avg), str(info_avg), str(undet_avg), str(unk_avg), str(total_avg)]
    combined_data = all_stats + [' '] + avg_stats
    csv_output_line = ','.join(combined_data) # join only works with strings, not ints
    with open(f"results.csv", "a") as f:
        f.write(csv_output_line + "\n")
        f.close()

def print_severities(crit_and_high, crit, high, med, low, gas, info, undetermined, unknown, total):
    print(str(crit_and_high) + " Critical and High findings or " + str(100 * crit_and_high/total) + "%")
    print(str(crit) + " Critical findings or " + str(100 * crit/total) + "%")
    print(str(high) + " High findings or " + str(100 * high/total) + "%")
    print(str(med) + " Medium findings or " + str(100 * med/total) + "%")
    print(str(low) + " Low findings or " + str(100 * low/total) + "%")
    print(str(gas) + " Gas findings or " + str(100 * gas/total) + "%")
    print(str(info) + " Info findings or " + str(100 * info/total) + "%")
    print(str(undetermined) + " Undetermined findings or " + str(100 * undetermined/total) + "%")
    print(str(unknown) + " Unknown findings or " + str(100 * unknown/total) + "%")
    print(str(total) + " total findings")
    print()

def print_averages(crit_and_high, crit, high, med, low, gas, info, undetermined, unknown, total):
    print("Average number of findings per audit:")
    print(str(crit_and_high) + " Critical and High findings per audit")
    print(str(crit) + " Critical findings per audit")
    print(str(high) + " High findings per audit")
    print(str(med) + " Medium findings per audit")
    print(str(low) + " Low findings per audit")
    print(str(gas) + " Gas findings per audit")
    print(str(info) + " Info findings per audit")
    print(str(undetermined) + " Undetermined findings per audit")
    print(str(unknown) + " Unknown findings per audit")
    print(str(total) + " total findings per audit")
    print()

def count_audits(file_name):
    try:
        with open("results/" + file_name, "r") as f:
            existing_findings = json.load(f)
    except FileNotFoundError:
        existing_findings = []

    all_reports = []
    # Iterate through all findings to list high, medium, low
    for finding in existing_findings:
        # Use the report url to identify the number of unique audits
        if 'html_url' in finding.keys():
            report_url = finding['html_url']
            # The codearena html link points to the specific issue, need to check only if report is unique
            if report_url.find("github.com/code-423n4/") > 0:
                report_url = report_url.split("/issues/")[0]
            if report_url not in all_reports: # this must be if, not else, to also handle c4 case
                all_reports.append(report_url)
        else:
            continue

    return len(all_reports)

def insert_csv_header():
    with open(f"results.csv", "w") as f:
        f.write("audit company, critical_and_high, critical, high, medium, low, gas, info, undetermined, unknown, total, audit count, BLANK, critical_and_high average, critical average, high average, medium average, low average, gas average, info average, undetermined average, unknown average, total average\n")
        f.close()

if __name__ == "__main__":
    insert_csv_header()
    severity_metrics("codearena_findings.json")
    severity_metrics("gitbook_docs.json")
    # severity_metrics("hacklabs_findings.json") # no severity data for hacklabs
    severity_metrics("immunefi_findings.json")
    severity_metrics("tob_findings.json")
    severity_metrics("yaudit_findings.json")
    severity_metrics("spearbit_findings.json")
    severity_metrics("dedaub_findings.json")
    severity_metrics("hacklabs_findings.json")
    severity_metrics("halborn_findings.json")
    severity_metrics("oak_security_findings.json")
    severity_metrics("slowmist_findings.json")
