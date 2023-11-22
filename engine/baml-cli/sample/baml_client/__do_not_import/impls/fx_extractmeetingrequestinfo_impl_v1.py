# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.

# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

from ..clients.client_main import Main
from ..functions.fx_extractmeetingrequestinfo import BAMLExtractMeetingRequestInfo
from ..types.classes.cls_attendee import Attendee
from ..types.classes.cls_meetingrequest import MeetingRequest
from baml_lib._impl.deserializer import Deserializer


# Impl: v1
# Client: Main
# An implementation of .


__prompt_template = """\
Given a user is trying to schedule a meeting, extract the relevant
information from the query.

Context:
```
Today is {now}
```

Query:
```
{query}
```

Output JSON:
{
  // Either an exact time, or a relative time. Use ISO 8601 Duration Format
  // when specifying a relative time (e.g. P1D for 1 day from now).
  "when": string,
  "attendees": {
    "name": string,
    "email": string
  }[],
  "topic": string
}

JSON:\
"""

__input_replacers = {
    "{now}",
    "{query}"
}


# We ignore the type here because baml does some type magic to make this work
# for inline SpecialForms like Optional, Union, List.
__deserializer = Deserializer[MeetingRequest](MeetingRequest)  # type: ignore






@BAMLExtractMeetingRequestInfo.register_impl("v1")
async def v1(*, query: str, now: str) -> MeetingRequest:
    response = await Main.run_prompt_template(template=__prompt_template, replacers=__input_replacers, params=dict(query=query, now=now))
    deserialized = __deserializer.from_string(response.generated)
    return deserialized