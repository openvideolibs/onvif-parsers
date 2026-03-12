"""Example to fetch pullpoint events."""

import argparse
import asyncio
import datetime
import os.path
import pprint
import socket
import sys
import typing
from types import TracebackType

import onvif
from aiohttp import web

import onvif_parsers
import onvif_parsers.errors


def get_local_ip() -> str | None:
    """Try to get the local machine IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


class OnvifEventReceiver:
    """ONVIF event receiver testing class."""

    @staticmethod
    async def run(args: argparse.Namespace) -> None:
        """Run the event receiver."""
        async with OnvifEventReceiver(args):
            pass

    def __init__(self, args: argparse.Namespace) -> None:
        """Create the event receiver."""
        self.args = args
        self.cam = onvif.ONVIFCamera(
            args.host,
            args.port,
            args.username,
            args.password,
            wsdl_dir=f"{os.path.dirname(onvif.__file__)}/wsdl/",
        )
        self.manager: onvif.NotificationManager | None = None
        self.runner: web.AppRunner | None = None

    async def __aenter__(self) -> None:
        """Start the receiver."""
        await self.cam.update_xaddrs()

        capabilities = await self.cam.get_capabilities()
        print("===== Camera Capabilities =====")
        pprint.pprint(capabilities)
        print()

        if self.args.notification:
            await self.webhook()
        else:
            await self.pullpoint()

    async def __aexit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop the receiver."""
        del type_, value, traceback
        if self.manager:
            await self.manager.shutdown()
        if self.runner:
            await self.runner.cleanup()
        await self.cam.close()

    def subscription_lost(self) -> None:
        """Callback when the pullpoint subscription is lost."""
        print("subscription lost")
        sys.exit(1)

    async def post_handler(self, request: web.Request) -> web.Response:
        """POST callback for onvif HTTP notifications."""
        print(request)
        print(request.url)
        for k, v in request.headers.items():
            print(f"{k}: {v}")
        body = await request.content.read()
        print(body)
        if self.manager is None:
            raise RuntimeError("Received notification but manager is not set up")
        result = self.manager.process(body)
        if not result:
            print("failed to process notification")
        else:
            await self.parse_messages(result.NotificationMessage)
        return web.Response()

    async def webhook(self) -> None:
        """Runs a webhook server to receive ONVIF notifications."""
        app = web.Application()
        app.add_routes([web.post("/", self.post_handler)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(
            runner, self.args.notification_address, self.args.notification_port
        )
        await site.start()

        receive_url = (
            f"http://{self.args.notification_address}:{self.args.notification_port}/"
        )
        self.manager = await self.cam.create_notification_manager(
            receive_url,
            datetime.timedelta(minutes=self.args.subscription_time),
            self.subscription_lost,
        )
        await self.manager.set_synchronization_point()

        print(f"waiting for messages at {receive_url}...")
        await asyncio.sleep(
            datetime.timedelta(minutes=self.args.wait_time).total_seconds()
        )

    async def pullpoint(self) -> None:
        """Runs pullpoint to receive ONVIF notifications."""
        self.manager = await self.cam.create_pullpoint_manager(
            datetime.timedelta(minutes=self.args.subscription_time),
            self.subscription_lost,
        )
        await self.manager.set_synchronization_point()
        pullpoint = self.manager.get_service()

        loop = asyncio.get_event_loop()
        end_time = (
            loop.time()
            + datetime.timedelta(minutes=self.args.wait_time).total_seconds()
        )
        print("waiting for messages...")
        while loop.time() < end_time:
            messages = await pullpoint.PullMessages(
                {
                    "MessageLimit": 5,
                    "Timeout": datetime.timedelta(seconds=30),
                }
            )
            if not messages or not messages.NotificationMessage:
                print("no messages received")
                continue
            await self.parse_messages(messages.NotificationMessage)

    async def parse_messages(self, messages: list[typing.Any]) -> None:
        """Parse incoming messages."""
        print(f"parsing {len(messages)} message")
        for msg in messages:
            topic = getattr(msg.Topic, "_value_1", None)

            def debug_msg(m: typing.Any = msg) -> typing.Any:
                """Shorthand to print the message for debugging."""
                return onvif_parsers.util.event_to_debug_format(m)

            if not topic:
                print(f"message missing topic, skipping {debug_msg()}")
                continue
            try:
                result = await onvif_parsers.parse(topic, "uid", msg)
            except onvif_parsers.errors.UnknownTopicError as e:
                print(f"unknown topic {e}: {topic}, skipping: {debug_msg()}")
                continue
            except (AttributeError, KeyError) as e:
                print(
                    f"invalid message structure for topic {topic}: {e}, skipping: "
                    f"{debug_msg()}"
                )
                continue
            if not result:
                print(f"failed to parse message with topic {topic}: {debug_msg()}")
            else:
                print(f"parsed message with topic {topic}: {result}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="OnvifEventReceiver",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host", default="192.168.3.10", help="ONVIF Camera hostname or IP address"
    )
    parser.add_argument("--port", type=int, default=2020, help="ONVIF Camera port")
    parser.add_argument(
        "--username",
        default="hass",  # codespell:ignore
        help="ONVIF Camera username",
    )
    parser.add_argument("--password", default="peek4boo", help="ONVIF Camera password")
    parser.add_argument(
        "--notification",
        action=argparse.BooleanOptionalAction,
        help=(
            "Use notification (webhook) instead of pullpoint. "
            "Many cameras have better support for webhook than pullpoint."
        ),
    )
    parser.add_argument(
        "--notification_address",
        default=get_local_ip(),
        help=(
            "Notification listen address. The camera must be able to reach this "
            "address. The default tries to determine your local IP address."
        ),
    )
    parser.add_argument(
        "--notification_port",
        type=int,
        default=8976,
        help="HTTP port to listen on for webhook HTTP notifications.",
    )
    parser.add_argument(
        "--subscription_time",
        type=int,
        default=1,
        help="Subscription time in minutes. This is how long an ONVIF notification "
        "subscription lasts before needing to be renewed. You likely don't need to "
        "change this.",
    )
    parser.add_argument(
        "--wait_time",
        type=int,
        default=1,
        help="Time in minutes to wait for events. After this time the program exits.",
    )

    args = parser.parse_args(sys.argv[1:])
    if args.notification and args.notification_address is None:
        parser.error("--notification requires --notification_address")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(OnvifEventReceiver.run(args))
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt")
        pass


if __name__ == "__main__":
    main()
