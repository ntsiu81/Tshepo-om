# import json
# import subprocess
# import sys
# import os 

# def load_terraform_plan(plan_file):
#     try:
#         with open(plan_file, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         print(f"Error: Plan file '{plan_file}' not found")
#         sys.exit(1)
#     except json.JSONDecodeError:
#         print(f"Error: Invalid JSON in '{plan_file}'.")
#         sys.exit(1)
# def is_tags_only_change(plan):
#     if 'resource_changes' not in plan:
#         print("No resources chnages found in plan")
#         return False
#     for resource in plan['resource_changes']:
#         change = resource.get('change', {})
#         actions = change.get('actions', [])
#         if 'update' not in actions:
#             print(f"Resource {resource['address']} has non-update actions: {actions}")
#             return False
#         before = change.get('before', {})
#         after = change.get('after', {})
#         changed_keys = set(after.keys()) - set(before.keys()) | set(k for k in before if before[k] != after.get(k))
#         allowed_keys = {'tags', 'tags_all'}
#         if not changed_keys.issubset(allowed_keys):
#             print(f"Resource {resource['address']} modifies non-tag attributes: {changed_keys}")
#             return False
#     return True
# def apply_terraform(plan_file):
#     try:
#         result = subprocess.run(
#             ['terraform', 'apply', plan_file],
#             check=True,
#             capture_output=True,
#             text=True
#         )
#         print("Terraform apply successfull:")
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         print("Error applying Terraform plan:")
#         print(e.stderr)
#         sys.exit(1)
# def main(plan_file='tfplan-1.json'):
#     if not os.path.exists(plan_file):
#         print(f"Error Terraform plan file '{plan_file}' does not exists.")
#         sys.exit(1)
#     plan = load_terraform_plan(plan_file)

#     if is_tags_only_change(plan):
#         print(f"Plan only modifies tags. Proceeding with apply....")
#         apply_terraform('tfplan-1')
#     else:
#         print("Plan Contains non tag changes. terraform apply aborted")
#         sys.exit(1)
# if __name__ == '__main__':
#     main()

import json
import subprocess
import sys
import os
import glob

def load_terraform_plan(plan_file):
    try:
        with open(plan_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Plan file '{plan_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{plan_file}'.")
        return None

def is_tags_only_change(plan):
    if 'resource_changes' not in plan:
        print("No resource changes found in plan.")
        return False

    for resource in plan['resource_changes']:
        change = resource.get('change', {})
        actions = change.get('actions', [])

        if 'update' not in actions:
            print(f"Resource {resource['address']} has non-update actions: {actions}")
            return False

        before = change.get('before', {})
        after = change.get('after', {})
        changed_keys = set(after.keys()) - set(before.keys()) | set(k for k in before if before[k] != after.get(k))
        allowed_keys = {'tags', 'tags_all'}

        if not changed_keys.issubset(allowed_keys):
            print(f"Resource {resource['address']} modifies non-tag attributes: {changed_keys}")
            return False

    return True

def apply_terraform(plan_file_base):
    try:
        result = subprocess.run(
            ['terraform', 'apply', plan_file_base],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Applied {plan_file_base} successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error applying Terraform plan '{plan_file_base}':")
        print(e.stderr)

def main():
    json_files = glob.glob("*.json")
    if not json_files:
        print("No JSON plan files found in the current directory.")
        sys.exit(0)

    for json_file in json_files:
        print(f"\n--- Processing {json_file} ---")
        plan = load_terraform_plan(json_file)
        if plan is None:
            continue

        if is_tags_only_change(plan):
            print("Only tag changes detected. Applying plan...")
            plan_base = os.path.splitext(json_file)[0]  # Remove .json to get base name (e.g., tfplan-1)
            apply_terraform(plan_base)
        else:
            print("Non-tag changes detected. Skipping apply.")

if __name__ == '__main__':
    main()
