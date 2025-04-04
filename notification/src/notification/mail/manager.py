from logging import Logger

from plant_common.env import config
from plant_common.message.severity import Severity

from notification.mail.abstract_mailbox import AbstractMailbox
from notification.mail.gmail.mailbox import GmailMailbox
from notification.mail.mock.mock import MockMailbox
from notification.mail.model import Message
from notification.mail.sns.mailbox import SnsMailbox

MAILBOX_CLS = {"GMAIL": GmailMailbox, "AWS": SnsMailbox, "MOCK": MockMailbox}


class MessageManager:

    def __init__(
        self,
        to: list[str],
        topic: str,
        content: str,
        severity: Severity,
        logger: Logger,
    ):

        self.message = Message.build(
            receivers=to,
            sender=config.get("SENDER", ""),
            topic=topic,
            content=content,
            severity=severity,
        )
        self.logger = logger

    def send(self):
        MailboxCls: AbstractMailbox = MAILBOX_CLS[config["MAILBOX"]]
        mailbox = MailboxCls(self.message, self.logger)
        mailbox.send()
