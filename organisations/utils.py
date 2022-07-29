from enum import Enum, unique


@unique
class InvitationStates(Enum):
    """Defines two states of invitation.
    After invitation created, state must be "created";
    After user accepts invitation, state must be "used".
    """

    created = "c"
    used = "u"
