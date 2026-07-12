from typing import TYPE_CHECKING, Annotated, Literal, overload
from typing_extensions import Unpack

from .read import AuditLog, AutoModerationAction, AutoModerationRule, TriggerMetadata
from .types import AuditLogEventType, AutoModerationRuleEventType, TriggerType
from .write import (
    CreateAutoModerationRuleParams,
    ModifyAutoModerationRuleParams,
)
from ...api.validation import (
    AtMostOne,
    ForbidIfEquals,
    Range,
    RequireIfNotEquals,
    validate,
    validate_outbound_value,
)
from ...protocol import UNSET, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot

NonSpamTriggerType = Literal[
    TriggerType.KEYWORD,
    TriggerType.KEYWORD_PRESET,
    TriggerType.MENTION_SPAM,
    TriggerType.MEMBER_PROFILE,
]


class ModerationEndpointMixin:
    @overload
    async def _api_get_guild_audit_log(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @overload
    async def _api_get_guild_audit_log(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("before", "after"),
                message="before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_guild_audit_log(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog:
        """Get guild audit log.

        see https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log
        """

        data = {
            "user_id": user_id,
            "action_type": action_type,
            "before": before,
            "after": after,
            "limit": limit,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/audit-logs",
            response=JsonResponse(AuditLog),
            auth=BotAuth(bot.bot_info),
            query=data,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_auto_moderation_rules_for_guild(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[AutoModerationRule]:
        """List auto moderation rules for guild.

        see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            response=JsonResponse(list[AutoModerationRule]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
    ) -> AutoModerationRule:
        """Get auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @overload
    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: Literal[TriggerType.SPAM],
        actions: list[AutoModerationAction],
        trigger_metadata: None = None,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    @overload
    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: NonSpamTriggerType,
        actions: list[AutoModerationAction],
        trigger_metadata: TriggerMetadata,
        enabled: bool | None = None,
        exempt_roles: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = None,
        exempt_channels: Annotated[
            list[SnowflakeType] | None,
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = None,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    @validate(
        cross_rules=(
            ForbidIfEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata must be omitted for SPAM rules",
            ),
            RequireIfNotEquals(
                field="trigger_metadata",
                when_field="trigger_type",
                equals=TriggerType.SPAM,
                message="trigger_metadata is required for this trigger_type",
            ),
        )
    )
    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateAutoModerationRuleParams],
    ) -> AutoModerationRule:
        """Create auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
        """
        fields = validate_outbound_value(CreateAutoModerationRuleParams, fields)
        name = fields["name"]
        event_type = fields["event_type"]
        trigger_type = fields["trigger_type"]
        trigger_metadata = fields.get("trigger_metadata")
        actions = fields["actions"]
        enabled = fields.get("enabled")
        exempt_roles = fields.get("exempt_roles")
        exempt_channels = fields.get("exempt_channels")

        data = {
            "name": name,
            "event_type": event_type,
            "trigger_type": trigger_type,
            "actions": actions,
            "trigger_metadata": trigger_metadata,
            "enabled": enabled,
            "exempt_roles": exempt_roles,
            "exempt_channels": exempt_channels,
        }
        data = validate_outbound_value(
            CreateAutoModerationRuleParams,
            {
                key: value
                for key, value in {
                    key: value for key, value in data.items() if value is not None
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_modify_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyAutoModerationRuleParams],
    ) -> AutoModerationRule:
        """Modify auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        fields = validate_outbound_value(ModifyAutoModerationRuleParams, fields)
        name = fields.get("name")
        event_type = fields.get("event_type")
        trigger_metadata = fields.get("trigger_metadata")
        actions = fields.get("actions")
        enabled = fields.get("enabled")
        exempt_roles = fields.get("exempt_roles")
        exempt_channels = fields.get("exempt_channels")

        data = {
            "name": name,
            "event_type": event_type,
            "trigger_metadata": trigger_metadata,
            "actions": actions,
            "enabled": enabled,
            "exempt_roles": exempt_roles,
            "exempt_channels": exempt_channels,
        }
        data = validate_outbound_value(
            ModifyAutoModerationRuleParams,
            {
                key: value
                for key, value in {
                    key: value for (key, value) in data.items() if value is not None
                }.items()
                if value is not UNSET
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["ModerationEndpointMixin"]
