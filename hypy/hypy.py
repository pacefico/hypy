#!/usr/bin/env python3
# coding: utf-8

import configparser
import hvclient
import click
import base64
import time

@click.group()
@click.option('--host', default='', help='Host')
@click.option('--domain', default='', help='Domaing')
@click.option('--username', default='', help='Username')
@click.option('--password', default='', help='Password')
@click.pass_context
def main(ctx, host, domain, username, password):
    """
    Multiplataform Hyper-V Manager using Python and FreeRDP
    """
    ctx.obj = { "host":host, "domain":domain, "user":username, "pass":password }
    load_config(ctx.obj)


@main.command(help='List virtual machines and its indexes')
@click.option('--sync', '-s', is_flag=True, help='Syncronize with server updating local cache')
def list(sync):
    hvclient.update_all_cache(sync)
    hvclient.list_vms()


@main.command(help='List virtual machine snapshots')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
def snaps(name, index):
    hvclient.list_vm_snaps(int(index), name)


@main.command(help='List and set network adpater configuration from vm')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--setswitch', '-s', default="", help='Vm´s name')
@click.option('--tbefore', '-b', default=3, help='Time to wait in seconds before start')
@click.option('--tafter', '-a', default=3, help='Time to wait in seconds after completed')
def network(name, index, setswitch, tbefore, tafter):
    time.sleep(tbefore)
    if setswitch != "":
        hvclient.set_vm_switch(int(index), setswitch, name)
        time.sleep(tafter)

    hvclient.get_vm_network(int(index), name)


@main.command(help='List hyper-v switches available')
def switches():
    hvclient.load_switches()


@main.command(help='Restore virtual machine snapshot by name or index')
@click.argument('snap_name')
@click.option('--name', '-n', default="", help='Vm´s name to be restored')
@click.option('--force', '-f', is_flag=True, help='Forces a restore and start if necessary')
@click.option('--cache', '-c', is_flag=True, help='For use cache file based')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def restore(snap_name, name, force, cache, index, asjob, waitjob):
    hvclient.restore_vm_snap(index, snap_name, vm_name=name, force=force, no_cache=cache, asjob=asjob, waitjob=waitjob)


@main.command(help="Delete a machine's snapshot by name using vm´s name")
@click.option('--snap', '-s', help='snap name ')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('-r', is_flag=True, help="Remove snapshot's children as well")
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def delete(snap, name, r, index, asjob, waitjob):
    hvclient.remove_vm_snapshot(index, snap, r, name, asjob, waitjob)


@main.command(help="Create a new snapshot with vm's current state using vm´s name")
@click.option('--snap', '-s', help='snap name ')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def create(snap, name, index, asjob, waitjob):
    hvclient.create_vm_snapshot(int(index), snap, name, asjob, waitjob)


@main.command(help="Connect to virtual machine identified by index")
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
def connect(name, index):
    hvclient.connect(int(index), vm_name=name)


@main.command(help='Start virtual machine identified by it´s name')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def start(name, index, asjob, waitjob):
    hvclient.start_vm(int(index), name, asjob, waitjob)


@main.command(help='Put virtual machine in saved state by it´s name')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def save(name, index, asjob, waitjob):
    hvclient.save_vm(int(index), name, asjob, waitjob)


@main.command(help='Put all virtual machines in saved state for except the ones in the whitelist')
@click.option('--whitelist', '-w', default="", help='Whitelist for Vm´s name that should not be saved')
def save_all_vms(whitelist):
    hvclient.save_all_vms(whitelist)


@main.command(help='Pause virtual machine identified by it´s name')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
def pause(name, index):
    hvclient.pause_vm(index, name)


@main.command(help='Resume (paused) virtual machine identified by it´s name')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def resume(name, index, asjob, waitjob):
    hvclient.resume_vm(int(index), name, asjob, waitjob)


@main.command(help='Stop virtual machine identified by its name')
@click.option('--name', '-n', default="", help='Vm´s name')
@click.option('--force', '-f', is_flag=True, help='Hyper-V gives the guest five minutes to save data, then forces a shutdown')
@click.option('--index', '-i', default=-1, help='Index optional for vm')
@click.option('--asjob', '-j', is_flag=True, help='Execute as a powershell job')
@click.option('--waitjob', '-w', is_flag=True, help='Wait job completion. When used with --asjob')
def stop(name, force, index, asjob, waitjob):
    hvclient.stop_vm(index, force, name, asjob, waitjob)


def load_config(ctx=None):
    """
    Read config file and sends the resultant dict to setup hvclient
    TODO: Validate options
    """
    try:
        config = configparser.ConfigParser()
        config.read('hypy.conf')

        credentials = config['credentials']

        username = bytes.decode(base64.b64decode(credentials['user'].encode())) if ctx == None or ctx['user'] == '' else ctx['user']
        password = bytes.decode(base64.b64decode(credentials['pass'].encode())) if ctx == None or ctx['pass'] == '' else ctx['pass']
        domain = credentials['domain'] if ctx == None or ctx['domain'] == '' else ctx['domain']
        host = credentials['host'] if ctx == None or ctx['host'] == '' else ctx['host']

        configuration = {'user': username,
                         'pass': password,
                         'domain': domain,
                         'host': host}

        options = config['options']

        configuration['cache_file'] = options['cache_file']
        configuration['sync_interval'] = options['sync_interval']

        hvclient.setup(configuration)

    except KeyError:
        print ("\n Please, configure your credentials file - hypy.conf")
        exit()


if __name__ == "__main__":
    main()
    exit(0)
