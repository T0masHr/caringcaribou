import argparse
from caringcaribou.utils.can_actions import CanActions
import can
import time

def proxy_traffic(source_interface, target_interface, duration):
    """
    Proxies CAN traffic from source_interface to target_interface for a specified duration.

    :param source_interface: Source CAN interface
    :param target_interface: Target CAN interface
    :param duration: Duration in seconds to run the proxy
    """
    source_bus = can.Bus(source_interface)
    target_bus = can.Bus(target_interface)
    start_time = time.time()
    end_time = start_time + duration

    print(f"Proxying CAN traffic from {source_interface} to {target_interface} for {duration} seconds (press Ctrl+C to exit)")

    try:
        while time.time() < end_time:
            msg = source_bus.recv(0.1)
            if msg:
                target_bus.send(msg)
    except KeyboardInterrupt:
        print("\nProxying stopped by user.")
    finally:
        source_bus.shutdown()
        target_bus.shutdown()

def parse_args(args):
    """
    Argument parser for the proxy module.

    :param args: List of arguments
    :return: Argument namespace
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog="caringcaribou proxy",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="CAN traffic proxy module for CaringCaribou")
    parser.add_argument("-s", "--source",
                        required=True,
                        help="Source CAN interface")
    parser.add_argument("-t", "--target",
                        required=True,
                        help="Target CAN interface")
    parser.add_argument("-d", "--duration",
                        type=float,
                        required=True,
                        help="Duration in seconds to run the proxy")
    return parser.parse_args(args)

def module_main(args):
    """
    Proxy module main wrapper.

    :param args: List of module arguments
    """
    args = parse_args(args)
    proxy_traffic(args.source, args.target, args.duration)