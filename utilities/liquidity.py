import os
import json
import logging
import subprocess

from utilities.external_services import sending_net_liquidity_alert_to_discord

logger = logging.getLogger()


def run_liquidty_calculations(update_type='TGA'):
    allowed_values = ['TGA', 'RRP', 'WALCL']
    if update_type not in allowed_values:
        raise ValueError(f"Invalid value for update_type. Allowed values are {allowed_values}")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = '{}/{}'.format(root_dir, 'liquidity/net-liquidity.ps1')
    # For mac
    # subprocess.run(['/usr/local/bin/pwsh', '-File', script_path])
    # for ubuntu
    subprocess.run(['/usr/bin/pwsh', '-File', script_path])

    # The path to the JSON file
    liquidity_file_path = 'liquidity_data.json'
    last_data_file_path = 'last_datapoint.json'
    spx_fair_value_path = 'spx_fair_value.txt'
    fed_liquidity_path = 'fed_liquidity.txt'

    # liquidity_file_path = '../liquidity/liquidity_data.json'
    # last_data_file_path = '../liquidity/last_datapoint.json'
    # spx_fair_value_path = '../liquidity/spx_fair_value.txt'
    # fed_liquidity_path = '../liquidity/fed_liquidity.txt'

    if os.path.exists(liquidity_file_path):
        with open(liquidity_file_path) as user_file:
            parsed_json = json.load(user_file)

        latest_datapoint = parsed_json[len(parsed_json) - 1]

    # Check if the file exists
    if os.path.exists(last_data_file_path):
        # Open the file in read mode
        with open(last_data_file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
        last_datapoint = data
    else:
        print(f"The file {last_data_file_path} does not exist.")
        last_datapoint = parsed_json[len(parsed_json) - 2]

    # Open the file in write mode
    with open(last_data_file_path, 'w') as file:
        # Write the data to the file
        json.dump(latest_datapoint, file)

    final_output = latest_datapoint
    if 'WALCL' in update_type:
        final_output['fed_change'] = round((latest_datapoint['fed'] - last_datapoint['fed']) * (10 ** -9), 3)
    if 'TGA' in update_type:
        final_output['tga_change'] = round((latest_datapoint['tga'] - last_datapoint['tga']) * (10 ** -9), 3)
    if 'RRP' in update_type:
        final_output['rrp_change'] = round((latest_datapoint['rrp'] - last_datapoint['rrp']) * (10 ** -9), 3)

    final_output['net_liquidity_change'] = round((latest_datapoint['net_liquidity'] - last_datapoint['net_liquidity']) * (10 ** -9), 3)
    final_output['fed'] = round(final_output['fed'] * (10 ** -9), 3)
    final_output['rrp'] = round(final_output['rrp'] * (10 ** -9), 3)
    final_output['tga'] = round(final_output['tga'] * (10 ** -9), 3)
    final_output['net_liquidity'] = round(final_output['net_liquidity'] * (10 ** -9), 3)
    print(f'discord message: {final_output}')
    sending_net_liquidity_alert_to_discord(final_output)

    if 'TGA' in update_type:
        with open(spx_fair_value_path, 'r') as spx_file:
            link_to_spx_fair_value = spx_file.readline().strip()
        print(f'discord message: {link_to_spx_fair_value}')
        sending_net_liquidity_alert_to_discord(link_to_spx_fair_value)
        with open(fed_liquidity_path, 'r') as liquidity_file:
            link_to_fed_liquidity = liquidity_file.readline().strip()
        print(f'discord message: {link_to_fed_liquidity}')
        sending_net_liquidity_alert_to_discord(link_to_fed_liquidity)


if __name__ == "__main__":
    run_liquidty_calculations()
