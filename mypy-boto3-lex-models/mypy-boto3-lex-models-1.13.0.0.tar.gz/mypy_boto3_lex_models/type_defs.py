"""
Main interface for lex-models service type definitions.

Usage::

    from mypy_boto3.lex_models.type_defs import CodeHookTypeDef

    data: CodeHookTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CodeHookTypeDef",
    "LogSettingsRequestTypeDef",
    "ConversationLogsRequestTypeDef",
    "IntentTypeDef",
    "MessageTypeDef",
    "PromptTypeDef",
    "StatementTypeDef",
    "CreateBotVersionResponseTypeDef",
    "FollowUpPromptTypeDef",
    "FulfillmentActivityTypeDef",
    "SlotTypeDef",
    "CreateIntentVersionResponseTypeDef",
    "EnumerationValueTypeDef",
    "SlotTypeRegexConfigurationTypeDef",
    "SlotTypeConfigurationTypeDef",
    "CreateSlotTypeVersionResponseTypeDef",
    "LogSettingsResponseTypeDef",
    "ConversationLogsResponseTypeDef",
    "GetBotAliasResponseTypeDef",
    "BotAliasMetadataTypeDef",
    "GetBotAliasesResponseTypeDef",
    "GetBotChannelAssociationResponseTypeDef",
    "BotChannelAssociationTypeDef",
    "GetBotChannelAssociationsResponseTypeDef",
    "GetBotResponseTypeDef",
    "BotMetadataTypeDef",
    "GetBotVersionsResponseTypeDef",
    "GetBotsResponseTypeDef",
    "BuiltinIntentSlotTypeDef",
    "GetBuiltinIntentResponseTypeDef",
    "BuiltinIntentMetadataTypeDef",
    "GetBuiltinIntentsResponseTypeDef",
    "BuiltinSlotTypeMetadataTypeDef",
    "GetBuiltinSlotTypesResponseTypeDef",
    "GetExportResponseTypeDef",
    "GetImportResponseTypeDef",
    "GetIntentResponseTypeDef",
    "IntentMetadataTypeDef",
    "GetIntentVersionsResponseTypeDef",
    "GetIntentsResponseTypeDef",
    "GetSlotTypeResponseTypeDef",
    "SlotTypeMetadataTypeDef",
    "GetSlotTypeVersionsResponseTypeDef",
    "GetSlotTypesResponseTypeDef",
    "UtteranceDataTypeDef",
    "UtteranceListTypeDef",
    "GetUtterancesViewResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutBotAliasResponseTypeDef",
    "PutBotResponseTypeDef",
    "PutIntentResponseTypeDef",
    "PutSlotTypeResponseTypeDef",
    "StartImportResponseTypeDef",
)

CodeHookTypeDef = TypedDict("CodeHookTypeDef", {"uri": str, "messageVersion": str})

_RequiredLogSettingsRequestTypeDef = TypedDict(
    "_RequiredLogSettingsRequestTypeDef",
    {
        "logType": Literal["AUDIO", "TEXT"],
        "destination": Literal["CLOUDWATCH_LOGS", "S3"],
        "resourceArn": str,
    },
)
_OptionalLogSettingsRequestTypeDef = TypedDict(
    "_OptionalLogSettingsRequestTypeDef", {"kmsKeyArn": str}, total=False
)


class LogSettingsRequestTypeDef(
    _RequiredLogSettingsRequestTypeDef, _OptionalLogSettingsRequestTypeDef
):
    pass


ConversationLogsRequestTypeDef = TypedDict(
    "ConversationLogsRequestTypeDef",
    {"logSettings": List[LogSettingsRequestTypeDef], "iamRoleArn": str},
)

IntentTypeDef = TypedDict("IntentTypeDef", {"intentName": str, "intentVersion": str})

_RequiredMessageTypeDef = TypedDict(
    "_RequiredMessageTypeDef",
    {"contentType": Literal["PlainText", "SSML", "CustomPayload"], "content": str},
)
_OptionalMessageTypeDef = TypedDict("_OptionalMessageTypeDef", {"groupNumber": int}, total=False)


class MessageTypeDef(_RequiredMessageTypeDef, _OptionalMessageTypeDef):
    pass


_RequiredPromptTypeDef = TypedDict(
    "_RequiredPromptTypeDef", {"messages": List[MessageTypeDef], "maxAttempts": int}
)
_OptionalPromptTypeDef = TypedDict("_OptionalPromptTypeDef", {"responseCard": str}, total=False)


class PromptTypeDef(_RequiredPromptTypeDef, _OptionalPromptTypeDef):
    pass


_RequiredStatementTypeDef = TypedDict(
    "_RequiredStatementTypeDef", {"messages": List[MessageTypeDef]}
)
_OptionalStatementTypeDef = TypedDict(
    "_OptionalStatementTypeDef", {"responseCard": str}, total=False
)


class StatementTypeDef(_RequiredStatementTypeDef, _OptionalStatementTypeDef):
    pass


CreateBotVersionResponseTypeDef = TypedDict(
    "CreateBotVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": Literal["BUILDING", "READY", "READY_BASIC_TESTING", "FAILED", "NOT_BUILT"],
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Literal["en-US", "en-GB", "de-DE"],
        "childDirected": bool,
        "detectSentiment": bool,
    },
    total=False,
)

FollowUpPromptTypeDef = TypedDict(
    "FollowUpPromptTypeDef", {"prompt": PromptTypeDef, "rejectionStatement": StatementTypeDef}
)

_RequiredFulfillmentActivityTypeDef = TypedDict(
    "_RequiredFulfillmentActivityTypeDef", {"type": Literal["ReturnIntent", "CodeHook"]}
)
_OptionalFulfillmentActivityTypeDef = TypedDict(
    "_OptionalFulfillmentActivityTypeDef", {"codeHook": CodeHookTypeDef}, total=False
)


class FulfillmentActivityTypeDef(
    _RequiredFulfillmentActivityTypeDef, _OptionalFulfillmentActivityTypeDef
):
    pass


_RequiredSlotTypeDef = TypedDict(
    "_RequiredSlotTypeDef", {"name": str, "slotConstraint": Literal["Required", "Optional"]}
)
_OptionalSlotTypeDef = TypedDict(
    "_OptionalSlotTypeDef",
    {
        "description": str,
        "slotType": str,
        "slotTypeVersion": str,
        "valueElicitationPrompt": PromptTypeDef,
        "priority": int,
        "sampleUtterances": List[str],
        "responseCard": str,
        "obfuscationSetting": Literal["NONE", "DEFAULT_OBFUSCATION"],
    },
    total=False,
)


class SlotTypeDef(_RequiredSlotTypeDef, _OptionalSlotTypeDef):
    pass


CreateIntentVersionResponseTypeDef = TypedDict(
    "CreateIntentVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
    },
    total=False,
)

_RequiredEnumerationValueTypeDef = TypedDict("_RequiredEnumerationValueTypeDef", {"value": str})
_OptionalEnumerationValueTypeDef = TypedDict(
    "_OptionalEnumerationValueTypeDef", {"synonyms": List[str]}, total=False
)


class EnumerationValueTypeDef(_RequiredEnumerationValueTypeDef, _OptionalEnumerationValueTypeDef):
    pass


SlotTypeRegexConfigurationTypeDef = TypedDict("SlotTypeRegexConfigurationTypeDef", {"pattern": str})

SlotTypeConfigurationTypeDef = TypedDict(
    "SlotTypeConfigurationTypeDef",
    {"regexConfiguration": SlotTypeRegexConfigurationTypeDef},
    total=False,
)

CreateSlotTypeVersionResponseTypeDef = TypedDict(
    "CreateSlotTypeVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": Literal["ORIGINAL_VALUE", "TOP_RESOLUTION"],
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
    },
    total=False,
)

LogSettingsResponseTypeDef = TypedDict(
    "LogSettingsResponseTypeDef",
    {
        "logType": Literal["AUDIO", "TEXT"],
        "destination": Literal["CLOUDWATCH_LOGS", "S3"],
        "kmsKeyArn": str,
        "resourceArn": str,
        "resourcePrefix": str,
    },
    total=False,
)

ConversationLogsResponseTypeDef = TypedDict(
    "ConversationLogsResponseTypeDef",
    {"logSettings": List[LogSettingsResponseTypeDef], "iamRoleArn": str},
    total=False,
)

GetBotAliasResponseTypeDef = TypedDict(
    "GetBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
    },
    total=False,
)

BotAliasMetadataTypeDef = TypedDict(
    "BotAliasMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
    },
    total=False,
)

GetBotAliasesResponseTypeDef = TypedDict(
    "GetBotAliasesResponseTypeDef",
    {"BotAliases": List[BotAliasMetadataTypeDef], "nextToken": str},
    total=False,
)

GetBotChannelAssociationResponseTypeDef = TypedDict(
    "GetBotChannelAssociationResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": Literal["Facebook", "Slack", "Twilio-Sms", "Kik"],
        "botConfiguration": Dict[str, str],
        "status": Literal["IN_PROGRESS", "CREATED", "FAILED"],
        "failureReason": str,
    },
    total=False,
)

BotChannelAssociationTypeDef = TypedDict(
    "BotChannelAssociationTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": Literal["Facebook", "Slack", "Twilio-Sms", "Kik"],
        "botConfiguration": Dict[str, str],
        "status": Literal["IN_PROGRESS", "CREATED", "FAILED"],
        "failureReason": str,
    },
    total=False,
)

GetBotChannelAssociationsResponseTypeDef = TypedDict(
    "GetBotChannelAssociationsResponseTypeDef",
    {"botChannelAssociations": List[BotChannelAssociationTypeDef], "nextToken": str},
    total=False,
)

GetBotResponseTypeDef = TypedDict(
    "GetBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": Literal["BUILDING", "READY", "READY_BASIC_TESTING", "FAILED", "NOT_BUILT"],
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Literal["en-US", "en-GB", "de-DE"],
        "childDirected": bool,
        "detectSentiment": bool,
    },
    total=False,
)

BotMetadataTypeDef = TypedDict(
    "BotMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "status": Literal["BUILDING", "READY", "READY_BASIC_TESTING", "FAILED", "NOT_BUILT"],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

GetBotVersionsResponseTypeDef = TypedDict(
    "GetBotVersionsResponseTypeDef",
    {"bots": List[BotMetadataTypeDef], "nextToken": str},
    total=False,
)

GetBotsResponseTypeDef = TypedDict(
    "GetBotsResponseTypeDef", {"bots": List[BotMetadataTypeDef], "nextToken": str}, total=False
)

BuiltinIntentSlotTypeDef = TypedDict("BuiltinIntentSlotTypeDef", {"name": str}, total=False)

GetBuiltinIntentResponseTypeDef = TypedDict(
    "GetBuiltinIntentResponseTypeDef",
    {
        "signature": str,
        "supportedLocales": List[Literal["en-US", "en-GB", "de-DE"]],
        "slots": List[BuiltinIntentSlotTypeDef],
    },
    total=False,
)

BuiltinIntentMetadataTypeDef = TypedDict(
    "BuiltinIntentMetadataTypeDef",
    {"signature": str, "supportedLocales": List[Literal["en-US", "en-GB", "de-DE"]]},
    total=False,
)

GetBuiltinIntentsResponseTypeDef = TypedDict(
    "GetBuiltinIntentsResponseTypeDef",
    {"intents": List[BuiltinIntentMetadataTypeDef], "nextToken": str},
    total=False,
)

BuiltinSlotTypeMetadataTypeDef = TypedDict(
    "BuiltinSlotTypeMetadataTypeDef",
    {"signature": str, "supportedLocales": List[Literal["en-US", "en-GB", "de-DE"]]},
    total=False,
)

GetBuiltinSlotTypesResponseTypeDef = TypedDict(
    "GetBuiltinSlotTypesResponseTypeDef",
    {"slotTypes": List[BuiltinSlotTypeMetadataTypeDef], "nextToken": str},
    total=False,
)

GetExportResponseTypeDef = TypedDict(
    "GetExportResponseTypeDef",
    {
        "name": str,
        "version": str,
        "resourceType": Literal["BOT", "INTENT", "SLOT_TYPE"],
        "exportType": Literal["ALEXA_SKILLS_KIT", "LEX"],
        "exportStatus": Literal["IN_PROGRESS", "READY", "FAILED"],
        "failureReason": str,
        "url": str,
    },
    total=False,
)

GetImportResponseTypeDef = TypedDict(
    "GetImportResponseTypeDef",
    {
        "name": str,
        "resourceType": Literal["BOT", "INTENT", "SLOT_TYPE"],
        "mergeStrategy": Literal["OVERWRITE_LATEST", "FAIL_ON_CONFLICT"],
        "importId": str,
        "importStatus": Literal["IN_PROGRESS", "COMPLETE", "FAILED"],
        "failureReason": List[str],
        "createdDate": datetime,
    },
    total=False,
)

GetIntentResponseTypeDef = TypedDict(
    "GetIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
    },
    total=False,
)

IntentMetadataTypeDef = TypedDict(
    "IntentMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

GetIntentVersionsResponseTypeDef = TypedDict(
    "GetIntentVersionsResponseTypeDef",
    {"intents": List[IntentMetadataTypeDef], "nextToken": str},
    total=False,
)

GetIntentsResponseTypeDef = TypedDict(
    "GetIntentsResponseTypeDef",
    {"intents": List[IntentMetadataTypeDef], "nextToken": str},
    total=False,
)

GetSlotTypeResponseTypeDef = TypedDict(
    "GetSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": Literal["ORIGINAL_VALUE", "TOP_RESOLUTION"],
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
    },
    total=False,
)

SlotTypeMetadataTypeDef = TypedDict(
    "SlotTypeMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

GetSlotTypeVersionsResponseTypeDef = TypedDict(
    "GetSlotTypeVersionsResponseTypeDef",
    {"slotTypes": List[SlotTypeMetadataTypeDef], "nextToken": str},
    total=False,
)

GetSlotTypesResponseTypeDef = TypedDict(
    "GetSlotTypesResponseTypeDef",
    {"slotTypes": List[SlotTypeMetadataTypeDef], "nextToken": str},
    total=False,
)

UtteranceDataTypeDef = TypedDict(
    "UtteranceDataTypeDef",
    {
        "utteranceString": str,
        "count": int,
        "distinctUsers": int,
        "firstUtteredDate": datetime,
        "lastUtteredDate": datetime,
    },
    total=False,
)

UtteranceListTypeDef = TypedDict(
    "UtteranceListTypeDef",
    {"botVersion": str, "utterances": List[UtteranceDataTypeDef]},
    total=False,
)

GetUtterancesViewResponseTypeDef = TypedDict(
    "GetUtterancesViewResponseTypeDef",
    {"botName": str, "utterances": List[UtteranceListTypeDef]},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": List[TagTypeDef]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutBotAliasResponseTypeDef = TypedDict(
    "PutBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
        "tags": List[TagTypeDef],
    },
    total=False,
)

PutBotResponseTypeDef = TypedDict(
    "PutBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": Literal["BUILDING", "READY", "READY_BASIC_TESTING", "FAILED", "NOT_BUILT"],
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": Literal["en-US", "en-GB", "de-DE"],
        "childDirected": bool,
        "createVersion": bool,
        "detectSentiment": bool,
        "tags": List[TagTypeDef],
    },
    total=False,
)

PutIntentResponseTypeDef = TypedDict(
    "PutIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "createVersion": bool,
    },
    total=False,
)

PutSlotTypeResponseTypeDef = TypedDict(
    "PutSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": Literal["ORIGINAL_VALUE", "TOP_RESOLUTION"],
        "createVersion": bool,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
    },
    total=False,
)

StartImportResponseTypeDef = TypedDict(
    "StartImportResponseTypeDef",
    {
        "name": str,
        "resourceType": Literal["BOT", "INTENT", "SLOT_TYPE"],
        "mergeStrategy": Literal["OVERWRITE_LATEST", "FAIL_ON_CONFLICT"],
        "importId": str,
        "importStatus": Literal["IN_PROGRESS", "COMPLETE", "FAILED"],
        "tags": List[TagTypeDef],
        "createdDate": datetime,
    },
    total=False,
)
